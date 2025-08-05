import os
import tempfile
import shutil
import uuid
from zipfile import ZipFile
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from loguru import logger
from database.db import get_db
from database.models import DIPublication
from models.publication import Publication
from services.xml_parser import XmlParser
from services.amqp_publisher import AmqpPublisher

router = APIRouter()

@router.post("/upload", status_code=201)
async def upload_zip(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Processa arquivo ZIP contendo XMLs do Diário Oficial e armazena no banco de dados
    """
    if not file.filename.endswith('.zip'):
        raise HTTPException(400, detail="Apenas arquivos .zip são aceitos")

    processed_files = 0
    saved_publications = 0
    errors = 0
    batch_size = 100  # Processa em lotes para melhor performance

    try:
        # Salva o arquivo temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        logger.info(f"Arquivo {file.filename} salvo temporariamente em {tmp_path}")

        # Extrai arquivos do ZIP
        with ZipFile(tmp_path, 'r') as zip_ref:
            extract_dir = tempfile.mkdtemp()
            zip_ref.extractall(extract_dir)
            xml_files = [f for f in zip_ref.namelist() if f.endswith('.xml')]
        logger.info(f"Extraídos {len(xml_files)} arquivos XML")

        if not xml_files:
            raise HTTPException(400, detail="Nenhum arquivo XML encontrado no ZIP")

        publications = []
        
        # Processa cada XML
        for xml_file in xml_files:
            xml_path = os.path.join(extract_dir, xml_file)
            try:
                with open(xml_path, 'r', encoding='utf-8') as f:
                    xml_content = f.read()
                
                parser = XmlParser(xml_content)
                pub_data = parser.parse()
                
                for pub in pub_data:
                    if not isinstance(pub, dict):
                        logger.warning(f"Publicação inválida no arquivo {xml_file}")
                        errors += 1
                        continue
                    
                    # Garante que cada publicação tenha um ID
                    pub['id'] = pub.get('id') or str(uuid.uuid4())
                    
                    # Converte e valida a data
                    if pub.get('pubDate'):
                        try:
                            pub['pubDate'] = datetime.strptime(pub['pubDate'], "%d/%m/%Y").replace(tzinfo=timezone.utc)
                        except ValueError as e:
                            logger.error(f"Data inválida no arquivo {xml_file}: {e}")
                            pub['pubDate'] = None
                    
                    # Trunca campos muito longos para evitar erros
                    pub['name'] = pub.get('name', '')[:500] if pub.get('name') else None
                    
                    publications.append(pub)
                    processed_files += 1
                    
            except Exception as e:
                logger.error(f"Erro ao processar {xml_file}: {str(e)}")
                errors += 1
                continue

        # Armazena no PostgreSQL em lotes
        try:
            for i in range(0, len(publications), batch_size):
                batch = publications[i:i + batch_size]
                
                for pub in batch:
                    try:
                        db_pub = DIPublication(
                            id=pub['id'],
                            name=pub.get('name', '')[:500],
                            idOficio=pub.get('idOficio'),
                            pubName=pub.get('pubName', '')[:200],
                            artType=pub.get('artType', '')[:100],
                            pubDate=pub.get('pubDate'),
                            artClass=pub.get('artClass'),
                            artCategory=pub.get('artCategory'),
                            artSize=pub.get('artSize'),
                            artNotes=pub.get('artNotes'),
                            numberPage=pub.get('numberPage'),
                            pdfPage=pub.get('pdfPage'),
                            editionNumber=pub.get('editionNumber'),
                            highlightType=pub.get('highlightType'),
                            highlightPriority=pub.get('highlightPriority'),
                            highlight=pub.get('highlight'),
                            highlightimage=pub.get('highlightimage'),
                            highlightimagename=pub.get('highlightimagename'),
                            idMateria=pub.get('idMateria'),
                            body=json.dumps(pub.get('body')) if pub.get('body') else None,
                            midias=json.dumps(pub.get('midias')) if pub.get('midias') else None
                        )
                        db.merge(db_pub)
                        saved_publications += 1
                    
                    except Exception as e:
                        logger.error(f"Erro ao preparar publicação {pub.get('id')}: {str(e)}")
                        errors += 1
                        continue
                
                db.commit()
            
            logger.info(f"Salvas {saved_publications} publicações no banco de dados")

        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao salvar no banco de dados: {str(e)}")
            raise HTTPException(500, detail=f"Erro ao salvar no banco de dados: {str(e)}")

        # Publica no RabbitMQ em lotes
        if saved_publications > 0:
            try:
                with AmqpPublisher() as publisher:
                    for i in range(0, len(publications), batch_size):
                        batch = publications[i:i + batch_size]
                        for pub in batch:
                            try:
                                publisher.publish({
                                    'id': pub['id'],
                                    'name': pub.get('name', '')[:500],
                                    'idOficio': pub.get('idOficio'),
                                    'pubName': pub.get('pubName', '')[:200],
                                    'artType': pub.get('artType', '')[:100],
                                    'pubDate': pub.get('pubDate').isoformat() if pub.get('pubDate') else None,
                                    'artClass': pub.get('artClass'),
                                    'artCategory': pub.get('artCategory'),
                                    'artSize': pub.get('artSize'),
                                    'artNotes': pub.get('artNotes'),
                                    'numberPage': pub.get('numberPage'),
                                    'pdfPage': pub.get('pdfPage'),
                                    'editionNumber': pub.get('editionNumber'),
                                    'highlightType': pub.get('highlightType'),
                                    'highlightPriority': pub.get('highlightPriority'),
                                    'highlight': pub.get('highlight'),
                                    'highlightimage': pub.get('highlightimage'),
                                    'highlightimagename': pub.get('highlightimagename'),
                                    'idMateria': pub.get('idMateria'),
                                    'body': pub.get('body'),  # Já deve estar em formato dicionário
                                    'midias': pub.get('midias')  # Já deve estar em formato dicionário
                                })
                            except Exception as e:
                                logger.error(f"Erro ao publicar no RabbitMQ: {str(e)}")
                                continue
            except Exception as e:
                logger.error(f"Erro na conexão com RabbitMQ: {str(e)}")
                
        return {
            "message": "Arquivo processado com sucesso",
            "publications_processed": processed_files,
            "publications_saved": saved_publications,
            "xml_files_processed": len(xml_files),
            "errors": errors
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro geral no processamento: {str(e)}")
        raise HTTPException(500, detail=f"Erro no processamento: {str(e)}")
    
    finally:
        try:
            if 'tmp_path' in locals() and os.path.exists(tmp_path):
                os.unlink(tmp_path)
            if 'extract_dir' in locals() and os.path.exists(extract_dir):
                shutil.rmtree(extract_dir)
        except Exception as e:
            logger.error(f"Erro na limpeza de arquivos temporários: {str(e)}")

@router.get("/publications", response_model=List[Publication])
async def get_publications(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    art_type: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Retorna publicações com filtros avançados
    """
    query = db.query(DIPublication)

    # Filtros de data
    if start_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(DIPublication.pubDate >= start)
        except ValueError:
            raise HTTPException(400, detail="Formato de data inválido (use YYYY-MM-DD)")
    
    if end_date:
        try:
            end = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(DIPublication.pubDate <= end)
        except ValueError:
            raise HTTPException(400, detail="Formato de data inválido (use YYYY-MM-DD)")

    # Filtro por tipo
    if art_type:
        query = query.filter(DIPublication.artType.ilike(f"%{art_type}%"))

    # Busca geral
    if search:
        search_filter = (
            DIPublication.name.ilike(f"%{search}%") |
            DIPublication.pubName.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    # Ordenação e paginação
    results = query.order_by(
        DIPublication.pubDate.desc(),
        DIPublication.id
    ).offset(skip).limit(limit).all()

    if not results:
        raise HTTPException(404, detail="Nenhuma publicação encontrada")

    return results

@router.get("/publications/{pub_id}", response_model=Publication)
async def get_publication(
    pub_id: str,
    db: Session = Depends(get_db)
):
    """
    Obtém uma publicação específica por ID
    """
    publication = db.query(DIPublication).filter(DIPublication.id == pub_id).first()
    
    if not publication:
        raise HTTPException(404, detail="Publicação não encontrada")
    
    return publication

@router.get("/publications/count")
async def count_publications(
    db: Session = Depends(get_db),
    art_type: Optional[str] = None
):
    """
    Retorna o total de publicações armazenadas
    """
    query = db.query(DIPublication)
    
    if art_type:
        query = query.filter(DIPublication.artType == art_type)
    
    count = query.count()
    
    return {"count": count}
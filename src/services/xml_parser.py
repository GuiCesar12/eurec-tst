import uuid


class XmlParser:
    def __init__(self, xml_content):
        self.xml_content = xml_content

    def parse(self):
        import xml.etree.ElementTree as ET
        
        root = ET.fromstring(self.xml_content)
        publications = []

        for article in root.findall('article'):
            publication = {
                'id': article.get('id', str(uuid.uuid4())),  # Gera ID se não existir
                'name': article.get('name', ''),
                'idOficio': article.get('idOficio'),
                'name': article.get('name'),
                'idOficio': article.get('idOficio'),
                'pubName': article.get('pubName'),
                'artType': article.get('artType'),
                'pubDate': article.get('pubDate'),
                'artClass': article.get('artClass'),
                'artCategory': article.get('artCategory'),
                'artSize': article.get('artSize'),
                'artNotes': article.get('artNotes'),
                'numberPage': article.get('numberPage'),
                'pdfPage': article.get('pdfPage'),
                'editionNumber': article.get('editionNumber'),
                'highlightType': article.get('highlightType'),
                'highlightPriority': article.get('highlightPriority'),
                'highlight': article.get('highlight'),
                'highlightimage': article.get('highlightimage'),
                'highlightimagename': article.get('highlightimagename'),
                'idMateria': article.get('idMateria'),
                'body': {
                    'Identifica': article.findtext('body/Identifica', '').strip(),
                    'Data': article.findtext('body/Data', '').strip(),
                    'Ementa': article.find('body/Ementa').text,
                    'Titulo': article.find('body/Titulo').text,
                    'SubTitulo': article.find('body/SubTitulo').text,
                    'Texto': article.find('body/Texto').text,
                },
                'midias': article.findtext('Midias', '').strip()
            }
            publications.append(publication)

        return publications
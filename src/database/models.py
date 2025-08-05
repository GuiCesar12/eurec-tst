from sqlalchemy import Column, String, JSON, DateTime, Text
from sqlalchemy.sql import func
from database.base import Base

class DIPublication(Base):
    __tablename__ = "di_publications"
    
    id = Column(String(100), primary_key=True, index=True)
    name = Column(Text)
    idOficio = Column(Text)
    pubName = Column(Text)
    artType = Column(Text)
    pubDate = Column(DateTime)
    artClass = Column(Text)
    artCategory = Column(Text)
    artSize = Column(Text)
    artNotes = Column(Text)
    numberPage = Column(Text)
    pdfPage = Column(Text)
    editionNumber = Column(Text)
    highlightType = Column(Text)
    highlightPriority = Column(Text)
    highlight = Column(Text)
    highlightimage = Column(Text)
    highlightimagename = Column(Text)
    idMateria = Column(Text)
    body = Column(JSON)
    midias = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
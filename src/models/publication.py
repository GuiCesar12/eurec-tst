import json
from pydantic import BaseModel, validator
from typing import Optional, Dict, Any
import uuid
from datetime import datetime

class PublicationBase(BaseModel):
    """Base model with common fields and validation"""
    id: str
    name: str
    idOficio: Optional[str] = None
    pubName: Optional[str] = None
    artType: Optional[str] = None
    pubDate: Optional[str] = None
    artClass: Optional[str] = None
    artCategory: Optional[str] = None
    artSize: Optional[str] = None
    artNotes: Optional[str] = None
    numberPage: Optional[str] = None
    pdfPage: Optional[str] = None
    editionNumber: Optional[str] = None
    highlightType: Optional[str] = None
    highlightPriority: Optional[str] = None
    highlight: Optional[str] = None
    highlightimage: Optional[str] = None
    highlightimagename: Optional[str] = None
    idMateria: Optional[str] = None
    body: Optional[Dict[str, Any]] = None
    midias: Optional[Dict[str, Any]] = None

    @validator('id', pre=True)
    def ensure_id(cls, v):
        return v or str(uuid.uuid4())

    @validator('pubDate', pre=True)
    def parse_date(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v

    @validator('body', 'midias', pre=True)
    def parse_json_fields(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return None
        return v

class PublicationCreate(PublicationBase):
    """Model for creating publications (additional validations can be added here)"""
    pass

class Publication(PublicationBase):
    """Complete publication model with ORM mode"""
    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class PublicationResponse(Publication):
    """Response model with additional metadata"""
    processed_at: Optional[datetime] = None
    source_file: Optional[str] = None
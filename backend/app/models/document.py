from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class DocumentStatus(str, Enum):
    """Document processing status"""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"
    DELETED = "deleted"


class DocumentType(str, Enum):
    """Document type enumeration"""
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"


class DocumentMetadata(BaseModel):
    """Document metadata model"""
    pages: Optional[int] = None
    word_count: Optional[int] = None
    file_size: int
    extraction_method: str
    language: Optional[str] = None
    author: Optional[str] = None
    title: Optional[str] = None
    creation_date: Optional[datetime] = None


class Document(BaseModel):
    """Document model"""
    id: str = Field(..., description="Unique document identifier")
    filename: str = Field(..., description="Original filename")
    file_path: str = Field(..., description="Path to stored file")
    document_type: DocumentType = Field(..., description="Document type")
    status: DocumentStatus = Field(default=DocumentStatus.UPLOADED)
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    processed_date: Optional[datetime] = None
    metadata: DocumentMetadata
    content: Optional[str] = None
    content_preview: Optional[str] = None
    
    class Config:
        use_enum_values = True


class DocumentChunk(BaseModel):
    """Document chunk model for vector storage"""
    id: str
    document_id: str
    chunk_index: int
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None
    
    class Config:
        arbitrary_types_allowed = True


class DocumentSearchResult(BaseModel):
    """Document search result model"""
    document_id: str
    chunk_id: str
    content: str
    score: float
    metadata: Dict[str, Any]
    highlights: Optional[List[str]] = None 
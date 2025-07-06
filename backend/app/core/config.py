from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    SERPER_API_KEY: Optional[str] = None
    
    # Database Configuration
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    REDIS_URL: str = "redis://localhost:6379"
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    
    # Application Configuration
    SECRET_KEY: str = "your-secret-key-change-in-production"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Server Configuration
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    FRONTEND_PORT: int = 3000
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = 10485760  # 10MB
    UPLOAD_DIRECTORY: str = "./uploads"
    ALLOWED_FILE_EXTENSIONS: list = [".pdf", ".docx", ".txt"]
    
    # Search Configuration
    DEFAULT_SEARCH_LIMIT: int = 10
    HYBRID_SEARCH_WEIGHTS_DENSE: float = 0.7
    HYBRID_SEARCH_WEIGHTS_SPARSE: float = 0.3
    RERANK_TOP_K: int = 20
    
    # Caching Configuration
    CACHE_TTL: int = 3600  # 1 hour
    ENABLE_CACHING: bool = True
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Model Configuration
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    RERANK_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    
    # Web Search Configuration
    WEB_SEARCH_ENABLED: bool = True
    WEB_SEARCH_TIMEOUT: int = 10
    WEB_SEARCH_MAX_RESULTS: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings() 
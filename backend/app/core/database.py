import asyncio
from typing import Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
import redis.asyncio as redis
from elasticsearch import AsyncElasticsearch

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# Global database connections
chroma_client: Optional[chromadb.Client] = None
redis_client: Optional[redis.Redis] = None
elasticsearch_client: Optional[AsyncElasticsearch] = None


async def initialize_databases() -> None:
    """Initialize all database connections"""
    global chroma_client, redis_client, elasticsearch_client
    
    try:
        # Initialize ChromaDB
        chroma_client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIRECTORY,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        logger.info("ChromaDB initialized successfully")
        
        # Initialize Redis
        redis_client = redis.from_url(settings.REDIS_URL)
        await redis_client.ping()
        logger.info("Redis connected successfully")
        
        # Initialize Elasticsearch
        elasticsearch_client = AsyncElasticsearch([settings.ELASTICSEARCH_URL])
        await elasticsearch_client.ping()
        logger.info("Elasticsearch connected successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


async def get_chroma_client() -> chromadb.Client:
    """Get ChromaDB client"""
    if chroma_client is None:
        raise RuntimeError("ChromaDB not initialized")
    return chroma_client


async def get_redis_client() -> redis.Redis:
    """Get Redis client"""
    if redis_client is None:
        raise RuntimeError("Redis not initialized")
    return redis_client


async def get_elasticsearch_client() -> AsyncElasticsearch:
    """Get Elasticsearch client"""
    if elasticsearch_client is None:
        raise RuntimeError("Elasticsearch not initialized")
    return elasticsearch_client


async def close_databases() -> None:
    """Close all database connections"""
    global redis_client, elasticsearch_client
    
    if redis_client:
        await redis_client.close()
        logger.info("Redis connection closed")
    
    if elasticsearch_client:
        await elasticsearch_client.close()
        logger.info("Elasticsearch connection closed") 
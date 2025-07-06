from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import Dict, Any, List
import os
import uuid
from pathlib import Path

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


def validate_file_extension(filename: str) -> bool:
    """Validate file extension"""
    file_ext = Path(filename).suffix.lower()
    return file_ext in settings.ALLOWED_FILE_EXTENSIONS


def validate_file_size(file_size: int) -> bool:
    """Validate file size"""
    return file_size <= settings.MAX_FILE_SIZE


@router.post("/file")
async def upload_file(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Upload a file for processing"""
    
    # Check if filename exists
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    # Validate file extension
    if not validate_file_extension(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"File type not supported. Allowed types: {settings.ALLOWED_FILE_EXTENSIONS}"
        )
    
    # Read file content to check size
    content = await file.read()
    if not validate_file_size(len(content)):
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE} bytes"
        )
    
    # Generate unique filename
    file_id = str(uuid.uuid4())
    file_extension = Path(file.filename).suffix
    unique_filename = f"{file_id}{file_extension}"
    file_path = Path(settings.UPLOAD_DIRECTORY) / unique_filename
    
    try:
        # Save file
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        logger.info(f"File uploaded successfully: {unique_filename}")
        
        # TODO: Queue file for processing
        # await queue_file_processing(file_path, file_id)
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "size": len(content),
            "status": "uploaded",
            "message": "File uploaded successfully and queued for processing"
        }
        
    except Exception as e:
        logger.error(f"File upload failed: {e}")
        # Clean up file if it was created
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail="File upload failed")


@router.get("/status/{file_id}")
async def get_upload_status(file_id: str) -> Dict[str, Any]:
    """Get upload and processing status"""
    # TODO: Implement actual status checking
    return {
        "file_id": file_id,
        "status": "processing",
        "progress": 50,
        "message": "File is being processed"
    }


@router.delete("/file/{file_id}")
async def delete_file(file_id: str) -> Dict[str, Any]:
    """Delete uploaded file"""
    # TODO: Implement file deletion logic
    return {
        "file_id": file_id,
        "status": "deleted",
        "message": "File deleted successfully"
    } 
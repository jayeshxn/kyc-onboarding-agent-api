from fastapi import FastAPI, HTTPException
from typing import Dict
import boto3
from botocore.exceptions import ClientError
import os
import tempfile
from pydantic import BaseModel
from dotenv import load_dotenv
import easyocr
import json
from agent import parse_kyc_documents
import io
from pathlib import Path
from enum import Enum

# Load environment variables
load_dotenv()

# Configuration
class StorageType(str, Enum):
    S3 = "s3"
    LOCAL = "local"

# Set this to change storage type
STORAGE_TYPE = StorageType.LOCAL  # Change to StorageType.S3 for S3 storage

# Configure file paths here
LOCAL_FILE_PATH = "Aadhar Sample.jpeg"  # Example local file path
S3_CONFIG = {
    "bucket": os.getenv('S3_BUCKET_NAME'),
    "key": "kyc_documents/user123.jpg"  # Example S3 object key
}

app = FastAPI(title="KYC Document Auto-fill API",
             description="API to process KYC documents using OCR and Groq LLM")

# Initialize S3 client only if using S3
s3_client = None
if STORAGE_TYPE == StorageType.S3:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )

class KYCRequest(BaseModel):
    userId: str

def get_local_file() -> dict:
    """Get file from specified local path"""
    try:
        with open(LOCAL_FILE_PATH, 'rb') as f:
            return {'document': io.BytesIO(f.read())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

def get_s3_file() -> dict:
    """Get file from specified S3 path"""
    if not s3_client:
        raise HTTPException(status_code=500, detail="S3 client not initialized")
    
    try:
        response = s3_client.get_object(
            Bucket=S3_CONFIG["bucket"],
            Key=S3_CONFIG["key"]
        )
        return {'document': io.BytesIO(response['Body'].read())}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/fill-kyc-json")
async def fill_kyc_json(request: KYCRequest):
    """
    Process single KYC document and fill JSON schema using OCR and Groq LLM
    """
    try:
        # Get file based on storage type
        if STORAGE_TYPE == StorageType.S3:
            uploaded_files = get_s3_file()
        else:
            uploaded_files = get_local_file()
        
        if not uploaded_files:
            raise HTTPException(status_code=404, detail="Could not read document")
        
        # Process document using the existing agent
        result = parse_kyc_documents(uploaded_files)
        
        # Parse the JSON string returned by the agent
        try:
            json_result = json.loads(result)
            return json_result
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Error parsing JSON response from agent")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"} 
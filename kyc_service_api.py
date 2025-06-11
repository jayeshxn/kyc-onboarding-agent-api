from fastapi import FastAPI, HTTPException
from typing import Dict
import boto3
from botocore.exceptions import ClientError
import os
from pydantic import BaseModel
from dotenv import load_dotenv
import json
from agent import parse_kyc_documents
import io
from pathlib import Path
from enum import Enum
from lab import get_s3_file

load_dotenv()

LOCAL_FILE_PATH = "kyc.img"

# Ensure KYC_Images directory exists
os.makedirs("KYC_Images", exist_ok=True)

S3_CONFIG = {
    "bucket": os.getenv('S3_BUCKET_NAME'),
    "key_prefix": "kyc_documents/"  # Prefix for S3 objects
}

app = FastAPI(title="KYC Document Processing API",
             description="API to process KYC documents using OCR and LLM")

s3_client = None
s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )

class KYCResponse(BaseModel):
    documentType: str
    documentId: str
    fullName: str
    dateOfBirth: str
    gender: str
    address: str

def get_local_file() -> dict:
    """Get file from specified local path"""
    try:
        with open(LOCAL_FILE_PATH, 'rb') as f:
            return {'document': io.BytesIO(f.read())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

# def get_s3_file(userId: str):
#     """Get file from specified S3 path"""
#     if not s3_client:
#         raise HTTPException(status_code=500, detail="S3 client not initialized")
    
#     try:
#         print("Downloading file from S3")
#         s3_client.download_file("dtcchakathon", userId+"/kyc.img", "kyc.img")
#         print("File downloaded")
        
#     except ClientError as e:
#         raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/ocr-service/process/{userId}", response_model=KYCResponse)
async def process_document(userId: str):
    """
    Process single KYC document and fill JSON schema using OCR and Groq LLM
    """
    try:
        print("User ID", userId)
        get_s3_file(userId)
        print("File downloaded")
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
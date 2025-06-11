from fastapi import FastAPI, HTTPException
from typing import Dict
import boto3
from botocore.exceptions import ClientError
import os
from pydantic import BaseModel
from dotenv import load_dotenv
from agent import parse_kyc_documents
from pathlib import Path
from enum import Enum

load_dotenv()

s3_client = None
s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )

def get_s3_file(userId: str) -> dict:
    """Get file from specified S3 path"""
    if not s3_client:
        raise HTTPException(status_code=500, detail="S3 client not initialized")
    
    try:
        s3_client.download_file("dtcchakathon", userId+"/kyc.img", "kyc.img")
        
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))

# print(get_s3_file("919930866565"))
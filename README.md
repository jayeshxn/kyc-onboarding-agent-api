# KYC Document Processing API

A FastAPI-based service that processes KYC documents (currently supporting Aadhar cards) using OCR and LLM to extract structured information.

## Features

- OCR processing using Tesseract
- LLM-based information extraction using Groq
- Support for both local files and S3 storage
- Structured JSON output following a defined schema
- FastAPI-based REST API

## Prerequisites

- Python 3.8+
- Tesseract OCR
- Groq API key
- (Optional) AWS credentials for S3 storage

### Installing Tesseract

#### macOS
```bash
brew install tesseract
```

#### Ubuntu/Debian
```bash
sudo apt-get install tesseract-ocr
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/kyc-processing-api.git
cd kyc-processing-api
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```
GROQ_API_KEY=your_groq_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key  # Optional for S3
AWS_SECRET_ACCESS_KEY=your_aws_secret_key  # Optional for S3
AWS_REGION=your_aws_region  # Optional for S3
S3_BUCKET_NAME=your_bucket_name  # Optional for S3
```

## Configuration

Edit `kyc_service_api.py` to configure storage type and file paths:

```python
# Set storage type (S3 or LOCAL)
STORAGE_TYPE = StorageType.LOCAL

# Configure file paths
LOCAL_FILE_PATH = "path/to/your/file.jpg"  # For local storage
S3_CONFIG = {
    "bucket": os.getenv('S3_BUCKET_NAME'),
    "key": "path/to/your/file.jpg"  # For S3 storage
}
```

## Usage

1. Start the API server:
```bash
uvicorn kyc_service_api:app --reload
```

2. Make a request:
```bash
curl -X POST "http://localhost:8000/fill-kyc-json" \
     -H "Content-Type: application/json" \
     -d '{"userId": "USR-123"}'
```

## API Endpoints

### POST /fill-kyc-json

Process a KYC document and extract information.

Request body:
```json
{
    "userId": "string"
}
```

Response:
```json
{
    "documentType": "AADHAR",
    "documentId": "123456789012",
    "fullName": "John Doe",
    "dateOfBirth": "01/01/1990",
    "gender": "MALE",
    "address": "123 Main Street, City Name, State, PIN Code"
}
```

### GET /health

Health check endpoint.

## Project Structure

```
.
├── README.md
├── requirements.txt
├── kyc_service_api.py    # Main FastAPI application
├── ocr.py               # OCR processing module
├── agent.py            # LLM processing module
├── prompt_template.py  # LLM prompt templates
└── kyc_schema.json    # JSON schema definition
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

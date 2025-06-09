from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json
from ocr import extract_text_from_image
from prompt_template import SYSTEM_PROMPT
import os
from dotenv import load_dotenv

load_dotenv()

def load_schema():
    """Load the KYC schema from JSON file"""
    with open('kyc_schema.json', 'r') as f:
        return json.load(f)

# Initialize the JSON parser with schema
parser = JsonOutputParser(pydantic_object=load_schema())

# Create the prompt template using external prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "Please extract the KYC information from the provided text.")
])

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY")
)

chain = prompt | llm | parser

def parse_kyc_documents(uploaded_files: dict) -> dict:
    """Process multiple documents and combine their information"""
    combined_text = ""
    
    for doc_type, file in uploaded_files.items():
        extracted_text = extract_text_from_image(file)
        combined_text += f"\n=== {doc_type.upper()} DOCUMENT ===\n{extracted_text}\n"
    
    try:
        result = chain.invoke({
            "text": combined_text
        })
        return json.dumps(result, indent=2)
    except Exception as e:
        print(f"Error processing documents: {str(e)}")
        return json.dumps({
            "error": "Failed to process documents",
            "details": str(e)
        }, indent=2)

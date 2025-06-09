import pytesseract
from PIL import Image
import io

def extract_text_from_image(uploaded_file):
    """
    Extract text from an image using Tesseract OCR.
    Supports both image files and file-like objects.
    """
    try:
        # If uploaded_file is a file-like object (BytesIO), use it directly
        if isinstance(uploaded_file, io.BytesIO):
            image = Image.open(uploaded_file)
        else:
            # If it's a file path, open it
            image = Image.open(uploaded_file)
        
        # Convert image to RGB if it's not
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Extract text using Tesseract
        text = pytesseract.image_to_string(
            image,
            lang='eng',
            config='--psm 3'  # Page segmentation mode: Fully automatic page segmentation
        )
        
        return text.strip()
        
    except Exception as e:
        print(f"Error in OCR processing: {str(e)}")
        return ""
    finally:
        if 'image' in locals():
            image.close()
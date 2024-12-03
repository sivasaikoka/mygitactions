import easyocr
from PIL import Image

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])  # Specify languages (e.g., 'en' for English)

def ocr_image_to_text(image_path):
    with Image.open(image_path) as img:
        result = reader.readtext(img)

    # Extract text from result
    text = ' '.join([entry[1] for entry in result])
    return text
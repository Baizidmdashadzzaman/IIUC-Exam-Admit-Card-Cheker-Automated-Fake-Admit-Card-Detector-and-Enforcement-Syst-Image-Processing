import cv2
import pytesseract
import re

def extract_id_no(image_path):
    # Step 1: Read and preprocess image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Step 2: OCR
    custom_config = r'--psm 6'
    text = pytesseract.image_to_string(thresh, config=custom_config)

    # Debug: Print raw text to inspect
    # print(text)

    # Step 3: Search for ID-like patterns
    lines = text.split('\n')
    for line in lines:
        if 'ID' in line and 'No' in line:
            match = re.search(r'ID\s*No\.?\s*:?[\s]*([A-Z0-9]{6,})', line)
            if match:
                return match.group(1)

    return "ID No not found"

# Example usage
id_no = extract_id_no("image.png")
print("Extracted ID No:", id_no)

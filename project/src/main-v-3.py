import cv2
import pytesseract
import re

def extract_student_info(image_path):
    # Step 1: Read and preprocess image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Step 2: OCR
    custom_config = r'--psm 6'
    text = pytesseract.image_to_string(thresh, config=custom_config)

    # Step 3: Initialize data
    id_no = None
    semester = None
    name = None

    lines = text.split('\n')
    for line in lines:
        # ID No
        if 'ID' in line and 'No' in line and not id_no:
            match = re.search(r'ID\s*No\.?\s*:?[\s]*([A-Z0-9]{6,})', line)
            if match:
                id_no = match.group(1)

        # Semester / Session
        if 'Session' in line and not semester:
            match = re.search(r'Session\s*:?[\s]*(Spring|Fall|Summer)-?\s*(\d{4})', line, re.IGNORECASE)
            if match:
                semester = f"{match.group(1).capitalize()}-{match.group(2)}"

        # Name (clean up extra parts like "CSE-xxxx")
        if 'Name' in line and not name:
            match = re.search(r'Name\s*:?[\s]*([A-Z\s\-]+)', line)
            if match:
                raw_name = match.group(1).strip()
                # Stop at first word like 'CSE-' if present
                name = re.split(r'\bCSE\b|\bEEE\b|\bENG\b|\bPHY\b|\bMAT\b', raw_name)[0].strip()

    return {
        'ID No': id_no or "Not found",
        'Semester': semester or "Not found",
        'Name': name or "Not found"
    }

# Example usage
info = extract_student_info("image.png")
print("✅ Extracted Student Info:")
for key, value in info.items():
    print(f"{key}: {value}")

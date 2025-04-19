import cv2
import pytesseract
import re


def extract_admit_card_data(image_path):
    # Load image
    image = cv2.imread(image_path)

    # Resize for better accuracy (optional)
    image = cv2.resize(image, None, fx=1.5, fy=1.5)

    # Convert to gray and apply threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Run OCR
    custom_config = r'--psm 6'
    full_text = pytesseract.image_to_string(thresh, config=custom_config)

    # Debug: Print raw text
    # print(full_text)

    # === PERSONAL INFO EXTRACTION ===
    def extract_field(label, text, fallback=None):
        match = re.search(rf'{label}\s*:\s*(.*)', text)
        return match.group(1).split('\n')[0].strip() if match else fallback

    personal_info = {
        'Session': extract_field('Session', full_text),
        'ID No': extract_field('ID No', full_text),
        'Registration No': extract_field('Registration No', full_text),
        'Name': extract_field('Name', full_text),
        "Father's Name": extract_field("Father's Name", full_text),
        "Mother's Name": extract_field("Mother's Name", full_text),
        'Section': extract_field('Section', full_text),
        'Program': extract_field('Program', full_text),
        'Validity': extract_field('Validity', full_text),
        'Print Date': extract_field('Print Date', full_text),
    }

    # === COURSE EXTRACTION ===
    course_pattern = re.compile(r'(MGT|CSE)-\d{4}\s+([A-Za-z /,]+.*?)\s+(\d)')
    course_matches = course_pattern.findall(full_text)

    course_list = []
    for code_prefix, title, credit in course_matches:
        course_code_match = re.search(rf'({code_prefix}-\d{{4}})', f"{code_prefix}-{title}")
        course_code = course_code_match.group(1) if course_code_match else f"{code_prefix}-XXXX"
        clean_title = title.replace(course_code, '').strip()
        course_list.append({
            'Course Code': course_code,
            'Course Title': clean_title,
            'Credit Hours': int(credit)
        })

    return {
        'Personal Info': personal_info,
        'Courses': course_list
    }


# Example usage
if __name__ == "__main__":
    data = extract_admit_card_data("image.png")

    print("✅ Personal Information:")
    for key, value in data['Personal Info'].items():
        print(f"{key}: {value}")

    print("\n📚 Registered Courses:")
    for course in data['Courses']:
        print(course)

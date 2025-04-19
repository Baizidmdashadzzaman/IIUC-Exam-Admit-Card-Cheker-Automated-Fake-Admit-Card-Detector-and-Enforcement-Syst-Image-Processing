import re
import pandas as pd
from typing import Dict, List, Any

FIELD_PATTERNS = {
    "session":    r"Session\s*:\s*(Spring|Summer|Fall)-\d{4}",
    "id_no":      r"ID No\.?\s*:\s*([A-Z0-9]+)",
    "reg_no":     r"Registration No\.?\s*:\s*(\d+)",
    "name":       r"Name\s*:\s*([A-Z\s]+)",
    "father":     r"Father'?s Name\s*:\s*([A-Z\s]+)",
    "mother":     r"Mother'?s Name\s*:\s*([A-Z\s]+)",
    "section":    r"Section\s*:\s*(\w+)",
    "program":    r"Program\s*:\s*(.+)",
    "print_date": r"Print Date\s*:\s*(\d{4}-\d{2}-\d{2})",
    "semester":   r"Semester Enrolled\s*:\s*(\d+)",
}

# Match course line like: "CSE-4743  Computer Security  2"
COURSE_LINE = re.compile(r"([A-Z]{3}-\d{4})\s+(.+?)\s+(\d+)$")

def parse_fields(text: str) -> Dict[str, Any]:
    data: Dict[str, Any] = {}

    # Extract main fields using regex
    for key, pat in FIELD_PATTERNS.items():
        match = re.search(pat, text, re.IGNORECASE)
        data[key] = match.group(1).strip() if match else None

    # Clean long name lines that may contain course names
    if data.get("name") and "CSE-" in data["name"]:
        data["name"] = data["name"].split("CSE-")[0].strip()

    if data.get("father") and "CSE-" in data["father"]:
        data["father"] = data["father"].split("CSE-")[0].strip()

    if data.get("mother") and "CSE-" in data["mother"]:
        data["mother"] = data["mother"].split("CSE-")[0].strip()

    data["courses"] = parse_courses(text)
    return data

def parse_courses(text: str) -> List[Dict[str, Any]]:
    lines = text.splitlines()
    courses = []
    for ln in lines:
        ln = ln.strip()
        match = COURSE_LINE.search(ln)
        if match:
            courses.append({
                "code": match.group(1),
                "title": match.group(2).strip(),
                "credit": int(match.group(3))
            })
    return courses

def courses_to_df(courses: List[Dict[str, Any]]) -> pd.DataFrame:
    return pd.DataFrame(courses)

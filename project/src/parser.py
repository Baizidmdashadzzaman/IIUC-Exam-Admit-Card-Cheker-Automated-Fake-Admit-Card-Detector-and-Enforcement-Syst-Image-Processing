import re
import pandas as pd
from typing import Dict, List, Any

FIELD_PATTERNS = {
    "session":    r"Session\s*:\s*(.+)",
    "id_no":      r"ID No\.?\s*:\s*([A-Z0-9]+)",
    "reg_no":     r"Registration No\.?\s*:\s*([0-9]+)",
    "name":       r"Name\s*:\s*(.+)",
    "father":     r"Father's Name\s*:\s*(.+)",
    "mother":     r"Mother's Name\s*:\s*(.+)",
    "section":    r"Section\s*:\s*(.+)",
    "program":    r"Program\s*:\s*(.+)",
    "print_date": r"Print Date\s*:\s*(\d{4}-\d{2}-\d{2})",
    "semester":   r"Semester Enrolled\s*:\s*(\d+)",
}

COURSE_LINE = re.compile(r"([A-Z]{3}-\d{4})\s+(.+?)\s+(\d+)$")

def parse_fields(text: str) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    for key, pat in FIELD_PATTERNS.items():
        m = re.search(pat, text)
        data[key] = m.group(1).strip() if m else None
    data["courses"] = parse_courses(text)
    return data

def parse_courses(text: str) -> List[Dict[str, Any]]:
    lines = text.splitlines()
    courses = []
    for ln in lines:
        m = COURSE_LINE.search(ln)
        if m:
            courses.append({
                "code":   m.group(1),
                "title":  m.group(2).strip(),
                "credit": int(m.group(3))
            })
    return courses

def courses_to_df(courses: List[Dict[str,Any]]) -> pd.DataFrame:
    return pd.DataFrame(courses)

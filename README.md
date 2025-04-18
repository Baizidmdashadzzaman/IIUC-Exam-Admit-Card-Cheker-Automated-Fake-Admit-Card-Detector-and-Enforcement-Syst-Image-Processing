Project Title:
IIUC-Exam-Admit-Card-Cheker : Automated Fake Admit Card Detector & Enforcement System Using Image Processing

Detailed Description:

IIUC-AdmitSentry is a specialized security system designed for the International Islamic University Chittagong (IIUC) that leverages advanced image processing and machine learning techniques to validate exam admit cards. Its primary objective is to detect counterfeit or tampered admit cards and enforce strict disciplinary measures, including automatic expulsion procedures for students found using fake documents. Below are the key aspects and functionalities of the project:

Advanced Image Processing:
Utilizes libraries such as OpenCV to analyze scanned images of admit cards. The system performs tasks like edge detection, pattern matching, and watermark recognition to verify the authenticity of the card’s features.

Machine Learning Integration:
Incorporates pre-trained machine learning models to learn and recognize standard security markers and layout patterns typical to genuine IIUC admit cards. Any deviations or anomalies are flagged for further review.

Automated Validation Pipeline:
Implements a multi-stage verification process where an uploaded admit card is subjected to several layers of analysis—from text verification (e.g., comparing printed names and IDs) to image quality and document integrity checks.

Alert & Enforcement Mechanism:
On detection of a fake or tampered admit card, the system triggers an immediate alert to the examination board. The automated process facilitates rapid decision-making, potentially leading to immediate student expulsion in accordance with university policies.

User-Friendly Dashboard:
Provides an intuitive interface for exam invigilators and administrative staff to review flagged cases. Detailed logs and reports allow for transparency and facilitate further investigation if needed.

Secure & Scalable Design:
Engineered to integrate seamlessly within the IIUC exam management systems, ensuring data security and easy scalability. The system can be updated to incorporate new security features as document standards evolve.


# Setup
python -m venv venv
source venv/Scripts/activate



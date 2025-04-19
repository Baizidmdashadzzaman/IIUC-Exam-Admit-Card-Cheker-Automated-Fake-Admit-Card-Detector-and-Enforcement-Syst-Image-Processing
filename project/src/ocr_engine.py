from PIL import Image
import pytesseract
import numpy as np

def image_to_text(img_array: np.ndarray) -> str:
    # convert OpenCV image back to PIL
    pil = Image.fromarray(img_array)
    # configure language if you need Bangla/English
    config = "--psm 6"
    return pytesseract.image_to_string(pil, config=config)

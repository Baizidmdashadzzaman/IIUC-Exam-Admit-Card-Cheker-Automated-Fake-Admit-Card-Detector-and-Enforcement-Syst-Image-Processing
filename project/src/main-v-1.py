import json
import os
from preprocessing import preprocess
from ocr_engine import image_to_text
from parser import parse_fields, courses_to_df

def run(image_path: str, json_out: str = None, csv_out: str = None):
    # Ensure the image exists
    if not os.path.isfile(image_path):
        print(f"[✘] Image file not found: {image_path}")
        return

    # Preprocess and OCR
    img = preprocess(image_path)
    raw = image_to_text(img)

    # --- DEBUG: dump raw OCR output ---
    print("\n----- RAW OCR OUTPUT -----\n")
    print(raw)
    print("\n----- END OF RAW OUTPUT -----\n")

    # Parse fields and courses
    data = parse_fields(raw)

    # Display parsed JSON
    print("\n[✔] Parsed Data:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    # Optionally save courses to CSV
    if csv_out:
        df = courses_to_df(data.get("courses", []))
        df.to_csv(csv_out, index=False)
        print(f"[✔] Saved courses CSV to {csv_out}")

    # Optionally save full JSON
    if json_out:
        with open(json_out, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[✔] Saved JSON to {json_out}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract admit card data from image")
    parser.add_argument("image", help="Path to the admit card image")
    parser.add_argument("--json", help="Output JSON file path")
    parser.add_argument("--csv", help="Output courses CSV file path")
    args = parser.parse_args()
    run(args.image, args.json, args.csv)

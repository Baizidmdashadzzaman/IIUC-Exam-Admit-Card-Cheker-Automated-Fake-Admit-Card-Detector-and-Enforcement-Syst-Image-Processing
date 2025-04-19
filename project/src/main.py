import json
from preprocessing import preprocess
from ocr_engine import image_to_text
from parser import parse_fields, courses_to_df
import os

def run(image_path: str, json_out: str = None, csv_out: str = None):
    # image_path = "image.jpg"

    if not os.path.isfile(image_path):
        print(f"[✘] Image file not found: {image_path}")
        return

    img = preprocess(image_path)
    raw = image_to_text(img)
    data = parse_fields(raw)

    # Print JSON
    print(json.dumps(data, indent=2))

    # Optionally save courses to CSV
    if csv_out:
        df = courses_to_df(data["courses"])
        df.to_csv(csv_out, index=False)
    # Optionally save full JSON
    if json_out:
        with open(json_out, "w") as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("image")
    p.add_argument("--json", help="output JSON file")
    p.add_argument("--csv",  help="output courses CSV")
    args = p.parse_args()
    run(args.image, args.json, args.csv)

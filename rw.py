import fitz  # PyMuPDF
import re
import csv
from typing import List, Dict

def extract_fields_from_text(text: str, channel: str = "RWS") -> List[Dict[str, str]]:
    lines = text.split('\n')
    data = []
    current_pcd = None

    for line in lines:
        # Detect section headers like "R0805 OS"
        match = re.match(r'^(R\d{4})\s+OS\b', line.strip())
        if match:
            current_pcd = match.group(1)
            continue

        # Skip known headers and empty lines
        if any(keyword in line for keyword in ["Field", "Format", "Action", "----", "PAS"]):
            continue
        if not line.strip():
            continue

        # Attempt to split the line into parts
        parts = re.split(r'\s{2,}|\t+', line.strip())
        if len(parts) >= 2:
            field_name = parts[0].strip()
            description = parts[2].strip() if len(parts) > 2 else ""
            if current_pcd:
                data.append({
                    "Field Name": field_name,
                    "Description": description,
                    "PCD Number": current_pcd,
                    "Channel": channel
                })

    return data

def extract_from_pdf(pdf_path: str, channel: str = "RWS") -> List[Dict[str, str]]:
    final_data = []
    doc = fitz.open(pdf_path)
    for page in doc:
        text = page.get_text()
        page_data = extract_fields_from_text(text, channel=channel)
        final_data.extend(page_data)
    return final_data

def write_to_csv(data: List[Dict[str, str]], output_csv_path: str):
    if not data:
        print("No data to write.")
        return

    fieldnames = ["Field Name", "Description", "PCD Number", "Channel"]
    with open(output_csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"CSV written to {output_csv_path}")

# Example usage
if __name__ == "__main__":
    pdf_file_path = "/mnt/data/RWS.pdf"  # Replace this with your actual PDF file path
    output_csv_path = "/mnt/data/pcd_fields_output.csv"

    extracted_data = extract_from_pdf(pdf_file_path)
    write_to_csv(extracted_data, output_csv_path)

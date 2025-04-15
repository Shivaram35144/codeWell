import fitz  # PyMuPDF
import csv
import re
from typing import List, Dict

def extract_aps_sections(text: str, channel: str = "APS") -> List[Dict[str, str]]:
    data = []
    current_pcd = None

    # Find COPYBOOK blocks ending in _OS
    pattern = re.compile(r'(COPYBOOK:\s+(\w+_OS)[\s\S]+?END OF DATA STRUCTURE)', re.MULTILINE)
    matches = pattern.findall(text)

    for match in matches:
        full_block, pcd = match
        current_pcd = pcd.strip()

        for line in full_block.split('\n'):
            if "FILLER" in line or not line.strip():
                continue

            # Attempt to extract field name
            line_parts = re.split(r'\s{2,}|\t+', line.strip())
            if len(line_parts) >= 2:
                field_name = line_parts[1].strip() if line_parts[0].isdigit() else line_parts[0].strip()
                data.append({
                    "Field Name": field_name,
                    "Description": "",  # Description not available
                    "PCD Number": current_pcd,
                    "Channel": channel
                })

    return data

def extract_from_pdf_aps(pdf_path: str, channel: str = "APS") -> List[Dict[str, str]]:
    final_data = []
    doc = fitz.open(pdf_path)
    for page in doc:
        text = page.get_text()
        final_data.extend(extract_aps_sections(text, channel))
    return final_data

def write_to_csv(data: List[Dict[str, str]], output_csv_path: str):
    if not data:
        print("No data extracted.")
        return

    fieldnames = ["Field Name", "Description", "PCD Number", "Channel"]
    with open(output_csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"CSV saved to {output_csv_path}")

# Example usage
if __name__ == "__main__":
    pdf_path = "/mnt/data/APS.pdf"  # Use your actual file path
    output_csv_path = "/mnt/data/aps_fields_output.csv"

    extracted_data = extract_from_pdf_aps(pdf_path)
    write_to_csv(extracted_data, output_csv_path)

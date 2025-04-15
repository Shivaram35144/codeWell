import fitz  # PyMuPDF
import csv
import re
from typing import List, Dict

pcd_list = [
    "1600", "1607", "1616", "1619", "1623", "1663", "1664", "1665",
    "1676", "1678", "1691", "13197", "98084", "75420240", "75422800",
    "75426601", "75500100", "75501001", "75640855", "5501"
]
# Convert to padded strings for matching
pcd_str_list = [f"P{p}_OS" for p in pcd_list]

def extract_matching_copybooks(text: str, channel: str = "APS") -> List[Dict[str, str]]:
    data = []
    pattern = re.compile(r'(COPYBOOK:\s+(P\d+_OS)[\s\S]+?END OF DATA STRUCTURE)', re.MULTILINE)
    matches = pattern.findall(text)

    for block, pcd in matches:
        if pcd not in pcd_str_list:
            continue

        for line in block.split('\n'):
            if "FILLER" in line or not line.strip():
                continue

            # Try to extract the field name
            line_parts = re.split(r'\s{2,}|\t+', line.strip())
            if len(line_parts) >= 2:
                field_name = line_parts[1].strip() if line_parts[0].isdigit() else line_parts[0].strip()
                data.append({
                    "Field Name": field_name,
                    "Description": "",
                    "PCD Number": pcd,
                    "Channel": channel
                })

    return data

def extract_from_pdf_aps_filtered(pdf_path: str, channel: str = "APS") -> List[Dict[str, str]]:
    final_data = []
    doc = fitz.open(pdf_path)
    for page in doc:
        text = page.get_text()
        final_data.extend(extract_matching_copybooks(text, channel))
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

    print(f"Filtered CSV saved to {output_csv_path}")

# Example usage
if __name__ == "__main__":
    pdf_path = "/mnt/data/APS.pdf"  # Update this path with your full APS PDF path
    output_csv_path = "/mnt/data/aps_filtered_pcds.csv"

    filtered_data = extract_from_pdf_aps_filtered(pdf_path)
    write_to_csv(filtered_data, output_csv_path)

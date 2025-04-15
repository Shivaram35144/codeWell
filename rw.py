import fitz  # PyMuPDF
import re

def extract_data_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    results = []
    current_pcd = None

    pcd_pattern = re.compile(r'R\d{4}\s+OS\s+\(PCD\s+(\d+)\s+Output\)', re.IGNORECASE)

    for page in doc:
        text = page.get_text("text")
        lines = text.split('\n')

        for line in lines:
            # Check if this line is a PCD section header
            pcd_match = pcd_pattern.search(line)
            if pcd_match:
                current_pcd = 'R' + pcd_match.group(1)
                continue

            # Ignore lines if no PCD section has started
            if not current_pcd:
                continue

            # Try splitting each line assuming 3-column structure
            parts = re.split(r'\s{2,}', line.strip())
            if len(parts) >= 2:
                field_name = parts[0].strip()
                format_part = parts[1].strip()
                action = parts[2].strip() if len(parts) > 2 else ""

                results.append({
                    "Field Name": field_name,
                    "Description": action,
                    "PCD Number": current_pcd,
                    "Channel": "RWS"
                })

    return results

# Save result as a CSV or print
import csv

output = extract_data_from_pdf("path/to/RWS.pdf")  # Replace with your actual PDF path
with open("rws_output.csv", "w", newline='') as csvfile:
    fieldnames = ["Field Name", "Description", "PCD Number", "Channel"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output)

print("Extraction completed and saved as rws_output.csv.")

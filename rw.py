import fitz  # PyMuPDF
import re
import csv

def extract_table_data_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    results = []

    # Match lines like: R1600_OS – PCD 1600 Output
    pcd_header_pattern = re.compile(r'^(R\d{4})_OS\s+–\s+PCD\s+\d+\s+Output$', re.IGNORECASE)

    current_pcd = None
    for page in doc:
        lines = page.get_text("text").split('\n')

        for i, line in enumerate(lines):
            line = line.strip()

            # Match and store current PCD from header line
            match = pcd_header_pattern.match(line)
            if match:
                current_pcd = match.group(1)
                continue

            # Only extract table rows after a PCD section has started
            if not current_pcd:
                continue

            # Skip empty lines and lines too short
            if len(line.strip()) == 0 or line.startswith('Format'):
                continue

            # Extract fields assuming tabular format split by double or more spaces
            parts = re.split(r'\s{2,}', line.strip())

            if len(parts) >= 2:
                field_name = parts[0].strip()
                description = parts[2].strip() if len(parts) >= 3 else ""

                results.append({
                    "Field Name": field_name,
                    "Description": description,
                    "PCD Number": current_pcd,
                    "Channel": "RWS"
                })

    return results

# Save results to CSV
def save_to_csv(data, output_file='rws_output.csv'):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Field Name", "Description", "PCD Number", "Channel"])
        writer.writeheader()
        writer.writerows(data)
    print(f"Saved {len(data)} rows to {output_file}")

# Example usage
pdf_path = "path/to/your/RWS.pdf"  # Replace with your actual PDF path
output_data = extract_table_data_from_pdf(pdf_path)
save_to_csv(output_data)

import fitz  # PyMuPDF
import re
import csv

# Step 1: Extract full text
def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text("text")
    return full_text

# Step 2: Split PCD sections
def split_pcds(text):
    pattern = r'(R\d{4}_OS\s+–\s+PCD\s+\d+\s+Output)'  # Matches PCD Headers
    parts = re.split(pattern, text)
    grouped = []

    for i in range(1, len(parts), 2):
        header = parts[i].strip()
        content = parts[i+1].strip()
        grouped.append((header, content))
    return grouped

# Step 3: Parse tables under each PCD
def extract_table_data(grouped_sections):
    results = []

    for header, content in grouped_sections:
        pcd_match = re.match(r'(R\d{4})_OS', header)
        if not pcd_match:
            continue
        pcd_number = pcd_match.group(1)

        lines = content.split('\n')
        for line in lines:
            if line.strip() == "":
                continue
            # Ignore column headers like "PAS Segment & Field    Format    Action"
            if "PAS Segment" in line and "Format" in line:
                continue

            # Split line based on 2 or more spaces
            parts = re.split(r'\s{2,}', line.strip())

            if len(parts) >= 1:
                field_name = parts[0]
                description = parts[2] if len(parts) >= 3 else ""

                results.append({
                    "Field Name": field_name,
                    "Description": description,
                    "PCD Number": pcd_number,
                    "Channel": "RWS"
                })

    return results

# Step 4: Save to CSV
def save_to_csv(data, output_file='rws_output.csv'):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Field Name", "Description", "PCD Number", "Channel"])
        writer.writeheader()
        writer.writerows(data)
    print(f"Saved {len(data)} rows to {output_file}")

# Main function
def process_pdf(pdf_path):
    text = extract_pdf_text(pdf_path)
    grouped_sections = split_pcds(text)
    data = extract_table_data(grouped_sections)
    save_to_csv(data)

# === RUN HERE ===
pdf_path = "RWS.pdf"  # Replace with your actual path
process_pdf(pdf_path)

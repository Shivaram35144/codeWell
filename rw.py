import fitz  # PyMuPDF
import re
import csv

def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text("text")
    return full_text

def split_pcds(text):
    # Updated to match both "R0085 OS – PCD 75420085 Output" or "R1602 OS – PCD 1602 Output"
    pattern = r'(R\d{4})[ _-]OS\s+[–-]\s+PCD\s+\d+\s+Output'
    matches = list(re.finditer(pattern, text))
    
    grouped = []
    for i, match in enumerate(matches):
        pcd_number = match.group(1)
        start = match.end()
        end = matches[i+1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        grouped.append((pcd_number, content))
    return grouped

def extract_table_data(grouped_sections):
    results = []
    for pcd_number, content in grouped_sections:
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # Skip headers and dividers
            if 'PAS Segment' in line and 'Format' in line and 'Action' in line:
                continue
            if re.match(r'^\s*[-_]+$', line):  # horizontal lines
                continue
            if re.match(r'^R\d{4}.*Output', line):  # black line titles
                continue

            # Split by 2+ spaces (aligns with visual table columns)
            parts = re.split(r'\s{2,}', line)
            if len(parts) >= 1:
                field_name = parts[0].strip()
                description = parts[2].strip() if len(parts) >= 3 else ""
                results.append({
                    "Field Name": field_name,
                    "Description": description,
                    "PCD Number": pcd_number,
                    "Channel": "RWS"
                })
    return results

def save_to_csv(data, output_file='rws_output.csv'):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Field Name", "Description", "PCD Number", "Channel"])
        writer.writeheader()
        writer.writerows(data)
    print(f"Saved {len(data)} rows to {output_file}")

def process_pdf(pdf_path):
    text = extract_pdf_text(pdf_path)
    grouped_sections = split_pcds(text)
    data = extract_table_data(grouped_sections)
    save_to_csv(data)

# === RUN THIS ===
pdf_path = "RWS.pdf"  # Make sure this is the correct path
process_pdf(pdf_path)

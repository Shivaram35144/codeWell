import json
import xmltodict

# --- Read the JSON file ---
with open("data.json", "r") as f:
    json_data = json.load(f)

# --- Wrap the entire JSON into SOAP body ---
soap_body = {}

for key, value in json_data.items():
    # Prefix each top-level key with namespace (optional)
    soap_body["ex:" + key] = value

soap_dict = {
    "soapenv:Envelope": {
        "@xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
        "@xmlns:ex": "http://example.com/employee",
        "soapenv:Header": None,
        "soapenv:Body": soap_body
    }
}

# --- Convert to XML ---
soap_xml = xmltodict.unparse(soap_dict, pretty=True)

# --- Write to file ---
with open("output.xml", "w") as f:
    f.write(soap_xml)

print("✅ Full JSON converted to SOAP XML → output.xml")

import json
import xmltodict

# --- Read the JSON file ---
with open("data.json", "r") as f:
    json_data = json.load(f)

# --- Wrap JSON inside SOAP envelope ---
soap_dict = {
    "soapenv:Envelope": {
        "@xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
        "@xmlns:ex": "http://example.com/employee",
        "soapenv:Header": None,
        "soapenv:Body": {
            "ex:" + list(json_data.keys())[0]: json_data[list(json_data.keys())[0]]
        }
    }
}

# --- Convert dict to XML string ---
soap_xml = xmltodict.unparse(soap_dict, pretty=True)

# --- Save to file ---
with open("output.xml", "w") as f:
    f.write(soap_xml)

print("✅ Converted JSON to SOAP XML and saved to output.xml")

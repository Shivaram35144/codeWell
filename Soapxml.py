import xmltodict
import json

soap_xml = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:ex="http://example.com/employee">
   <soapenv:Header/>
   <soapenv:Body>
      <ex:GetEmployeeRequest>
         <ex:EmployeeId>123</ex:EmployeeId>
      </ex:GetEmployeeRequest>
   </soapenv:Body>
</soapenv:Envelope>
"""

# --- Convert SOAP XML to JSON ---
# Parse the XML into a Python dictionary
data_dict = xmltodict.parse(soap_xml)

# Extract only the body content
body = data_dict['soapenv:Envelope']['soapenv:Body']

# Convert that to JSON string
json_data = json.dumps(body, indent=2)
print("SOAP → JSON:")
print(json_data)


# --- Convert JSON back to SOAP XML ---
# Load back from JSON string
body_dict = json.loads(json_data)

# Re-wrap in SOAP envelope
soap_back = {
    "soapenv:Envelope": {
        "@xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
        "@xmlns:ex": "http://example.com/employee",
        "soapenv:Header": None,
        "soapenv:Body": body_dict
    }
}

soap_xml_back = xmltodict.unparse(soap_back, pretty=True)
print("\nJSON → SOAP XML:")
print(soap_xml_back)

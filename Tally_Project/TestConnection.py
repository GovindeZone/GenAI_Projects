import requests
import xml.etree.ElementTree as ET

TALLY_URL = "http://192.168.1.38:9000"

xml = """
<ENVELOPE>
    <HEADER>
        <VERSION>1</VERSION>
        <TALLYREQUEST>Export Data</TALLYREQUEST>
        <TYPE>Collection</TYPE>
        <ID>List of Ledgers</ID>
    </HEADER>
</ENVELOPE>
"""

response = requests.post(TALLY_URL, data=xml)

xml_text = response.text

root = ET.fromstring(xml_text)

for ledger in root.findall(".//LEDGER"):
    print(ledger.get("NAME"))
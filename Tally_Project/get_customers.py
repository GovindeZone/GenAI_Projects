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

print(response.text[:2000])

with open("response.xml", "w", encoding="utf-8") as f:
    f.write(response.text)

print("Saved response.xml")

root = ET.fromstring(response.text)

for ledger in root.findall(".//LEDGER"):
    print("Ledger =", ledger.get("NAME"))

    for child in ledger:
        print(child.tag)

    break
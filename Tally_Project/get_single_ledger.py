import requests

TALLY_URL = "http://localhost:9000"

xml = """
<ENVELOPE>
 <HEADER>
  <TALLYREQUEST>Export Data</TALLYREQUEST>
 </HEADER>
 <BODY>
  <EXPORTDATA>
   <REQUESTDESC>
    <REPORTNAME>Ledger</REPORTNAME>

    <STATICVARIABLES>
      <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
      <LEDGERNAME>Velavan  Steels</LEDGERNAME>
    </STATICVARIABLES>

   </REQUESTDESC>
  </EXPORTDATA>
 </BODY>
</ENVELOPE>
"""

response = requests.post(TALLY_URL, data=xml)

print(response.text)
import requests

TALLY_URL = "http://192.168.1.38:9000"

xml = """
<ENVELOPE>
 <HEADER>
  <TALLYREQUEST>Export Data</TALLYREQUEST>
 </HEADER>

 <BODY>
  <EXPORTDATA>

   <REQUESTDESC>

    <REPORTNAME>Ledger Vouchers</REPORTNAME>

    <STATICVARIABLES>
      <SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
    </STATICVARIABLES>

   </REQUESTDESC>

  </EXPORTDATA>
 </BODY>
</ENVELOPE>
"""

response = requests.post(
    TALLY_URL,
    data=xml
)

print(response.text[:5000])
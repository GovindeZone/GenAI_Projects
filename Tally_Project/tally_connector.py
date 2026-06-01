import requests

class TallyConnector:

    def __init__(self, host):
        self.host = host

    def execute(self, xml_request):

        response = requests.post(
            self.host,
            data=xml_request,
            timeout=60
        )

        response.raise_for_status()

        return response.text
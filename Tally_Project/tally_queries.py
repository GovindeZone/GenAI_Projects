from tally_connector import TallyConnector

connector = TallyConnector(
    "http://192.168.1.38:9000"
)

def get_ledgers():

    xml = """
    YOUR WORKING XML
    """

    return connector.execute(xml)
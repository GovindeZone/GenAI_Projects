import pandas as pd

def load_excel(file):

    invoices = pd.read_excel(file,"Invoices")
    po = pd.read_excel(file,"Purchase_Orders")
    vendors = pd.read_excel(file,"Vendors")
    policies = pd.read_excel(file,"Policies")
    approvals = pd.read_excel(file,"Approvals")

    return invoices,po,vendors,policies,approvals
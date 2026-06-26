import pandas as pd


def get_invoice_details(
    invoice_id,
    invoices,
    po,
    vendors,
    policies,
    approvals
):

    invoice = invoices[
        invoices["Invoice_ID"] == invoice_id
    ]

    if invoice.empty:
        return None

    invoice = invoice.iloc[0]

    po_row = po[
        po["PO_ID"] == invoice["PO_ID"]
    ]

    vendor_row = vendors[
        vendors["Vendor_ID"] == invoice["Vendor_ID"]
    ]

    approval_row = approvals[
        approvals["Invoice_ID"] == invoice_id
    ]

    po_amount = None

    if not po_row.empty:
        po_amount = float(po_row.iloc[0]["PO_Amount"])

    policy_text = ""

    if pd.notna(invoice["Reason_Code"]):

        policy_row = policies[
            policies["Reason_Code"]
            == invoice["Reason_Code"]
        ]

        if not policy_row.empty:
            policy_text = policy_row.iloc[0]["Policy_Rule"]

    evidence = {

        "invoice_id": invoice["Invoice_ID"],
        "vendor_id": invoice["Vendor_ID"],
        "po_id": invoice["PO_ID"],
        "invoice_amount": float(invoice["Invoice_Amount"]),
        "po_amount": po_amount,
        "status": invoice["Status"],
        "reason_code": invoice["Reason_Code"],
        "policy": policy_text

    }

    if not vendor_row.empty:

        evidence["vendor_name"] = vendor_row.iloc[0]["Vendor_Name"]
        evidence["vendor_status"] = vendor_row.iloc[0]["Vendor_Status"]

    if not approval_row.empty:

        evidence["approver"] = approval_row.iloc[0]["Approver"]
        evidence["approval_comment"] = approval_row.iloc[0]["Comments"]

    return evidence
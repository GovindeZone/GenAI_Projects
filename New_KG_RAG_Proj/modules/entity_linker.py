def build_links(
    invoices,
    po,
    vendors,
    policies,
    approvals
):

    links = []

    for _, inv in invoices.iterrows():

        links.append(
            (
                inv["Invoice_ID"],
                "HAS_PO",
                inv["PO_ID"]
            )
        )

        links.append(
            (
                inv["Invoice_ID"],
                "HAS_VENDOR",
                inv["Vendor_ID"]
            )
        )

        if str(inv["Reason_Code"]) != "nan":

            links.append(
                (
                    inv["Invoice_ID"],
                    "REJECTED_BY",
                    inv["Reason_Code"]
                )
            )

    return links
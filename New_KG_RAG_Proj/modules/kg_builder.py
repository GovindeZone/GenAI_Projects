def build_kg(invoices, po, vendors, policies, approvals):

    nodes = []
    edges = []

    for _, row in invoices.iterrows():
        inv = row["Invoice_ID"]
        vendor = row.get("Vendor", "Unknown")

        nodes.append(inv)
        nodes.append(vendor)

        edges.append({"source": inv, "target": vendor})

    return nodes, edges
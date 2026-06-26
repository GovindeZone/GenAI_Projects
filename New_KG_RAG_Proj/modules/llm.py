from groq import Groq


MODEL_NAME = "llama-3.1-8b-instant"


def explain_invoice(evidence, api_key):

    client = Groq(api_key=api_key)

    invoice_id = evidence.get("invoice_id", "")
    vendor_name = evidence.get("vendor_name", "")
    vendor_status = evidence.get("vendor_status", "")
    po_id = evidence.get("po_id", "")
    invoice_amount = evidence.get("invoice_amount", "")
    po_amount = evidence.get("po_amount", "")
    status = evidence.get("status", "")
    reason_code = evidence.get("reason_code", "")
    policy = evidence.get("policy", "")
    approver = evidence.get("approver", "")
    approval_comment = evidence.get("approval_comment", "")

    variance = None

    try:
        if po_amount and invoice_amount:
            variance = float(invoice_amount) - float(po_amount)
    except:
        pass

    prompt = f"""
You are a Senior Accounts Payable Analyst.

Analyze the invoice evidence and provide a professional business explanation.

Invoice Details:

Invoice ID: {invoice_id}
Vendor Name: {vendor_name}
Vendor Status: {vendor_status}

PO ID: {po_id}

Invoice Amount: {invoice_amount}
PO Amount: {po_amount}

Variance: {variance}

Status: {status}

Reason Code: {reason_code}

Policy:
{policy}

Approver:
{approver}

Approval Comment:
{approval_comment}

Instructions:

1. Explain what happened.
2. Explain why the invoice was approved or rejected.
3. Reference the policy if available.
4. Mention any amount variance.
5. Recommend corrective action.
6. Keep answer concise and professional.
7. Use bullet points where appropriate.

Do not invent information.
Use only the supplied evidence.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert Finance, AP, "
                    "Procure-to-Pay and Reconciliation Analyst."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
        max_tokens=1000,
    )

    return response.choices[0].message.content
from mcp.server.fastmcp import FastMCP
import pandas as pd
import os

mcp = FastMCP("Excel Finance Assistant")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE = os.path.join(BASE_DIR, "sample_data", "finance_data.xlsx")


@mcp.tool()
def summarize_excel() -> dict:
    """Summarize finance Excel data."""
    if not os.path.exists(EXCEL_FILE):
        return {"error": f"Excel file not found: {EXCEL_FILE}"}

    df = pd.read_excel(EXCEL_FILE)

    summary = {
        "rows": len(df),
        "columns": list(df.columns),
    }

    if "Revenue" in df.columns:
        summary["total_revenue"] = float(df["Revenue"].sum())

    if "Cost" in df.columns:
        summary["total_cost"] = float(df["Cost"].sum())

    if "Revenue" in df.columns and "Cost" in df.columns:
        revenue = df["Revenue"].sum()
        cost = df["Cost"].sum()
        profit = revenue - cost
        margin = profit / revenue * 100 if revenue else 0

        summary["profit"] = float(profit)
        summary["margin_percent"] = round(float(margin), 2)

    return summary


@mcp.tool()
def read_excel_preview() -> str:
    """Show first 10 rows of finance Excel data."""
    if not os.path.exists(EXCEL_FILE):
        return f"Excel file not found: {EXCEL_FILE}"

    df = pd.read_excel(EXCEL_FILE)
    return df.head(10).to_markdown(index=False)


if __name__ == "__main__":
    mcp.run()
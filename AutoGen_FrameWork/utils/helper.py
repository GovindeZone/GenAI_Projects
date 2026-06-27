import pandas as pd


def dataframe_summary(df: pd.DataFrame) -> str:
    """
    Generate a concise summary of the uploaded dataframe.
    """

    summary = []

    summary.append(f"Rows : {len(df)}")

    summary.append(f"Columns : {len(df.columns)}")

    summary.append(
        f"Column Names : {', '.join(df.columns)}"
    )

    summary.append("\nSample Data:\n")

    #summary.append(df.head(10).to_markdown(index=False))
    summary.append(df.head(10).to_string(index=False))

    return "\n".join(summary)
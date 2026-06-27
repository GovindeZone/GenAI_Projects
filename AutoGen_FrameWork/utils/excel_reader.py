import pandas as pd


def load_excel(uploaded_file):
    """
    Read uploaded Excel file.
    """

    try:

        df = pd.read_excel(uploaded_file)

        return df

    except Exception as e:

        raise Exception(
            f"Unable to read Excel file.\n{e}"
        )

import pandas as pd
from io import BytesIO


def load_data(uploaded_file):
    """
    Load CSV or Excel files into a Pandas DataFrame.
    """

    if uploaded_file is None:
        raise ValueError("No file was uploaded.")

    file_name = uploaded_file.name.lower()

    try:
        if file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        elif file_name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)

        else:
            raise ValueError(
                "Unsupported file format. Please upload CSV or Excel."
            )

        if df.empty:
            raise ValueError("The uploaded file contains no data.")

        return df

    except Exception as error:
        raise ValueError(f"Unable to read the file: {error}")

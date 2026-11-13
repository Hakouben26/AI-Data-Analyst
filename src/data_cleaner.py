
import pandas as pd


def clean_data(
    df,
    missing_strategy="Keep original",
    remove_duplicates=True,
    trim_text=True
):
    """
    Clean a dataset without modifying the original DataFrame.

    Returns:
        cleaned_df: cleaned DataFrame
        report: dictionary containing cleaning statistics
    """

    # Create a copy to preserve original data
    cleaned_df = df.copy()

    # Initial statistics
    initial_rows = len(cleaned_df)
    initial_missing = int(cleaned_df.isnull().sum().sum())
    initial_duplicates = int(cleaned_df.duplicated().sum())

    # ----------------------------------
    # 1. CLEAN TEXT SPACES
    # ----------------------------------

    if trim_text:

        text_columns = cleaned_df.select_dtypes(
            include=["object", "string"]
        ).columns

        for column in text_columns:
            cleaned_df[column] = cleaned_df[column].apply(
                lambda value: value.strip()
                if isinstance(value, str)
                else value
            )

    # ----------------------------------
    # 2. HANDLE MISSING VALUES
    # ----------------------------------

    if missing_strategy == "Drop rows with missing values":

        cleaned_df = cleaned_df.dropna()

    elif missing_strategy == "Fill with median/mode":

        for column in cleaned_df.columns:

            if cleaned_df[column].isnull().sum() == 0:
                continue

            if pd.api.types.is_numeric_dtype(cleaned_df[column]):

                median_value = cleaned_df[column].median()

                if pd.notna(median_value):
                    cleaned_df[column] = cleaned_df[column].fillna(
                        median_value
                    )

            else:

                mode_values = cleaned_df[column].mode(dropna=True)

                if not mode_values.empty:
                    cleaned_df[column] = cleaned_df[column].fillna(
                        mode_values.iloc[0]
                    )

    # ----------------------------------
    # 3. REMOVE DUPLICATES
    # ----------------------------------

    if remove_duplicates:

        cleaned_df = cleaned_df.drop_duplicates()

    # ----------------------------------
    # 4. GENERATE CLEANING REPORT
    # ----------------------------------

    report = {
        "initial_rows": initial_rows,
        "final_rows": len(cleaned_df),
        "removed_rows": initial_rows - len(cleaned_df),
        "initial_missing": initial_missing,
        "remaining_missing": int(
            cleaned_df.isnull().sum().sum()
        ),
        "initial_duplicates": initial_duplicates,
        "remaining_duplicates": int(
            cleaned_df.duplicated().sum()
        )
    }

    return cleaned_df, report

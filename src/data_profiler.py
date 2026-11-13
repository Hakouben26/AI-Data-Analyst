
import pandas as pd


def get_dataset_overview(df):
    """
    Return general information about the dataset.
    """

    overview = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_usage": round(
            df.memory_usage(deep=True).sum() / 1024, 2
        )
    }

    return overview


def get_column_profile(df):
    """
    Analyze each column independently.
    """

    profile = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isnull().sum().values,
        "Missing (%)": (
            df.isnull().mean().values * 100
        ).round(2),
        "Unique Values": df.nunique().values
    })

    return profile


def get_numeric_statistics(df):
    """
    Calculate descriptive statistics for numeric columns.
    """

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        return pd.DataFrame()

    statistics = numeric_df.describe().round(2)

    return statistics


def get_categorical_summary(df):
    """
    Analyze categorical columns.
    """

    categorical_df = df.select_dtypes(
        include=["object", "category"]
    )

    if categorical_df.empty:
        return pd.DataFrame()

    summary = []

    for column in categorical_df.columns:

        summary.append({
            "Column": column,
            "Unique Values": categorical_df[column].nunique(),
            "Most Frequent": (
                categorical_df[column].mode().iloc[0]
                if not categorical_df[column].mode().empty
                else None
            )
        })

    return pd.DataFrame(summary)

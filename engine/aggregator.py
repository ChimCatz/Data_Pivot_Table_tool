import pandas as pd


def build_summary(df, mapping):

    result = {}
    total_rows = len(df)

    for field, col in mapping.items():

        series = (
            df[col]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

        full = (
            series.value_counts()
            .reset_index()
        )

        full.columns = [field, "Count"]

        result[field] = {
            "table": full,
            "total": total_rows
        }

    return result
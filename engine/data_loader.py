import pandas as pd


def load_csv(file_path):

    # 1️⃣ Try normal fast read first (works for Zoho usually)
    try:
        df = pd.read_csv(
            file_path,
            encoding="utf-8",
            low_memory=False,
            on_bad_lines="skip"
        )
        return clean_headers(df)
    except Exception:
        pass

    # 2️⃣ Try latin encoding fallback
    try:
        df = pd.read_csv(
            file_path,
            encoding="latin1",
            low_memory=False,
            on_bad_lines="skip"
        )
        return clean_headers(df)
    except Exception:
        pass

    # 3️⃣ Last attempt → delimiter auto detect
    try:
        df = pd.read_csv(
            file_path,
            encoding="latin1",
            sep=None,
            engine="python",
            low_memory=False,
            on_bad_lines="skip"
        )
        return clean_headers(df)
    except Exception:
        raise Exception(
            "Failed to read CSV. File may be corrupted or unsupported."
        )


def clean_headers(df):
    """
    Normalize messy CRM headers like:
    Country-
    Designation/s
    Notes-
    """

    df.columns = (
        df.columns
        .str.strip()
        .str.replace("-", "", regex=False)
        .str.replace("/", " ", regex=False)
    )

    return df
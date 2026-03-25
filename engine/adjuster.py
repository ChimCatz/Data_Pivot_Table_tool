def scale_summary(summary_table, target_total):

    df = summary_table.copy()

    original_total = df["Count"].sum()

    if original_total == 0:
        return df

    growth_mode = target_total > original_total

    # proportional exact values
    df["Exact"] = df["Count"] / original_total * target_total

    df["Scaled"] = df["Exact"].astype(int)

    # ⭐ force minimum growth for small categories
    if growth_mode:
        mask = (df["Count"] == 1) & (df["Scaled"] < 2)
        df.loc[mask, "Scaled"] = 2

    # recompute remainder
    remainder = target_total - df["Scaled"].sum()

    df["Decimal"] = df["Exact"] - df["Scaled"]

    df = df.sort_values("Decimal", ascending=False)

    i = 0
    while remainder > 0:
        df.iloc[i % len(df), df.columns.get_loc("Scaled")] += 1
        remainder -= 1
        i += 1

    df = df.sort_index()

    df["Count"] = df["Scaled"]

    df = df.drop(columns=["Exact", "Scaled", "Decimal"])

    return df
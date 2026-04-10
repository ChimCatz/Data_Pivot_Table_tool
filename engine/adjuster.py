import math


def scale_summary(summary_table, target_total):

    df = summary_table.copy()

    original_total = int(df["Count"].sum())

    if original_total == 0 or target_total <= 0:
        return df

    if target_total == original_total:
        return df

    category_count = len(df)

    if target_total < category_count:
        target_total = category_count

    remaining_total = target_total - category_count
    original_counts = df["Count"].astype(float)

    adjustment_ratio = abs(target_total - original_total) / original_total
    exponent = max(0.82, 1 - (adjustment_ratio * 0.25))
    weights = original_counts.pow(exponent)

    if weights.sum() == 0:
        weights = original_counts.replace(0, 1)

    df["Scaled"] = 1
    df["Exact"] = 1 + (weights / weights.sum() * remaining_total)
    df["Scaled"] += (df["Exact"] - 1).apply(math.floor).astype(int)
    df["RemainderWeight"] = df["Exact"] - df["Scaled"]

    remainder = target_total - int(df["Scaled"].sum())

    while remainder > 0:
        idx = df["RemainderWeight"].idxmax()
        df.loc[idx, "Scaled"] += 1
        df.loc[idx, "RemainderWeight"] -= 1
        remainder -= 1

    while remainder < 0:
        eligible = df[df["Scaled"] > 1]
        if eligible.empty:
            break
        idx = eligible["RemainderWeight"].idxmin()
        df.loc[idx, "Scaled"] -= 1
        df.loc[idx, "RemainderWeight"] += 1
        remainder += 1

    df["Count"] = df["Scaled"].astype(int)

    return df.drop(columns=["Scaled", "Exact", "RemainderWeight"])

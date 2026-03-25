from matplotlib.figure import Figure


def build_bar_chart(df, field):

    height = max(4, len(df) * 0.6)

    fig = Figure(figsize=(8, height))
    ax = fig.add_subplot(111)

    ax.barh(
        df[field].astype(str),
        df["Count"]
    )

    ax.set_title(f"Top 10 {field}")
    ax.invert_yaxis()

    fig.tight_layout()

    return fig
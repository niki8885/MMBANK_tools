import pandas as pd
import matplotlib.pyplot as plt


def production_profit_analysis(
        production_csv: str,
        market_csv: str,
        output_csv: str,
        top_n: int = 20
):
    prod_df = pd.read_csv(production_csv)
    market_df = pd.read_csv(market_csv)

    df = pd.merge(prod_df, market_df, on="item_id", how="inner", suffixes=('_prod', '_market'))

    df["sell_margin"] = df["sellAvgFivePercent"] - df["Total_production_price"]
    df["buy_margin"] = df["buyAvgFivePercent"] - df["Total_production_price"]
    df["sell_margin_percent"] = df["sell_margin"] / df["Total_production_price"] * 100
    df["buy_margin_percent"] = df["buy_margin"] / df["Total_production_price"] * 100

    df_sorted = df.sort_values(by="sell_margin_percent", ascending=False)
    df_sorted.to_csv(output_csv, index=False)

    top_df = df_sorted.head(top_n)

    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    fig.suptitle(f"Production Profit Analysis (Top {top_n})", fontsize=16)

    top_df.plot(
        x="name_prod",
        y=["Total_production_price", "sellAvgFivePercent"],
        kind="bar",
        ax=axes[0, 0]
    )
    axes[0, 0].set_title("Production vs Sell Price")
    axes[0, 0].set_ylabel("ISK per unit")
    axes[0, 0].tick_params(axis='x', rotation=45)

    top_df.plot(
        x="name_prod",
        y=["Total_production_price", "buyAvgFivePercent"],
        kind="bar",
        ax=axes[0, 1]
    )
    axes[0, 1].set_title("Production vs Buy Price")
    axes[0, 1].set_ylabel("ISK per unit")
    axes[0, 1].tick_params(axis='x', rotation=45)

    top_df.plot(
        x="name_prod",
        y="sell_margin_percent",
        kind="bar",
        color='green',
        ax=axes[1, 0]
    )
    axes[1, 0].set_title("Sell Margin %")
    axes[1, 0].set_ylabel("Margin %")
    axes[1, 0].tick_params(axis='x', rotation=45)

    top_df.plot(
        x="name_prod",
        y="buy_margin_percent",
        kind="bar",
        color='blue',
        ax=axes[1, 1]
    )
    axes[1, 1].set_title("Buy Margin %")
    axes[1, 1].set_ylabel("Margin %")
    axes[1, 1].tick_params(axis='x', rotation=45)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

    print("Analysis complete. Top products by sell margin:")
    print(top_df[["name_prod", "Total_production_price", "sellAvgFivePercent", "sell_margin", "sell_margin_percent"]])

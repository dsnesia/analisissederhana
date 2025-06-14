import matplotlib.pyplot as plt

def save_price_chart(df, coin_name):
    plt.figure(figsize=(8, 4))
    plt.plot(df["date"], df["price"], label=coin_name.upper(), color="blue")
    plt.title(f"Harga {coin_name.upper()} (7 Hari Terakhir)")
    plt.xlabel("Tanggal")
    plt.ylabel("Harga (USD)")
    plt.grid(True)
    plt.tight_layout()
    chart_path = f"{coin_name}_chart.png"
    plt.savefig(chart_path)
    plt.close()
    return chart_path

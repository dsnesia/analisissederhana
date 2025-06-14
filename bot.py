import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from crypto_api import get_crypto_price, get_crypto_info, get_price_history, simple_trend_signal
from chart import save_price_chart
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Kirim /harga btc, /analisis eth, atau /grafik doge")

async def harga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Contoh: /harga btc")
        return
    coin = context.args[0].lower()
    price = get_crypto_price(coin)
    if price:
        await update.message.reply_text(f"Harga {coin.upper()}: ${price}")
    else:
        await update.message.reply_text("Data tidak ditemukan.")

async def analisis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Contoh: /analisis eth")
        return
    coin = context.args[0].lower()
    data = get_crypto_info(coin)
    if data:
        msg = (
            f"🔍 {data['name']} ({data['symbol']})\n"
            f"Harga: ${data['price']:,.2f}\n"
            f"Market Cap: ${data['market_cap']:,.0f}\n"
            f"Volume: ${data['volume']:,.0f}\n"
            f"Perubahan 24h: {data['change_24h']:.2f}%"
        )
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("Data tidak ditemukan.")

async def grafik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Contoh: /grafik doge")
        return
    coin = context.args[0].lower()
    df = get_price_history(coin)
    if df is not None:
        signal = simple_trend_signal(df)
        chart_path = save_price_chart(df, coin)
        with open(chart_path, 'rb') as f:
            await update.message.reply_photo(f, caption=signal)
    else:
        await update.message.reply_text("Gagal mengambil data grafik.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("harga", harga))
app.add_handler(CommandHandler("analisis", analisis))
app.add_handler(CommandHandler("grafik", grafik))

print("Bot berjalan...")
app.run_polling()

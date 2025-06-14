import logging
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
BINANCE_URL = "https://api.binance.com/api/v3"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Selamat datang!\nGunakan:\n/harga BTCUSDT\n/analisis ETHUSDT")

async def harga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol = context.args[0].upper()
        res = requests.get(f"{BINANCE_URL}/ticker/price?symbol={symbol}")
        data = res.json()
        if 'price' in data:
            await update.message.reply_text(f"Harga {symbol}: ${data['price']}")
        else:
            await update.message.reply_text("❌ Simbol tidak valid.")
    except:
        await update.message.reply_text("❌ Format salah. Gunakan: /harga BTCUSDT")

async def analisis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol = context.args[0].upper()
        url = f"{BINANCE_URL}/klines?symbol={symbol}&interval=1h&limit=25"
        data = requests.get(url).json()

        closes = [float(k[4]) for k in data]
        ma7 = sum(closes[-7:]) / 7
        ma25 = sum(closes) / 25

        trend = "📈 Bullish" if ma7 > ma25 else "📉 Bearish"
        msg = (
            f"📊 *Analisis {symbol}*\n"
            f"MA 7 jam: {ma7:.2f}\n"
            f"MA 25 jam: {ma25:.2f}\n"
            f"Sinyal: {trend}"
        )
        await update.message.reply_text(msg, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text("❌ Gagal analisis. Gunakan format /analisis BTCUSDT")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("harga", harga))
app.add_handler(CommandHandler("analisis", analisis))

if __name__ == "__main__":
    app.run_polling()

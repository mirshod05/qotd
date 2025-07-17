import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import asyncio  # To run background tasks alongside the bot
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(
        "Hi and welcome to the Quote of the day bot. Type /quote for a random quote."
    )
def get_quote() -> str:
    response = requests.get('https://zenquotes.io/api/random')
    data = response.json()[0]
    quote = data['q'] + ' - ' + data['a']
    return quote

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quote_text = get_quote()
    await update.message.reply_text(quote_text)

BOT_TOKEN = os.environ["BOT_TOKEN"]
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("quote",quote))

print("Bot is running...")
app.run_polling()


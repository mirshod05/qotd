import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from aiohttp import web
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = "https://qotd-39d0.onrender.com" + WEBHOOK_PATH

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


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("quote",quote))

async def on_startup(app_):
    await app.bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook set to {WEBHOOK_URL}")

async def on_shutdown(app_):
    await app.bot.delete_webhook()
    print("Webhook deleted")

async def handle(request: web.Request) -> web.Response:
    """Handle incoming webhook updates from Telegram."""
    data = await request.json()
    update = Update.de_json(data, app.bot)
    await app.update_queue.put(update)
    return web.Response(text="ok")

web_app = web.Application()
web_app.router.add_post(WEBHOOK_PATH, handle)

web_app.on_startup.append(on_startup)
web_app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    print("Starting webhook server...")
    web.run_app(web_app, host="0.0.0.0", port=10000)


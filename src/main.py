# --- Hydrogram Telegram Client ---
# Kode ini mendukung dua mode: User dan Bot
# Konfigurasi diambil dari file .env

import os

from dotenv import load_dotenv
from hydrogram import Client, filters
from hydrogram.types import BotCommand

load_dotenv()
api_id = os.getenv("TELE__API_ID")
api_hash = os.getenv("TELE__API_HASH")
bot_token = os.getenv("TELE__BOT_TOKEN")


# Fokus ke bot client saja
app_bot = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


def run_bot():
    app_bot.run()


# Handler untuk chat personal (private)
@app_bot.on_message(filters=filters.private)
async def handle_private(client, message):
    print(f"[PRIVATE] Chat ID: {message.chat.id}")
    await message.reply_text(
        f"Halo {message.from_user.first_name}, kamu mengirim: {message.text}"
    )


# Handler untuk group/supergroup, hanya jika bot di-tag
@app_bot.on_message((filters.group & filters.mentioned))
async def handle_group_mention(client, message):
    print(f"[GROUP] Chat ID: {message.chat.id}")
    await message.reply_text(f"Hai, kamu mention bot: {message.text}")


# Handler untuk channel, hanya log pesan
@app_bot.on_message(filters.channel)
async def handle_channel(client, message):
    print(f"[CHANNEL] Chat ID: {message.chat.id} | Pesan: {message.text}")


# Contoh handler command /start
@app_bot.on_message(filters.command("start"))
async def start_command(client, message):
    await client.set_bot_commands([
        BotCommand("start", "Mulai percakapan"),
        BotCommand("help", "Dapatkan bantuan"),
    ])
    await message.reply_text("Selamat datang di bot!")


# Contoh handler command /help
@app_bot.on_message(filters.command("help"))
async def help_command(client, message):
    await message.reply_text(
        "Ini adalah bantuan bot. Silakan gunakan perintah yang tersedia."
    )

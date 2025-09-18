from loguru import logger
from telethon import TelegramClient, events

from src.config import get_settings
from src.storage import UserStorage

app_settings = get_settings()
api_id = app_settings.TELE.API_ID
api_hash = app_settings.TELE.API_HASH
bot_token = app_settings.TELE.BOT_TOKEN
admin_id = app_settings.TELE.ADMIN_ID

# Singleton client object (tanpa .start())
app_bot = TelegramClient("bot_session", api_id=api_id, api_hash=api_hash)

# Singleton storage object
storage = UserStorage("users.json")

# # ini registers handlers
# PrivateHandlers(app_bot, storage, admin_id)
# GroupHandlers(app_bot)
# ChannelHandlers(app_bot, admin_id)
# AdminHandlers(app_bot, storage, admin_id)
# CallbackHandlers(app_bot, storage, admin_id)


@app_bot.on(event=events.NewMessage(incoming=True, outgoing=False))
async def echo_handler(event):
    sender = await event.get_sender()
    sender_id = sender.id if sender else None
    sender_name = (
        sender.first_name if sender and hasattr(sender, "first_name") else None
    )
    text = event.raw_text
    logger.info(f"[ECHO] From {sender_name} ({sender_id}): {text}")
    # Reply only to private chat
    if event.is_private:
        await event.reply(f"Echo: {text}")


async def main():
    logger.info("Bot is starting...")
    await app_bot.start(bot_token=bot_token)  # type: ignore
    await app_bot.run_until_disconnected()  # type: ignore

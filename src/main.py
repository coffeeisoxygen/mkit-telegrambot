from loguru import logger
from telethon import TelegramClient, events

from src.config import get_settings
from src.database import sqlite_session_manager
from src.storage import UserStorage

app_settings = get_settings()
api_id = app_settings.TELE.API_ID
api_hash = app_settings.TELE.API_HASH
bot_token = app_settings.TELE.BOT_TOKEN
admin_id = app_settings.TELE.ADMIN_ID

# Singleton
client_bot = TelegramClient("bot_session", api_id=api_id, api_hash=api_hash)
client_user = TelegramClient("user_session", api_id=api_id, api_hash=api_hash)
# Singleton storage object
storage = UserStorage("users.json")
sqlite_session = sqlite_session_manager

# If sqlite_session_manager is a class, use:
# sqlite_session = sqlite_session_manager()


# # ini registers handlers
# PrivateHandlers(app_bot, storage, admin_id)
# GroupHandlers(app_bot)
# ChannelHandlers(app_bot, admin_id)
# AdminHandlers(app_bot, storage, admin_id)
# CallbackHandlers(app_bot, storage, admin_id)


@client_bot.on(event=events.NewMessage(incoming=True, outgoing=False))
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
    await client_bot.start(bot_token=bot_token)  # type: ignore
    await client_bot.run_until_disconnected()  # type: ignore
    await client_user.run_until_disconnected()  # type: ignore
    # close sqlite session
    await sqlite_session.close()

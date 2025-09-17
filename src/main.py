import os

from dotenv import load_dotenv
from hydrogram import Client
from loguru import logger

from src.handlers.admin_handlers import AdminHandlers
from src.handlers.callback_handlers import CallbackHandlers
from src.handlers.channel_handlers import ChannelHandlers
from src.handlers.group_handlers import GroupHandlers
from src.handlers.private_handlers import PrivateHandlers
from src.storage import UserStorage

load_dotenv()
api_id = os.getenv("TELE__API_ID")
api_hash = os.getenv("TELE__API_HASH")
bot_token = os.getenv("TELE__BOT_TOKEN")
admin_id = int(os.getenv("TELE__ADMIN_ID", "0"))

# ini singleton client object
app_bot = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# ini singleton storage object
storage = UserStorage("users.json")

# ini registers handlers
PrivateHandlers(app_bot, storage, admin_id)
GroupHandlers(app_bot)
ChannelHandlers(app_bot, admin_id)
AdminHandlers(app_bot, storage, admin_id)
CallbackHandlers(app_bot, storage, admin_id)


def run_bot():
    logger.info("Bot is starting...")
    app_bot.run()

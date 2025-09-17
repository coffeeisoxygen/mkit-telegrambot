from loguru import logger
from telethon import TelegramClient

from src.config import get_settings
from src.handlers.admin_handlers import AdminHandlers
from src.handlers.callback_handlers import CallbackHandlers
from src.handlers.channel_handlers import ChannelHandlers
from src.handlers.group_handlers import GroupHandlers
from src.handlers.private_handlers import PrivateHandlers
from src.storage import UserStorage

app_settings = get_settings()
api_id = app_settings.TELE.API_ID
api_hash = app_settings.TELE.API_HASH
bot_token = app_settings.TELE.BOT_TOKEN
admin_id = app_settings.TELE.ADMIN_ID


# ini singleton client object
app_bot = TelegramClient("my_bot", api_id=api_id, api_hash=api_hash).start(
    bot_token=bot_token
)

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
    app_bot.run_until_disconnected()

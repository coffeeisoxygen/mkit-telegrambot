from loguru import logger
from telethon import TelegramClient, events

from src.config import get_settings
from src.database.sqlite_session import get_sqlite_session, sqlite_session_manager
from src.schemas import UserApprovalStatus
from src.storage import UserStorage
from src.users.user_crud import create_user_entry, get_user_by_telegram_id

app_settings = get_settings()
api_id = app_settings.TELE.API_ID
api_hash = app_settings.TELE.API_HASH
bot_token = app_settings.TELE.BOT_TOKEN
admin_id = app_settings.TELE.ADMIN_ID
admin_name = app_settings.TELE.ADMIN_NAME

#
# Singleton
client_bot = TelegramClient("bot_session", api_id=api_id, api_hash=api_hash)
client_user = TelegramClient("user_session", api_id=api_id, api_hash=api_hash)
# Singleton storage object
storage = UserStorage("users.json")


# # ini registers handlers
# PrivateHandlers(app_bot, storage, admin_id)
# GroupHandlers(app_bot)
# ChannelHandlers(app_bot, admin_id)
# AdminHandlers(app_bot, storage, admin_id)
# CallbackHandlers(app_bot, storage, admin_id)


@client_bot.on(event=events.NewMessage(incoming=True, outgoing=False))
async def echo_handler(event):
    sender = await event.get_sender()
    if not sender:
        return

    sender_id = sender.id
    sender_name = sender.first_name or "N/A"
    text = event.raw_text
    logger.info(f"[ECHO] From {sender_name} ({sender_id}): {text}")

    # Create a new database session for each incoming event
    async with get_sqlite_session() as db_session:
        user = await get_user_by_telegram_id(db_session, sender_id)
        if user:
            logger.info(f"User '{user.name}' found in database.")
        else:
            logger.info(f"User with ID {sender_id} not found in database.")
            if event.is_private:
                await event.reply("anda belum terverifikasi")
            return  # Don't echo if not verified

    # Reply only to private chat
    if event.is_private:
        await event.reply(f"Echo: {text}")


async def seed_admin():
    """Create admin user if not exists."""
    logger.info("Checking admin user...")
    async with get_sqlite_session() as db_session:
        await create_user_entry(
            db_session=db_session,
            user_id=admin_id,
            name="Admin",
            rate_limit=100,
            is_superuser=1,
            status=UserApprovalStatus.APPROVED,
            raise_if_exists=False,
        )
    logger.info("Admin seeding checked/done.")


async def main():
    """App entrypoint."""
    # --- Lifespan Startup ---
    logger.info("Bot is starting...")
    await seed_admin()

    await client_bot.start(bot_token=bot_token)  # type: ignore
    logger.info("Bot client started.")

    # If you also need the user client to run, uncomment the following lines
    # logger.info("Starting user client...")
    # await client_user.start() # type: ignore
    # logger.info("User client started.")

    try:
        logger.info("Running clients until disconnected...")
        await client_bot.run_until_disconnected()  # type: ignore
        # await client_user.run_until_disconnected() # type: ignore
    finally:
        # --- Lifespan Shutdown ---
        logger.info("Closing resources...")
        await sqlite_session_manager.close()
        logger.info("Resources closed. Exiting.")

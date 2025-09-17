from hydrogram import filters
from loguru import logger


class GroupHandlers:
    def __init__(self, app_bot):
        self.app_bot = app_bot
        self.register_handlers()

    def register_handlers(self):
        @self.app_bot.on_message(filters.group & filters.mentioned)
        async def handle_group_mention(client, message):
            logger.info(f"[GROUP] {message.chat.id} | {message.text}")
            if "?" in (message.text or ""):
                await message.reply_text(
                    f"Hai {message.from_user.first_name}, saya dengar pertanyaanmu!"
                )
                logger.info(f"[GROUP] Replied to {message.from_user.id}'s question.")
            else:
                await message.reply_text(
                    f"Hi {message.from_user.first_name} - buat interaksi sama aku, akhir pertanyaan dengan '?'"
                )
                logger.info(
                    f"[GROUP] Replied to {message.from_user.id} for non-question mention."
                )

from hydrogram import filters
from loguru import logger


class ChannelHandlers:
    def __init__(self, app_bot, admin_id):
        self.app_bot = app_bot
        self.admin_id = admin_id
        self.register_handlers()

    def register_handlers(self):
        @self.app_bot.on_message(filters.channel)
        async def handle_channel(client, message):
            logger.info(f"[CHANNEL] {message.chat.id} | Pesan: {message.text}")
            if self.admin_id:
                await client.send_message(
                    self.admin_id, f"[CHANNEL] {message.chat.title} | {message.text}"
                )

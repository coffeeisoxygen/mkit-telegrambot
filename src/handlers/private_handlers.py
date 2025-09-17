from hydrogram import filters
from hydrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger


class PrivateHandlers:
    def __init__(self, app_bot, storage, admin_id):
        self.app_bot = app_bot
        self.storage = storage
        self.admin_id = admin_id
        self.register_handlers()

    def register_handlers(self):
        @self.app_bot.on_message(filters.private)
        async def handle_private(client, message):
            uid = message.from_user.id
            name = message.from_user.first_name
            logger.info(f"[PRIVATE] {uid} | {message.text}")

            if not self.storage.is_user_approved(uid):
                self.storage.add_pending_user(uid, name)
                await message.reply_text(
                    "⏳ Kamu belum terverifikasi. Tunggu admin approve ya."
                )
                if self.admin_id:
                    kb = InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton(
                                "✅ Approve", callback_data=f"approve:{uid}"
                            ),
                            InlineKeyboardButton(
                                "❌ Reject", callback_data=f"reject:{uid}"
                            ),
                        ]
                    ])
                    await client.send_message(
                        self.admin_id,
                        f"👤 User baru minta akses:\nID: {uid}\nNama: {name}\nPesan: {message.text}",
                        reply_markup=kb,
                    )
                return

            await message.reply_text(f"Halo {name}, kamu mengirim: {message.text}")

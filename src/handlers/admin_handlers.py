from hydrogram import filters
from hydrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class AdminHandlers:
    def __init__(self, app_bot, storage, admin_id):
        self.app_bot = app_bot
        self.storage = storage
        self.admin_id = admin_id
        self.register_handlers()

    def register_handlers(self):
        @self.app_bot.on_message(
            filters.command("approve") & filters.user(self.admin_id)
        )
        async def approve_user(client, message):
            parts = message.text.split()
            if len(parts) != 2:
                await message.reply_text("Format: /approve <user_id>")
                return
            uid = int(parts[1])
            self.storage.update_user_status(uid, "approved")
            await message.reply_text(f"✅ User {uid} approved.")
            await client.send_message(
                uid, "✅ Kamu sudah disetujui oleh admin. Silakan chat lagi!"
            )

        @self.app_bot.on_message(
            filters.command("reject") & filters.user(self.admin_id)
        )
        async def reject_user(client, message):
            parts = message.text.split()
            if len(parts) != 2:
                await message.reply_text("Format: /reject <user_id>")
                return
            uid = int(parts[1])
            self.storage.update_user_status(uid, "rejected")
            await message.reply_text(f"❌ User {uid} rejected.")
            await client.send_message(uid, "❌ Kamu ditolak oleh admin.")

        @self.app_bot.on_message(
            filters.command("pending") & filters.user(self.admin_id)
        )
        async def list_pending(client, message):
            pendings = self.storage.get_pending_users()
            if not pendings:
                await message.reply_text("✅ Tidak ada user pending.")
                return
            text = "⏳ Daftar user pending:\n\n"
            buttons = []
            for u in pendings:
                text += f"- {u['name']} (ID: {u['user_id']})\n"
                buttons.append([
                    InlineKeyboardButton(
                        "✅ Approve", callback_data=f"approve:{u['user_id']}"
                    ),
                    InlineKeyboardButton(
                        "❌ Reject", callback_data=f"reject:{u['user_id']}"
                    ),
                ])
            await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))

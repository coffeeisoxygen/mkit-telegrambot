class CallbackHandlers:
    def __init__(self, app_bot, storage, admin_id):
        self.app_bot = app_bot
        self.storage = storage
        self.admin_id = admin_id
        self.register_handlers()

    def register_handlers(self):
        @self.app_bot.on_callback_query()
        async def callback_handler(client, callback_query):
            data = callback_query.data
            action, uid = data.split(":")
            uid = int(uid)
            if callback_query.from_user.id != self.admin_id:
                await callback_query.answer("❌ Kamu bukan admin!", show_alert=True)
                return
            if action == "approve":
                self.storage.update_user_status(uid, "approved")
                await client.send_message(
                    uid, "✅ Kamu sudah disetujui oleh admin. Silakan chat lagi!"
                )
                await callback_query.answer("User approved ✅")
            elif action == "reject":
                self.storage.update_user_status(uid, "rejected")
                await client.send_message(uid, "❌ Kamu ditolak oleh admin.")
                await callback_query.answer("User rejected ❌")

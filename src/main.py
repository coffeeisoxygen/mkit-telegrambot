import os

from dotenv import load_dotenv
from hydrogram import Client, filters
from hydrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger
from tinydb import Query, TinyDB

# --- CONFIG ---
load_dotenv()
api_id = os.getenv("TELE__API_ID")
api_hash = os.getenv("TELE__API_HASH")
bot_token = os.getenv("TELE__BOT_TOKEN")

admin_id = int(os.getenv("TELE__ADMIN_ID", "443374733"))  # chat ID admin

# --- STORAGE ---
db = TinyDB("users.json")
UserQ = Query()

# --- BOT CLIENT ---
app_bot = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


def run_bot():
    logger.info("Bot is starting...")
    app_bot.run()


# --- HELPER FUNCTIONS ---
def is_user_approved(uid: int) -> bool:
    res = db.search(UserQ.user_id == uid)
    return bool(res and res[0]["status"] == "approved")


def add_pending_user(uid: int, name: str):
    if not db.search(UserQ.user_id == uid):
        db.insert({"user_id": uid, "name": name, "status": "pending"})


def update_user_status(uid: int, status: str):
    db.update({"status": status}, UserQ.user_id == uid)


def get_pending_users():
    return db.search(UserQ.status == "pending")


# --- HANDLERS ---


# Private chat
@app_bot.on_message(filters.private)
async def handle_private(client, message):
    uid = message.from_user.id
    name = message.from_user.first_name
    logger.info(f"[PRIVATE] {uid} | {message.text}")

    if not is_user_approved(uid):
        add_pending_user(uid, name)

        await message.reply_text(
            "⏳ Kamu belum terverifikasi. Tunggu admin approve ya."
        )
        # Forward ke admin
        if admin_id:
            kb = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ Approve", callback_data=f"approve:{uid}"),
                    InlineKeyboardButton("❌ Reject", callback_data=f"reject:{uid}"),
                ]
            ])
            await client.send_message(
                admin_id,
                f"👤 User baru minta akses:\nID: {uid}\nNama: {name}\nPesan: {message.text}",
                reply_markup=kb,
            )
        return

    # Jika approved
    await message.reply_text(f"Halo {name}, kamu mengirim: {message.text}")


# Group mention handler (only respond if tagged + has a question)
@app_bot.on_message(filters.group & filters.mentioned)
async def handle_group_mention(client, message):
    logger.info(f"[GROUP] {message.chat.id} | {message.text}")
    if "?" in (message.text or ""):
        await message.reply_text(
            f"Hai {message.from_user.first_name}, saya dengar pertanyaanmu!"
        )


# Channel log handler
@app_bot.on_message(filters.channel)
async def handle_channel(client, message):
    logger.info(f"[CHANNEL] {message.chat.id} | Pesan: {message.text}")
    if admin_id:
        await client.send_message(
            admin_id, f"[CHANNEL] {message.chat.title} | {message.text}"
        )


# Approve / Reject Command (admin only)
@app_bot.on_message(filters.command("approve") & filters.user(admin_id))
async def approve_user(client, message):
    parts = message.text.split()
    if len(parts) != 2:
        await message.reply_text("Format: /approve <user_id>")
        return

    uid = int(parts[1])
    update_user_status(uid, "approved")
    await message.reply_text(f"✅ User {uid} approved.")
    await client.send_message(
        uid, "✅ Kamu sudah disetujui oleh admin. Silakan chat lagi!"
    )


@app_bot.on_message(filters.command("reject") & filters.user(admin_id))
async def reject_user(client, message):
    parts = message.text.split()
    if len(parts) != 2:
        await message.reply_text("Format: /reject <user_id>")
        return

    uid = int(parts[1])
    update_user_status(uid, "rejected")
    await message.reply_text(f"❌ User {uid} rejected.")
    await client.send_message(uid, "❌ Kamu ditolak oleh admin.")


# List pending users (admin only)
@app_bot.on_message(filters.command("pending") & filters.user(admin_id))
async def list_pending(client, message):
    pendings = get_pending_users()
    if not pendings:
        await message.reply_text("✅ Tidak ada user pending.")
        return

    text = "⏳ Daftar user pending:\n\n"
    buttons = []
    for u in pendings:
        text += f"- {u['name']} (ID: {u['user_id']})\n"
        buttons.append([
            InlineKeyboardButton("✅ Approve", callback_data=f"approve:{u['user_id']}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject:{u['user_id']}"),
        ])

    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))


# Handle callback (approve/reject via button)
@app_bot.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data
    action, uid = data.split(":")
    uid = int(uid)

    if callback_query.from_user.id != admin_id:
        await callback_query.answer("❌ Kamu bukan admin!", show_alert=True)
        return

    if action == "approve":
        update_user_status(uid, "approved")
        await client.send_message(
            uid, "✅ Kamu sudah disetujui oleh admin. Silakan chat lagi!"
        )
        await callback_query.answer("User approved ✅")
    elif action == "reject":
        update_user_status(uid, "rejected")
        await client.send_message(uid, "❌ Kamu ditolak oleh admin.")
        await callback_query.answer("User rejected ❌")

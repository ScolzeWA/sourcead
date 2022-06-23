import asyncio
from config import BOT_USERNAME, SUDO_USERS
from NIXA.decorators import authorized_users_only, sudo_users_only, errors
from NIXA.filters import command, other_filters
from NIXA.filters import command2, other_filters
from NIXA.main import user as USER
from pyrogram import filters
from NIXA.main import bot as Client
from pyrogram.errors import UserAlreadyParticipant


@Client.on_message(
    command2(["المساعد","انضم"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def join_group(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except BaseException:
        await message.reply_text(
            "• **ɪ'ᴍ ɴᴏᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ:**\n\n» ❌ __ᴀᴅᴅ ᴜsᴇʀs__",
        )
        return

    try:
        user = await USER.get_me()
    except BaseException:
        user.first_name = "music assistant"

    try:
        await USER.join_chat(invitelink)
    except UserAlreadyParticipant:
        pass
    except Exception as e:
        print(e)
        await message.reply_text(
            f"🛑 تعذر الدخول 🛑 \n\n**اكتب تشغيل لكي ينضم**"
            "\n\n**او تفقد ان الحساب المساعد غير مقيد**",
        )
        return
    await message.reply_text(
        f"انا جيت اهو يارب مكونش اتٲخرت",
    )


@Client.on_message(command2(["غادر"]) & filters.group & ~filters.edited)
@authorized_users_only
async def leave_one(client, message):
    try:
        await USER.send_message(message.chat.id, "✅ طلب المعلم تم مغادرتي")
        await USER.leave_chat(message.chat.id)
    except BaseException:
        await message.reply_text(
            "❌ **هناك خطأ, تأكد ان حساب المساعد.**\n\n**» ليس لديه رتبة اشراف**"
        )

        return


@Client.on_message(command2(["غادر الكل"]))
@sudo_users_only
async def leave_all(client, message):
    if message.from_user.id not in SUDO_USERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("🔄 **ᴜsᴇʀʙᴏᴛ** ʟᴇᴀᴠɪɴɢ ᴀʟʟ ᴄʜᴀᴛs !")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            left += 1
            await lol.edit(
                f"تم خروج المساعد."
            )
        except BaseException:
            failed += 1
            await lol.edit(
                f"تم خروج المساعد بعد انهاء الاغنيه ."
            )
        await asyncio.sleep(0.7)
    await client.send_message(
        message.chat.id, f"✅ ʟᴇғᴛ ғʀᴏᴍ: {left} ᴄʜᴀᴛs.\n❌ ғᴀɪʟᴇᴅ ɪɴ: {failed} ᴄʜᴀᴛs."
    )

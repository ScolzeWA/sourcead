from NIXA.main import bot
from pyrogram import filters


@bot.on_message(filters.command('id'))
def ids(_, message):
    reply = message.reply_to_message
    if reply:
        message.reply_text(
            f"**ʏᴏᴜʀ ɪᴅ**: `{message.from_user.id}`\n**{reply.from_user.first_name}'s ɪᴅ**: `{reply.from_user.id}`\n**ᴄʜᴀᴛ ɪᴅ**: `{message.chat.id}`"
        )
    else:
        message.reply(
            f"**ʏᴏᴜʀ ɪᴅ**: `{message.from_user.id}`\n**ᴄʜᴀᴛ ɪᴅ**: `{message.chat.id}`"
        )

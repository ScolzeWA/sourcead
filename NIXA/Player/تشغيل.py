import io
from os import path
from typing import Callable
from asyncio.queues import QueueEmpty
import os
import random
import re

import aiofiles
import aiohttp
from NIXA.converter import convert
import ffmpeg
import requests
from NIXA.fonts import CHAT_TITLE
from PIL import Image, ImageDraw, ImageFont
from config import ASSISTANT_NAME, BOT_USERNAME, IMG_1, IMG_2, IMG_5, UPDATES_CHANNEL, GROUP_SUPPORT, START_PIC
from NIXA.filters import command2, other_filters
from NIXA.queues import QUEUE, add_to_queue
from NIXA.main import call_py, Test as user
from NIXA.utils import bash
from NIXA.main import bot as Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from youtubesearchpython import VideosSearch
import yt_dlp
import yt_dlp

FOREGROUND_IMG = [
    "Process/ImageFont/Red.png",
    "Process/ImageFont/Black.png",
    "Process/ImageFont/Blue.png",
    "Process/ImageFont/Grey.png",
    "Process/ImageFont/Green.png",
    "Process/ImageFont/Lightblue.png",
    "Process/ImageFont/Lightred.png",
    "Process/ImageFont/Purple.png",
]

def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = data["thumbnails"][0]["url"]
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0


async def ytdl(format: str, link: str):
    stdout, stderr = await bash(f'yt-dlp --geo-bypass -g -f "[height<=?720][width<=?1280]" {link}')
    if stdout:
        return 1, stdout
    return 0, stderr

chat_id = None
DISABLED_GROUPS = []
useer = "NaN"
ACTV_CALLS = []




def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", 
        format="s16le", 
        acodec="pcm_s16le", 
        ac=2, 
        ar="48k"
    ).overwrite_output().run()
    os.remove(filename)

def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))



def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def generate_cover(thumbnail, title, userid, ctitle):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open(f"thumb{userid}.png", mode="wb")
                await f.write(await resp.read())
                await f.close()
    image1 = Image.open(f"thumb{userid}.png")
    image2 = Image.open("Process/ImageFont/Nixa.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save(f"temp{userid}.png")
    img = Image.open(f"temp{userid}.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Process/ImageFont/finalfont.ttf", 60)
    font2 = ImageFont.truetype("Process/ImageFont/finalfont.ttf", 70)     
    draw.text((20, 45), f"{title[:30]}...", fill= "white", stroke_width = 1, stroke_fill="white", font=font2)
    draw.text((120, 595), f"Playing on: {ctitle[:20]}...", fill="white", stroke_width = 1, stroke_fill="white" ,font=font)
    img.save(f"final{userid}.png")
    os.remove(f"temp{userid}.png")
    os.remove(f"thumb{userid}.png") 
    final = f"final{userid}.png"
    return final



    
@Client.on_message(command2(["تشغيل","شغل"]) & other_filters)
async def play(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
                  [[
                      InlineKeyboardButton("▢", callback_data="cbstop"),
                      InlineKeyboardButton("II", callback_data="cbpause"),
                      InlineKeyboardButton("‣‣I", "skip"),
                      InlineKeyboardButton("▷", callback_data="cbresume"),
                  ],[
                      InlineKeyboardButton(text="🥇 ¦ الــجــروب", url=f"https://t.me/{GROUP_SUPPORT}"),
                      InlineKeyboardButton(text="⚙️ ¦ الـسـورس", url=f"https://t.me/{UPDATES_CHANNEL}"),
                  ],[
                      InlineKeyboardButton("•مسح•", callback_data="cls")],
                  ]
             )
    if m.sender_chat:
        return await m.reply_text("ʏᴏᴜ'ʀᴇ ᴀɴ __ᴀɴᴏɴʏᴍᴏᴜs__ ᴀᴅᴍɪɴ !\n\n» ʀᴇᴠᴇʀᴛ ʙᴀᴄᴋ ᴛᴏ ᴜsᴇʀ ᴀᴄᴄᴏᴜɴᴛ ғʀᴏᴍ ᴀᴅᴍɪɴ ʀɪɢʜᴛs.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 لأستخدام هذا البوت ارفعه مشرف اولا **في مجموعتك** بعد هذا اعطني **الصلاحيات**:\n\n» ❌ __حذف الرسائل__\n» ❌ __اضافة مستخدمين__\n» ❌ __ ادارة المحادثه __\n\n المرئيه**تحديث**ليتم تحديث البوت**وقاعة البيانات**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "عذرا اعطني صلاحية:" + "\n\n» ❌ __ادارة المحادثه__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "عذرا اعطني صلاحية:" + "\n\n» ❌ __حذف الرسائل__"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("عذرا اعطني صلاحية:" + "\n\n» ❌ __اضافة مستخدمين__")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **حساب المساعد محظور من المجموعه** {m.chat.title}\n\n» **الغي حظره واكتم انضم لكي ينضم المساعد.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **فشل الحساب المساعد في الانضمام**\n\n**سبب**: `{e}`")
                return
        else:
            try:
                invitelink = await c.export_chat_invite_link(
                    m.chat.id
                )
                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
                await user.join_chat(invitelink)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"❌ **فشل حساب المساعد في الانضمام**\n\n**سبب**: `{e}`"
                )
    if replied:
        if replied.audio or replied.voice:
            suhu = await replied.reply("📥 **جاري التحميل...**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:70]
                else:
                    if replied.audio.file_name:
                        songname = replied.audio.file_name[:70]
                    else:
                        songname = "Audio"
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 **تم اضافتها الى قائمة الانتظار »** `{pos}`\n\n🏷 **الاسم:** [{songname}]({link}) | `ᴍᴜsɪᴄ`\n💭 **الدردشة:** `{chat_id}`\n🎧 **طلب المعلم:** {m.from_user.mention()}",
                    reply_markup=keyboard,
                )
            else:
             try:
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().local_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_2}",
                    caption=f"🏷 **الاسم:** [{songname}]({link})\n💭 **الدردشة:** `{chat_id}`\n💡 **sᴛᴀᴛᴜs:** `ᴘʟᴀʏɪɴɢ`\n🎧 **طلب المعلم:** {requester}\n📹 **نوع المطلوب:** `اغنيه`",
                    reply_markup=keyboard,
                )
             except Exception as e:
                await suhu.delete()
                await m.reply_text(f"🚫 ᴇʀʀᴏʀ:\n\n» {e}")
        
    else:
        if len(m.command) < 2:
         await m.reply_photo(
                     photo=f"{START_PIC}",
                    caption="💬**اكتب: شغل  او تشغيل بل رد على ملف صوتي**"
                    ,
                      reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("مسح", callback_data="cls")
                        ]
                    ]
                )
            )
        else:
            suhu = await m.reply_text(
        f"**جاري التحميل**\n\n0% ▓▓▓▓▓▓▓▓▓▓▓▓ 100%"
    )
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await suhu.edit("💬 **لم اجد شيئ للأسف.**")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                userid = m.from_user.id
                gcname = m.chat.title
                ctitle = await CHAT_TITLE(gcname)
                image = await generate_cover(thumbnail, title, userid, ctitle)
                format = "bestaudio"
                abhi, ytlink = await ytdl(format, url)
                if abhi == 0:
                    await suhu.edit(f"💬 ʏᴛ-ᴅʟ ɪssᴜᴇs ᴅᴇᴛᴇᴄᴛᴇᴅ\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await suhu.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        await m.reply_photo(
                            photo=image,
                            caption=f"💡 **تم اضافتها الى قائمة الانتظار »** `{pos}`\n\n🏷 **الاسم:** [{songname[:22]}]({url}) | `الدقايق`\n**⏱ عدد:** `{duration}`\n🎧 **طلب المعلم:** {requester}",
                            reply_markup=keyboard,
                        )
                    else:
                        try:
                            await suhu.edit(
                            f"**جاري التحميل**\n\n**اسم الملف**: {title[:22]}\n\n100% ████████████100%\n\n**الوقت المستغرق**: 00:00 الثواني\n\n**تحويل الصوت[عملية التحويل تجري]**"
                        )
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=image,
                                caption=f"🏷 **الاسم:** [{songname[:22]}]({url})\n**⏱ المدة:** `{duration}`\n💡 **نوع المطلوب:** `موسيقى`\n🎧 **طلب المعلم:** {requester}",
                                reply_markup=keyboard,
                            )
                        except Exception as ep:
                            await suhu.delete()
                            await m.reply_text(f"💬 ᴇʀʀᴏʀ: `{ep}`")

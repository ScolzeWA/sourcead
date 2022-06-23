import asyncio
from time import time
from datetime import datetime
from config import BOT_USERNAME
from config import GROUP_SUPPORT, UPDATES_CHANNEL, START_PIC
from NIXA.filters import command
from NIXA.command import commandpro
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from NIXA.main import bot as Client

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)
    
   

@Client.on_message(command("start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_photo(
        photo=f"{START_PIC}",
        caption=f"""**━━━━━━━━━━━━
اهـلا يـبـنـي.؟ {message.from_user.mention()} !
مـرحبآ بـك انــا بــوت اقـوم بــتـشـغـيـل الاغــانــي فـي الـمـڪـالـمـه الـصـوتـية .🤔❤؟
يمكنني التشغيل بصوت رائع وبدون اي مشاكل او تقطيع في الاغنيه
 +اضفني الى مجموعتك وارفعني رول بشڪل مع ڪامل الصلاحيات
 البوت يشتغل بالاوامر عربي وانجليزي
 لانضمام الحساب المساعد لتشغيل البوت اكتب انضم


  لمعرفة استخدامي بشڪل صحيح اضغط علي زر الاوامر. 🤔𝑫𝑬𝑽 [𝑾𝑶𝑹𝑳𝑫 𝑴𝑼𝑺𝑰𝑪 💗ˣ](t.me/WORLD_MUSIC_F)
━━━━━━━━━━━━━━━━━━**""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "☬ اضفني الى مجموعتك ☬", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🖥 ¦ الأوامــر", url=f"https://telegra.ph/%F0%9D%91%BE%F0%9D%91%B6%F0%9D%91%B9%F0%9D%91%B3%F0%9D%91%AB-%F0%9D%91%B4%F0%9D%91%BC%F0%9D%91%BA%F0%9D%91%B0%F0%9D%91%AA-%CB%A3-06-23"
                    ),
                    InlineKeyboardButton(
                        "المطور", url="https://t.me/WORLD_MUSIC_F"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⚙️ ¦ الـسـورس", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                    InlineKeyboardButton(
                        "🥇 ¦ الــجروب", url=f"https://t.me/{GROUP_SUPPORT}"
                    )
                ]
                
           ]
        ),
    )
    
@Client.on_message(command(["source"]) & filters.group & ~filters.edited)
async def start(client: Client, message: Message):
    await message.delete()
    await message.reply_photo(
        photo=f"https://telegra.ph/file/a6c96cdbd066ca2388d06.jpg",
        caption=f"""ᴘʀᴏɢʀᴀᴍᴍᴇʀ [𝘿𝙀𝙑𝙀𝙇𝙊𝙋𝙀𝙍 ☤ ](https://t.me/WORLD_MUSIC_F) 𖡼\nᴛᴏ ᴄᴏᴍᴍụɴɪᴄᴀᴛᴇ ᴛᴏɢᴇᴛʜᴇʀ 𖡼\nғᴏʟʟᴏᴡ ᴛʜᴇ ʙụᴛᴛᴏɴѕ ʟᴏᴡᴇʀ 𖡼""",
        reply_markup=InlineKeyboardMarkup(
         [
            [
                InlineKeyboardButton("♡اضف البوت الى مجموعتك♡", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
            ]
         ]
     )
  )

@Client.on_message(command(["developer","dev"]) & filters.group & ~filters.edited)
async def help(client: Client, message: Message):
    await message.delete()
    await message.reply_photo(
        photo=f"{START_PIC}",
        caption=f"""◍ مش محتاجين نكتب كلام كتير خش ع اول زرار وانت هتعرف""",
        reply_markup=InlineKeyboardMarkup(
         [
            [
                InlineKeyboardButton("• 𝘿𝙀𝙑𝙀𝙇𝙊𝙋𝙀𝙍 ☤ ", url=f"https://t.me/WORLD_MUSIC_F"),
            ],
            [
                InlineKeyboardButton("ضيـف البـوت لمجمـوعتـك ✅", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
            ]
         ]
     )
  )
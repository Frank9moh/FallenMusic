import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import AudioPiped
import youtube_dl

# إعدادات Telegram API
API_ID = '6789249'
API_HASH = 'b0e83186601cc8a8953673d327cb5265'
BOT_TOKEN = '6397303521:AAFwTeFpGhT0uXnZIs5lNLoreMHB8mp8a6o'
SESSION_NAME = 'calls.session' # يمكن أن تكون جلسة بوت أو مستخدم

# إعداد Telegram Client و PyTgCalls
app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
pytgcalls = PyTgCalls(app)

# دالة لتحميل الصوت من YouTube
def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# تشغيل الموسيقى عند استقبال أمر "/play"
@app.on_message(filters.command("play") & filters.group)
async def play(_, message: Message):
    if len(message.command) < 2:
        await message.reply_text("يرجى تقديم رابط YouTube بعد الأمر /play")
        return

    url = message.command[1]
    await message.reply_text("جاري تحميل الصوت، يرجى الانتظار...")
    audio_file = download_audio(url)
    chat_id = message.chat.id

    await pytgcalls.join_group_call(
        chat_id,
        AudioPiped(audio_file),
    )

    await message.reply_text(f"تشغيل الموسيقى في المكالمة الصوتية: {url}")

# بدء تشغيل العميل والمكالمات
async def main():
    await app.start()
    await pytgcalls.start()
    await idle()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

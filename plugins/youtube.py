from datetime import datetime, timedelta
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from handlers.ytdlfunc import extractYt, create_buttons
import wget
import os
import ffmpeg
from PIL import Image

from plugins.google import get_text

ytregex = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
youtube_next_fetch = 0
user_time = {}


@Client.on_message(filters.command("yt"))
async def ytdl(_, message):
    await message.reply_chat_action("typing")
    msg = await message.reply_text("Processing...")
    userLastDownloadTime = user_time.get(message.chat.id)
    try:
        if userLastDownloadTime > datetime.now():
            wait_time = round((userLastDownloadTime - datetime.now()).total_seconds() / 60, 2)
            await msg.edit(f"`Wait {wait_time} Minutes before next Request`")
            return
    except:
        pass
    url = get_text(message)    
    if not url:
        return await msg.edit("**Give Me YouTube Link To Download.**")
    try:
        title, thumbnail_url, formats = extractYt(url)
        now = datetime.now()
        user_time[message.chat.id] = now + \
                                         timedelta(minutes=youtube_next_fetch)
    except Exception:
        await msg.edit("`Failed To Fetch Youtube Data... 😔 \nPossible Youtube Blocked server ip \n#error`")
        return
    buttons = InlineKeyboardMarkup(list(create_buttons(formats)))
    try:
        img = wget.download(thumbnail_url)
        im = Image.open(img).convert("RGB")
        output_directory = os.path.join(os.getcwd(), "downloads", str(message.chat.id))
        if not os.path.isdir(output_directory):
            os.makedirs(output_directory)
        thumb_image_path = f"{output_directory}.jpg"
        im.save(thumb_image_path,"jpeg")
        await message.reply_photo(thumb_image_path, caption=title, reply_markup=buttons)
        await msg.delete()
    except Exception as e:
        print(e)
        try:
            thumbnail_url = "https://telegra.ph/file/ce37f8203e1903feed544.png"
            await message.reply_photo(thumbnail_url, caption=title, reply_markup=buttons)
        except Exception as e:
            await msg.edit(
            f"<code>{e}</code> #Error")

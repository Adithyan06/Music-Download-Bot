import os
import ffmpeg
import time
import requests
import youtube_dl
import yt_dlp
from pyrogram import filters, Client
from youtube_search import YoutubeSearch
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))

@Client.on_message(filters.command(["s", "song", "music"]))
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    chat_id = message.chat.id
    m = message.reply('🔎 `Searching for your Song...`')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
            views = results[0]["views"]

            thor = results[0]["channel"]
          
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('Found Nothing ❌\nChange the Spelling & Try.\n\n`/s Believer`')
            return
    except Exception as e:
        m.edit(
            "❎ 𝐹𝑜𝑢𝑛𝑑 𝑁𝑜𝑡ℎ𝑖𝑛𝑔. 𝐒𝐨𝐫𝐫𝐲.\n\n𝖯𝗅𝖾𝖺𝗌𝖾 𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇 𝖮𝗋 𝖲𝖾𝖺𝗋𝖼𝗁 𝖺𝗍 Google.com 𝖥𝗈𝗋 𝖢𝗈𝗋𝗋𝖾𝖼𝗍 𝖲𝗉𝖾𝗅𝗅𝗂𝗇𝗀 𝗈𝖿 𝗍𝗁𝖾 𝙎𝙤𝙣𝙜.\n\nEg.`/s Believer`"
        )
        print(str(e))
        return
    m.edit("`Uploading Your Song....Please Wait`🙏\nPlease don't **Spam** me![🥺](https://telegra.ph/file/33e209cb838912e8714c9.mp4)")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        ironman = f'🍁 **Tittle** : __{title}__\n🍁 **Channel** : `{thor}`\n🍁 **Requested For** : `{query}`'
        rep = f"🎧 𝗧𝗶𝘁𝘁𝗹𝗲 : [{title[:35]}]({link})\n⏳ 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻 : `{duration}`\n👀 𝗩𝗶𝗲𝘄𝘀 : `{views}`\n\n📮 **By** : [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n📤 𝗕𝘆 : @MusicDownloadv2bot"
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton('Search Inline', switch_inline_query_current_chat='')]])
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        client.send_chat_action(chat_id, "upload_photo")
        message.reply_photo(thumbnail, caption=ironman, parse_mode='md', ttl_seconds=500)
        client.send_chat_action(chat_id, "upload_audio")
        message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=True, title=title, duration=dur, performer=str(info_dict["uploader"]), reply_markup=buttons, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit(f'😔**Failed**\n\n__Report this Error to my [Master](https://t.me/Peterparker6)\nOr try__ : `/spotify {query}`')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

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

@Client.on_message(filters.command(["v", "video", "vsong"]))
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    chat_id = message.chat.id
    m = message.reply("`🔎Searching for your Video Song...`")
    ydl_opts = {
        "format": "b[filesize<150M] / w",
        "preferedformat": "mp4",
        "outtmpl": "%(id)s.mp4",
    }
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
            m.edit('𝐅𝐨𝐮𝐧𝐝 𝐍𝐨𝐭𝐡𝐢𝐧𝐠. 𝐓𝐫𝐲 𝐂𝐡𝐚𝐧𝐠𝐢𝐧𝐠 𝐓𝐡𝐞 𝐒𝐩𝐞𝐥𝐥𝐢𝐧𝐠 𝐀 𝐋𝐢𝐭𝐭𝐥𝐞 🌝.\n\n`/v Faded`')
            return
    except Exception as e:
        m.edit(
            "❎ 𝐹𝑜𝑢𝑛𝑑 𝑁𝑜𝑡ℎ𝑖𝑛𝑔. 𝐒𝐨𝐫𝐫𝐲.\n\n𝖯𝗅𝖾𝖺𝗌𝖾 𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇 𝖮𝗋 𝖲𝖾𝖺𝗋𝖼𝗁 𝖺𝗍 Google.com 𝖥𝗈𝗋 𝖢𝗈𝗋𝗋𝖾𝖼𝗍 𝖲𝗉𝖾𝗅𝗅𝗂𝗇𝗀 𝗈𝖿 𝗍𝗁𝖾 𝙎𝙤𝙣𝙜.\n\nEg.`/v Believer`"
        )
        print(str(e))
        return
    m.edit("__Uploading Your Video....Please Wait__🙏🏻\nPlease don't **Spam** me![🥺](https://telegra.ph/file/988fecf605d9e2caf0a50.mp4)")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            video_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"🎧 𝗧𝗶𝘁𝘁𝗹𝗲 : [{title[:35]}]({link})\n⏳ 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻 : `{duration}`\n👀 𝗩𝗶𝗲𝘄𝘀 : `{views}`\n🍁**Channel** : `{thor}`\n⭕ **Requested For** : `{query}`\n\n📬 **By** : [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n📤 𝗕𝘆 : @MusicDownloadv2bot"
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton('Search Inline', switch_inline_query_current_chat='')]])
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        client.send_chat_action(chat_id, "upload_video")
        message.reply_video(video_file, caption=rep, parse_mode='md',quote=True, duration=dur, reply_markup=buttons, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('😔 **Failed**\n\n`Report this Error to` @Peterparker6 🧑‍💻')
        print(e)
    try:
        os.remove(video_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

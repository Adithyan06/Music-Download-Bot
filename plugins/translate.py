from pyrogram import Client, filters
from pyrogram.types import Message
from gpytranslate import Translator

trans = Translator()

TEXT = """💛 <u>**Language Codes**</u>

          • `af` - Afrikaans 
          • `am` - Amharic 
          • `ar` - Arabic 
          • `az` - Azerbaijani 
          • `be` - Belarusian 
          • `bg` - Bulgarian 
          • `bn` - Bengali 
          • `bs` - Bosnian 
          • `ca` - Catalan 
          • `ceb` - Chechen 
          • `co` - Corsican 
          • `cs` - Czech 
          • `cy` - Welsh 
          • `da` - Danish 
          • `de` - German 
          • `el` - Greek 
          • `en` - English 
          • `eo` - Esperanto 
          • `es` - Spanish 
          • `et` - Estonian 
          • `eu` - Basque 
          • `fa` - Persian 
          • `fi` - Finnish 
          • `fr` - French 
          • `fy` - WesternFrisian
          • `ga` - Irish 
          • `gd` - Gaelic 
          • `gl` - Galician 
          • `gu` - Gujarati 
          • `ha` - Hausa 
          • `haw` - ??? 
          • `hi` - Hindi 
          • `hmn` - ??? 
          • `hr` - Croatian 
          • `ko` - Korean 
          • `ku` - Kurdish 
          • `ky` - Kirghiz 
          • `la` - Latin 
          • `lb` - Luxembourgish 
          • `lo` - Lao 
          • `lt` - Lithuanian 
          • `lv` - Latvian 
          • `mg` - Malagasy 
          • `mi` - Maori 
          • `mk` - Macedonian 
          • `ml` - Malayalam 
          • `mn` - Mongolian 
          • `mr` - Marathi 
          • `ms` - Malay 
          • `sk` - Slovak 
          • `sl` - Slovenian 
          • `sm` - Samoan 
          • `sn` - Shona 
          • `so` - Somali 
          • `sq` - Albanian 
          • `sr` - Serbian 
          • `st` - Southern Sotho
          • `su` - Sundanese 
          • `sv` - Swedish 
          • `sw` - Swahili 
          • `ta` - Tamil 
          • `te` - Telugu 
          • `zh_CN` - Chinese 
          • `zh_TW` - Chinese 
          • `zu` - Zulu 

**By @MusicDownloadv2bot**"""

@Client.on_message(filters.command(["tl", "tr"]))
async def translate(_, message: Message) -> None:
    reply_msg = message.reply_to_message
    if not reply_msg:
        await message.reply_text("**Please reply to a message to translate it!** 😊\n\nSupporting Languages - /lang")
        return
    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = await trans.detect(to_translate)
            dest = args
    except IndexError:
        source = await trans.detect(to_translate)
        dest = "id"
    translation = await trans(to_translate, sourcelang=source, targetlang=dest)
    reply = (
        f"👉 <b>Translated from --> {source} to {dest}</b>:\n\n"
        f"📍 <code>{translation.text}</code>\n\n"
        f"@MusicDownloadv2bot"
    )

    await message.reply_text(reply, parse_mode="html", quote=True)

@Client.on_message(filters.command(["lang", "language"]))
async def lang(client, message):
    await message.reply_text(text=TEXT, quote=True)

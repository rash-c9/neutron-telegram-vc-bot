##################################################
## Biggest thanks to @theHamkerCat (on telegram)##
##################################################

from __future__ import unicode_literals
import youtube_dl
import asyncio
import aiohttp
import aiofiles
import time
import json
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from youtube_search import YoutubeSearch
from config import owner_id, bot_token, radio_link, sudo_chat_id, neutron_id

app = Client(
    ":memory:",
    bot_token=bot_token,
    api_id=6,
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
)


# Get User Input
def kwairi(message):
    query = ""
    for i in message.command[1:]:
        query += f"{i} "
    return query

def convert_seconds(seconds): 
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# For Blacklist filter
blacks = []


# Ping


@app.on_message(
    filters.command(["ping"]) & filters.chat(sudo_chat_id) & ~filters.edited
)
async def ping(_, message):
    global blacks
    if message.from_user.id in blacks:
        await message.reply_text("You're Blacklisted, So Stop Spamming. NOOB NIBBA")
        return
    start_time = int(round(time.time() * 1000))
    m = await message.reply_text(".")
    end_time = int(round(time.time() * 1000))
    await m.edit(f"{end_time - start_time} ms")


# Start


@app.on_message(filters.command(["neutron"]) & ~filters.edited)
async def start(_, message: Message):
    global blacks
    if message.from_user.id in blacks:
        await message.reply_text("You're Blacklisted, So Stop Spamming. NOOB NIBBA")
        return
    await message.reply_text(
        "Hi!!! I am Neutron... I am ready to rock 😎🤘"
    )


# Help


@app.on_message(
    filters.command(["nhelp"]) & filters.chat(sudo_chat_id) & ~filters.edited
)
async def help(_, message: Message):
    global blacks
    if message.from_user.id in blacks:
        await message.reply_text("You're Blacklisted, So Stop Spamming. NOOB NIBBA")
        return
    await message.reply_text(
        """Currently These Commands Are Supported.
〄⊏**Check Bot**⊐〄

/neutron To Start The bot.
/end To Stop Any Playing Music.
/help To Show This Message.
/ping To Ping All Datacenters Of Telegram.

〄⊏**Play Song**⊐〄

/play <song_name> To Play A Song From Jiosaavn.
/telegram To Play A Song Directly From Telegram File.
/radio To Play Radio Continuosly.
/pornhub Try it yourself...

〄⊏**Owner commands**⊐〄

/black To Blacklist A User.
/white To Whitelist A User.
/users To Get A List Of Blacklisted Users.

NOTE: **Do Not Write** as /ping@neutron_music_bot... Just write `/ping`"""
    )


# Jiosaavn
# Global vars
s = None
m = None


@app.on_message(
    filters.command(["play"])
    & filters.chat(sudo_chat_id)
    & ~filters.edited
)
async def JioSaavn(_, message: Message):
    global blacks
    if message.from_user.id in blacks:
        await message.reply_text("You're Blacklisted, So Stop Spamming. NOOB NIBBA")
        return
    global s
    global m
    if len(message.command) < 2:
        await message.reply_text("/play requires an argument")
        return
    try:
        os.system("killall -9 mpv")
    except:
        pass
    try:
        await m.delete()
    except:
        pass
    try:
        await message.delete()
    except:
        pass

    query = kwairi(message)

    m = await message.reply_text(f"Searching for `{query}` on JioSaavn")
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://jiosaavnapi.bhadoo.uk/result/?query={query}"
        ) as resp:
            r = json.loads(await resp.text())

    sname = r[0]["song"]
    slink = r[0]["media_url"]
    ssingers = r[0]["singers"]
    sthumb = r[0]["image"]
    sduration = r[0]["duration"]
    sduration_converted = convert_seconds(int(sduration)) 
    await m.edit("Processing Thumbnail.")
    async with aiohttp.ClientSession() as session:
        async with session.get(sthumb) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    def changeImageSize(maxWidth, maxHeight, image):
        widthRatio = maxWidth / image.size[0]
        heightRatio = maxHeight / image.size[1]
        newWidth = int(widthRatio * image.size[0])
        newHeight = int(heightRatio * image.size[1])
        newImage = image.resize((newWidth, newHeight))
        return newImage

    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/JetBrainsMonoNL-Regular.ttf", 32)
    font2 = ImageFont.truetype("etc/abnes.ttf", 64)
    draw.text(
        (90, 350), f"NEUTRON BOT", (255, 255, 255), font=font2
    )
    draw.text(
        (190, 550), f"Title: {sname}", (255, 255, 255), font=font
    )
    draw.text(
        (190, 590), f"Artist: {ssingers}", (255, 255, 255), font=font
    )
    draw.text(
        (190, 630),
        f"Duration: {sduration_converted} Seconds",
        (255, 255, 255),
        font=font,
    )
    draw.text(
        (190, 670),
        f"Played By: {message.from_user.first_name}",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.system("rm temp.png")
    os.system("rm background.png")
    await m.delete()
    m = await message.reply_photo(
        caption=f"Playing `{sname}` Via Jiosaavn #music #neutron",
        photo="final.png",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "STOP", callback_data="end"
                    )
                ]
            ]
        ),
        parse_mode="markdown",
    )

    s = await asyncio.create_subprocess_shell(
        f"mpv {slink} --no-video",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await s.wait()
    await m.delete()


# Telegram Audio


@app.on_message(
    filters.command(["telegram"]) & filters.chat(sudo_chat_id) & ~filters.edited
)
async def tgplay(_, message: Message):
    global blacks
    if message.from_user.id in blacks:
        await message.reply_text("You're Blacklisted, So Stop Spamming. NOOB NIBBA")
        return
    global m
    global s
    if not message.reply_to_message:
        await message.reply_text("Reply To A Telegram Audio To Play It.")
        return
    try:
        await message.delete()
    except:
        pass
    try:
        await m.delete()
    except:
        pass
    try:
        os.system("killall -9 mpv")
    except:
        pass
    try:
        os.remove("audio.mp3")
    except:
        pass
    try:
        os.remove("downloads/audio.mp3")
    except:
        pass
    m = await message.reply_text("Downloading")
    await app.download_media(message.reply_to_message, file_name="audio.mp3")
    await m.edit(f"Playing `{message.reply_to_message.link}` via Telegram.")
    s = await asyncio.create_subprocess_shell(
        "mpv downloads/audio.mp3 --no-video",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await s.wait()
    await m.delete()
    os.system("rm downloads/audio.mp3")


# Radio


@app.on_message(
    filters.command(["radio"]) & filters.chat(sudo_chat_id) & ~filters.edited
)
async def radio(_, message: Message):
    global blacks
    if message.from_user.id in blacks:
        await message.reply_text("You're Blacklisted, So Stop Spamming.")
        return
    global m
    global s

    try:
        os.system("killall -9 mpv")
    except:
        pass
    try:
        await m.delete()
    except:
        pass
    try:
        await message.delete()
    except:
        pass

    try:
        os.remove("audio.mp3")
    except:
        pass
    m = await message.reply_text(
        f"Playing Radio\nRequested by - {message.from_user.mention}"
    )
    s = await asyncio.create_subprocess_shell(
        f"mpv {radio_link} --no-video",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await s.wait()
    await m.delete()


# End Music

async def getadmins(chat_id):
    admins = []
    async for i in app.iter_chat_members(chat_id, filter="administrators"):
        admins.append(i.user.id)
    return admins


@app.on_message(
    filters.command(["end"]) & filters.chat(sudo_chat_id) & ~filters.edited
)
async def end(_, message: Message):
    global blacks
    global m
    global s
    
    if message.from_user.id in blacks:
        await message.reply_text("You're Blacklisted, So Stop Spamming.")
        return
    list_of_admins = await getadmins(message.chat.id)
    if message.from_user.id not in list_of_admins:
        await message.reply_text("Dear... You are not an admin... SO GET THE FCK OUTTA HERE AND DONT STOP ME... Only admins and Rashh can stop me...")
        return
    try:
        os.remove("audio.mp3")
    except:
        pass

    try:
        await message.delete()
    except:
        pass
    try:
        os.system("killall -9 mpv")
    except:
        pass
    try:
        s.terminate()
    except:
        pass
    try:
        await m.delete()
    except:
        pass

    await message.reply_text(
        f"{message.from_user.mention} Stopped The Music."
    )


@app.on_callback_query(filters.regex("end"))
async def end_callback(_, CallbackQuery):
    list_of_admins = await getadmins(CallbackQuery.message.chat.id)
    if CallbackQuery.from_user.id not in list_of_admins:
        await app.answer_callback_query(
            CallbackQuery.id, "Well, you're not admin, SO YOU CAN'T STOP"
            + " ME, HAH!, how about i ban you?", show_alert=True)
        return
    global blacks
    global m
    global s
    chat_id = int(CallbackQuery.message.chat.id)
    if CallbackQuery.from_user.id in blacks:
        return
    try:
        os.remove("audio.mp3")
    except:
        pass
    try:
        os.system("killall -9 mpv")
    except:
        pass
    try:
        s.terminate()
    except:
        pass
    try:
        await m.delete()
    except:
        pass
    await app.send_message(
        chat_id,
        f"{CallbackQuery.from_user.mention} - {CallbackQuery.from_user.id} Stopped The Music.",
    )


# Ban


@app.on_message(
    filters.command(["black"]) & filters.chat(sudo_chat_id) & ~filters.edited
)
async def blacklist(_, message: Message):
    global blacks
    if message.from_user.id != owner_id:
        await message.reply_text("Only owner can blacklist users.")
        return
    if not message.reply_to_message:
        await message.reply_text(
            "Reply to a message with /black to blacklist a user."
        )
        return
    if message.reply_to_message.from_user.id in blacks:
        await message.reply_text("This user is already blacklisted.")
        return
    blacks.append(message.reply_to_message.from_user.id)
    await message.reply_text(
        f"Blacklisted {message.reply_to_message.from_user.mention}"
    )


# Unban


@app.on_message(
    filters.command(["white"]) & filters.chat(sudo_chat_id) & ~filters.edited
)
async def whitelist(_, message: Message):
    global blacks
    if message.from_user.id != owner_id:
        await message.reply_text("Only owner can whitelist users.")
        return
    if not message.reply_to_message:
        await message.reply_text("Reply to a message to whitelist a user.")
        return
    if message.reply_to_message.from_user.id in blacks:
        blacks.remove(message.reply_to_message.from_user.id)
        await message.reply_text(
            f"Whitelisted {message.reply_to_message.from_user.mention}"
        )
    else:
        await message.reply_text("This user is already whitelisted.")


# Blacklisted users


@app.on_message(
    filters.command(["users"]) & filters.chat(sudo_chat_id) & ~filters.edited
)
async def users(client, message: Message):
    global blacks
    if message.from_user.id in blacks:
        await message.reply_text("You're Blacklisted, So Stop Spamming.")
        return
    output = "Blacklisted Users:\n"
    n = 1
    for i in blacks:
        usern = (await client.get_users(i)).mention
        output += f"{n}. {usern}\n"
        n += 1
    if len(blacks) == 0:
        await message.reply_text("No Users Are Blacklisted")
        return
    await message.reply_text(output)

#PH
@app.on_message(
    filters.command(["pornhub"]) & filters.chat(sudo_chat_id) & ~filters.edited
)
async def pornhub(_, message: Message):
    global blacks
    if message.from_user.id in blacks:
        await message.reply_text("Abe bhencho.... Music bot hu... Tharki bsdk😡")
        return
    await message.reply_text(
        """Abe bhencho.... Music bot hu... Tharki bsdk😡"""
    )


#DONE!!!!!!!!1
print("Neutron2 Bot Starting...")
app.run()

from aiogram import Bot, types
from .crawler import Crawler
from os import environ


if "BOT_TOKEN" not in environ:
    raise ValueError("No BOT_TOKEN in environment")

if "AUTH_LOGIN" not in environ or "AUTH_PASSWORD" not in environ:
    raise ValueError("Auth creds doesnt set")

if "SEND_GROUP" not in environ:
    raise ValueError("Send group undefined")

SEND_GROUP_ID = environ.get("SEND_GROUP")


async def bot_loop():
    bot = Bot(token=environ.get("BOT_TOKEN"))
    crawler = Crawler(
        pocket_login=environ.get("AUTH_LOGIN"), pocket_pass=environ.get("AUTH_PASSWORD")
    )
    crawler.login_pocket()
    while True:
        data = crawler.step()
        call_text = "UP" if data["call"] else "DOWN"
        await bot.send_message(
            chat_id=SEND_GROUP_ID,
            text=f"pair: {data['pair']}\ntime: "
            + f"{data['time']}sec\ncall: {call_text}",
        )
        await bot.send_media_group(
            chat_id=SEND_GROUP_ID,
            media=[
                types.InputFile("output/screenshots/screen1.png"),
                types.InputFile("output/screenshots/screen2.png"),
            ],
        )

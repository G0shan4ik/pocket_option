from pocket_option.bot import bot_loop
from asyncio import run


def start():
    run(bot_loop())

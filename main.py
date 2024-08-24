from pocket_option.bot import bot_loop
from asyncio import run


def start():
    """
    Launches a telegram bot
    """
    run(bot_loop())

import asyncio
from os import getenv
from dotenv import load_dotenv

from disnake import Intents

from core.bot import Bot

def main():
    bot = Bot(intents=Intents.all())

    try:
        load_dotenv()
        bot.run(getenv("TOKEN"))
    except KeyboardInterrupt:
        asyncio.get_event_loop().close()

if __name__ == "__main__":
    main()
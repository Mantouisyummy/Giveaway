import asyncio
import re
import os

from disnake import Message, Game, Status
from disnake.abc import Messageable
from disnake.ext.commands import InteractionBot

class Bot(InteractionBot):
    def __init__(self,  *args, **kwargs):
        """
        :param conversation: Conversation instance
        :param args: args
        :param kwargs: kwargs
        """
        super().__init__(*args, **kwargs)


    async def on_ready(self):
        await self.change_presence(activity=Game("V1.0 開源by.饅頭"), status=Status.online)
        for file in os.listdir('./cogs'):  # 抓取所有cog資料夾裡的檔案
            if file.endswith('.py'):  # 判斷檔案是否是python檔
                try:
                    # 載入cog,[:-3]是字串切片,為了把.py消除
                    self.load_extension(f'cogs.{file[:-3]}')
                    print(f'✅ 已加載 {file}')
                except Exception as error:  # 如果cog未正確載入
                    print(f'❌ {file} 發生錯誤  {error}')

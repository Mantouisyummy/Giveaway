from disnake.ext import commands
from disnake import ApplicationCommandInteraction,OptionType,Option, ButtonStyle, Embed, Colour, MessageInteraction
from disnake.ui import Button
from core.giveaway import Giveaway
import disnake
import asyncio
import datetime
import json
import os


class Cog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.giveaway = Giveaway() 
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Giveaway Ready!")

    @commands.Cog.listener()
    async def on_message_interaction(self, interaction:MessageInteraction):
        if interaction.data.custom_id == f"giveaway_join_{interaction.channel.id}":
            with open(f"./database/{interaction.message.id}.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            if interaction.user.id not in data['join_list']:
                data['join_list'].append(interaction.user.id)
                with open(f"./database/{interaction.message.id}.json", "w", encoding="utf-8") as f:
                    json.dump(data, f)

                await self.giveaway.edit(interaction=interaction, message_id=interaction.message.id)
            else:
                await interaction.response.send_message("你已經參加了!",ephemeral=True)

        if interaction.data.custom_id == f"giveaway_list_{interaction.channel.id}":
            with open(f"./database/{interaction.message.id}.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                if data['join_list'] == []:  # 如果list為空時
                    embed = disnake.Embed(title="❌ | 沒有任何人參加", colour=Colour.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    users = []
                    for user_id in data['join_list']:
                        user = self.bot.get_user(user_id)
                        if user is not None:
                            users.append(user.name)
                    embed = disnake.Embed(
                        title="參加名單",
                        description=", ".join(users),
                        colour=Colour.random(),
                    )  # 顯示名單
                    await interaction.response.send_message(embed=embed, ephemeral=True)


    @commands.slash_command(name="giveaway")
    async def sub_giveaway(self, interaction: ApplicationCommandInteraction):
        pass

    @sub_giveaway.sub_command(name="start",description="開始一個新的抽獎",options=[
        Option(name="prize",description="抽獎物",type=OptionType.string,required=True),
        Option(name="text",description="訊息內容",type=OptionType.string,required=True),
        Option(name="winners",description="抽出的數量",type=OptionType.integer,required=True),
        Option(name="day",description="天數",type=OptionType.integer,required=False),
        Option(name="hour",description="小時",type=OptionType.integer,required=False),
        Option(name="min",description="分鐘",type=OptionType.integer,required=False),
        Option(name="sec",description="秒數",type=OptionType.integer,required=False)])

    async def start(self, interaction: ApplicationCommandInteraction, prize:str, text:str, winners:int, day:int = 0, hour:int = 0, min:int = 0, sec:int = 0):
        total_seconds = day * 86400 + hour * 3600 + min * 60 + sec
        delta = datetime.timedelta(seconds=total_seconds)
        start_time = datetime.datetime.now() + delta
        timestamp = start_time.timestamp()

        await interaction.response.send_message("發送成功!",ephemeral=True,delete_after=3)

        components = [
            Button(label="參加",custom_id=f"giveaway_join_{interaction.channel.id}",style=ButtonStyle.green, emoji="🎉"),
            Button(label="查看名單",custom_id=f"giveaway_list_{interaction.channel.id}",style=ButtonStyle.gray)
        ]

        embed = Embed(title=prize,description=f"抽獎資訊：{text}\n獲獎人數：{winners}\n結束時間：<t:{int(timestamp)}:R>\n參加人數：0",colour=Colour.random())

        message = await interaction.channel.send(embed=embed,components=components)
        await self.giveaway.start(bot=self.bot, message_id=message.id, channel_id=interaction.channel.id,item=prize, text=text, winners=winners, timestamp=timestamp, total=total_seconds)

    @sub_giveaway.sub_command(name="reroll",description="重新選擇一個抽獎的中獎者",options=[Option(name="message_id",description="輸入抽獎訊息之ID",type=OptionType.string,required=True)])
    async def reroll(self, interaction: ApplicationCommandInteraction,message_id:int):
        if not os.path.exists(f"./database/{message_id}.json"):
            await interaction.response.send_message(":x: 找不到這個抽獎訊息!",ephemeral=True)
        else:
            await interaction.response.send_message("發送成功!",ephemeral=True,delete_after=3)
            await self.giveaway.reroll(bot=self.bot, message_id=message_id)


def setup(bot):
    bot.add_cog(Cog(bot))
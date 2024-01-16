import asyncio
import os
import json
import random
from disnake import MessageInteraction, Embed, Colour, Message, ButtonStyle
from disnake.ui import Button
from disnake.ext.commands import Bot


class Giveaway:
    def __init__(self) -> None:
        pass

    async def start(
        self,
        bot: Bot,
        message_id: int,
        channel_id: int,
        item: str,
        text: str,
        winners: int,
        timestamp: int,
        total: int,
    ):
        with open(f"./database/{message_id}.json", "w", encoding="utf-8") as f:
            temp = {
                "text": text,
                "item": item,
                "winners": winners,
                "timestamp": timestamp,
                "join_list": [],
                "channel_id": channel_id,
            }
            json.dump(temp, f)

        await asyncio.sleep(total - 2)

        await self.end(bot=bot, message_id=message_id, winners=winners)

        return True

    async def reroll(self, bot: Bot, message_id: int):
        with open(f"./database/{message_id}.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        channel = bot.get_channel(data["channel_id"])
        msg: Message = await channel.fetch_message(message_id)

        components = [
            Button(
                label="參加",
                custom_id=f"giveaway_join_{channel.id}",
                style=ButtonStyle.green,
                emoji="🎉",
                disabled=True,
            ),
            Button(
                label="查看名單",
                custom_id=f"giveaway_list_{channel.id}",
                style=ButtonStyle.gray,
            ),
        ]

        join_list = data["join_list"]
        if join_list != []:
            winner_list = []
            winners = data["winners"]
            winner = random.sample(join_list, k=winners)
            for user_id in winner:
                user = bot.get_user(user_id)
                winner_list.append(user.mention)
            winner_string = " 和 ".join(winner_list)
            embed = Embed(
                title="🎊 重新抽獎! 🎊",
                description=f"{winner_string} 中了 {data['item']}！",
                colour=Colour.green(),
            )
            embed.set_footer(text="• 重新選擇中獎者請使用/giveaway reroll")
            msg_embed = Embed(
                title="🎊 重新抽獎! 🎊",
                description=f"中獎者: {winner_string}",
                colour=Colour.random(),
            )
            await channel.send(content=f"恭喜 {winner_string} :tada:", embed=embed)
            await msg.edit(embed=msg_embed, components=components)
        else:
            embed = Embed(title="沒有人參加本次的抽獎!", colour=Colour.red())
            msg_embed = Embed(
                title="🎊 重新抽獎! 🎊", description=f"中獎者: 無", colour=Colour.random()
            )
            await channel.send(embed=embed)
            await msg.edit(embed=msg_embed, components=components)

    async def end(self, bot: Bot, message_id: int, winners: int):
        with open(f"./database/{message_id}.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        channel = bot.get_channel(data["channel_id"])
        msg = await channel.fetch_message(message_id)

        components = [
            Button(
                label="參加",
                custom_id=f"giveaway_join_{channel.id}",
                style=ButtonStyle.green,
                emoji="🎉",
                disabled=True,
            ),
            Button(
                label="查看名單",
                custom_id=f"giveaway_list_{channel.id}",
                style=ButtonStyle.gray,
            ),
        ]

        join_list = data["join_list"]
        if join_list != []:
            winner_list = []
            winner = random.sample(join_list, k=winners)
            for user_id in winner:
                user = bot.get_user(user_id)
                winner_list.append(user.mention)
            winner_string = " 和 ".join(winner_list)
            embed = Embed(
                title="🎊 抽獎已結束! 🎊",
                description=f"{winner_string} 中了 {data['item']}！",
                colour=Colour.green(),
            )
            embed.set_footer(text="• 重新選擇中獎者請使用/giveaway reroll")
            msg_embed = Embed(
                title="🎊 抽獎已結束! 🎊",
                description=f"中獎者: {winner_string}",
                colour=Colour.random(),
            )
            await channel.send(content=f"恭喜 {winner_string} :tada:", embed=embed)
            await msg.edit(embed=msg_embed, components=components)

        else:
            embed = Embed(title="沒有人參加本次的抽獎!", colour=Colour.red())
            msg_embed = Embed(
                title="🎊 抽獎已結束! 🎊", description=f"中獎者: 無", colour=Colour.random()
            )
            await channel.send(embed=embed)
            await msg.edit(embed=msg_embed, components=components)

    async def edit(self, interaction: MessageInteraction, message_id: int):
        with open(f"./database/{message_id}.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        timestamp = data["timestamp"]
        item = data["item"]
        winners = data["winners"]
        join_list = data["join_list"]
        text = data["text"]
        embed = Embed(
            title=item,
            description=f"抽獎資訊：{text}\n獲獎人數：{winners}\n結束時間：<t:{int(timestamp)}:R>\n參加人數：{len(join_list)}",
            colour=Colour.random(),
        )
        await interaction.response.edit_message(embed=embed)
        return True

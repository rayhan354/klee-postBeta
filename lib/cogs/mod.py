from asyncio import sleep
from datetime import datetime, timedelta
from re import search
from typing import Optional

from discord import Embed, Member
from discord.ext.commands import Cog, Greedy
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, bot_has_permissions

from ..db import db

# ^^^ I don't f ing know which exactly should I import

from better_profanity import profanity

profanity.load_censor_words_from_file("./data/profanity.txt")

kataKasar = 758415783176044605

class Mod(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="larang", aliases=["kasar", "bahaya"])
    @has_permissions(manage_guild=True)
    async def add_profanity(self, ctx, *words):
        with open("./data/profanity.txt", "a", encoding="utf-8") as f:
            f.write("".join([f"{w}\n" for w in words]))

        profanity.load_censor_words_from_file("./data/profanity.txt")
        await ctx.send(str(*words)+" adalah kata terlarang")

    @command(name="delarang", aliases=["delkasar", "delbahaya"])
    @has_permissions(manage_guild=True)
    async def remove_profanity(self, ctx, *words):
        with open("./data/profanity.txt", "r", encoding="utf-8") as f:
            stored = [w.strip() for w in f.readlines()]

        with open("./data/profanity.txt", "w", encoding="utf-8") as f:
            f.write("".join([f"{w}\n" for w in stored if w not in words]))

        profanity.load_censor_words_from_file("./data/profanity.txt")
        await ctx.send(str(*words)+" bukan lagi kata terlarang")

    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if profanity.contains_profanity(message.content):
                await message.delete()
                await message.channel.send(f"Traveler {message.author.mention}, kau tidak boleh berkata seperti itu!!!")
                await self.bot.get_channel(kataKasar).send(f"""{message.author.mention} menggunakan kata terlarang dalam chatnya:
```
{str(message.content)}
```""")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("mod")

def setup(bot):
	bot.add_cog(Mod(bot))
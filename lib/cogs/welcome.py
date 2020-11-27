from asyncio import sleep
from datetime import datetime
from glob import glob
from discord.errors import HTTPException, Forbidden

import os
import discord

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed, File, DMChannel
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown)
from discord.ext.commands import when_mentioned_or, command, has_permissions
# ^^^ idk which exactly to import

from discord import Forbidden
from discord.ext.commands import Cog
from discord.ext.commands import command
import random
from random import randint

from ..db import db

welcomePage = 750146707895091211
rules = 691558363393294338
general = 691557707269931088

Klee = discord.File("pics/klee.png", filename="klee.png")
PaimonCute = discord.File("pics/paimon.png", filename="paimon.png")
KleePic = discord.File("pics/Klee_Thumb.png", filename="Klee_Thumb.png")
rayhan352 = 606013036385271818

class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = None

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")

    @Cog.listener()
    async def on_member_join(self, member):
        # if member.id == rayhan352:
        #     pass
        # else:
            db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
            embed = Embed(title=f"""Selamat datang, {member.display_name}
＼(≧▽≦)／""", description=("Jangan lupa baca <#" + str(rules) +f"""> terlebih dahulu.
Semoga betah ya~~"""), color=discord.Colour.from_rgb(r=randint(0, 255), g=randint(0, 255), b=randint(0, 255)), timestamp=datetime.utcnow())
            embed.set_author(name="Genshin Impact Indonesia")
            embed.set_footer(text="Klee v0.9.6")
            embed.set_thumbnail(url= "https://cdn.glitch.com/9b304f27-f8a2-418f-9a53-7e1f301959f2%2FWelcome.png?v=1598041284654")
            await self.bot.get_channel(welcomePage).send(embed=embed)

    @Cog.listener()
    async def on_member_remove(self, member):
        if member.id == rayhan352:
            pass
        else:
            db.execute("DELETE FROM exp WHERE UserID = ?", member.id)
            await self.bot.get_channel(welcomePage).send(f"Yah... {member.display_name} telah keluar. Selamat tinggal, Traveler")


def setup(bot):
    bot.add_cog(Welcome(bot))

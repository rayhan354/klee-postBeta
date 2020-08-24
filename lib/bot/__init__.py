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
from ..db import db

Klee = discord.File("pics/klee.png", filename="klee.png")
PaimonCute = discord.File("pics/paimon.gif", filename="paimon.gif")
KleePic = discord.File("pics/Klee_Thumb.png", filename="Klee_Thumb.png")
PREFIX = "klee "
PREFIX = (PREFIX, PREFIX.capitalize(), PREFIX.upper())
OWNER_IDS = [326730266531856394]

COGS = [path.split(os.sep)[-1][:-3] for path in glob("./lib/cogs/*.py")] #going to the cogs directory, and returns the name of any cog inside em
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

dev_area = 691557707269931088
Server = 691557706846306385
peraturanumum = 691558363393294338

class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)
    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog ready")
    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready= False
        self.cogs_ready = Ready()

        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} cog loaded")
        print("setup complete")
    
    def run(self, version):
        self.VERSION = version

        print("running setup")
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()
        
        print("running bot...")
        super().run(self.TOKEN, reconnect = True)
    
    async def rules_reminder(self):
        channel = self.get_channel(dev_area)
        await channel.send("Jangan lupa untuk menaati peraturan yang ada di <#" + str(peraturanumum) +"> ya ヽ(^o^)ノ")

    async def on_connect(self):
        print("bot connected")

    async def on_disconnect(self):
        print("bot disconnected")
    
    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Ahh, aku tidak paham apa maksudmu...")

        await self.stdout.send("Error")

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("Missing Argument/s")

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f"Sabar ya, Jangan buru-buru. Coba lagi dalam {exc.retry_after:,.2f} detik")

        elif hasattr(exc, "original"):
            # if isinstance(exc.original, HTTPException):
            #     await ctx.send("Tidak dapat mengirim pesan")

            if isinstance(exc.original, Forbidden):
                await ctx.send("Aku tidak boleh melakukan itu karena aku ingin menjadi anak baik.")

            else:
                raise exc.original

        else:
            raise exc

    async def notused(self):
        self.get_channel(dev_area)
        embed = Embed(title="""Selamat datang di Genshin Impact Indonesia ヾ(＠⌒▽⌒＠)ﾉ""", description="Klee siap melayani kamu disini", colour=0x00FFFF, timestamp=datetime.utcnow())
        embed.set_author(name="Genshin Impact Indonesia", icon_url=self.guild.icon_url)
        embed.set_footer(text="embed by rayhan354")
        embed.set_image(url="attachment://klee.png")
        await self.stdout.send(embed=embed, file=Klee)


    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(Server)
            self.stdout = self.get_channel(dev_area) #genshin_chat
            self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=0, minute=0, second=0)) # 
            self.scheduler.start()

            while not self.cogs_ready.all_ready():
                await sleep(0.5)
            
            await self.stdout.send("Halo semua, Klee siap melayani kalian")
            self.ready = True
            print("bot ready")
        else:
            print("bot reconnected")

    async def on_message(self, message):
        if not message.author.bot:  #ignore bot messages
            message.content = message.content.lower()
            await self.process_commands(message)


bot = Bot()

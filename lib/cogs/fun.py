from random import choice, randint
from typing import Optional

import random

from discord import Member, Embed
from aiohttp import request
from discord.errors import HTTPException
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown
from discord.ext.commands import BadArgument
class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="cmd", aliases=["command","c"], hidden=True) # Basics of Running command
    async def somecommand(self, ctx):
        pass
    
    @command(name="hello", aliases=["hi", "hai", "halo", "sapa"]) # saying hello command 
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hai','Haloooo', 'Yo', 'Yaahooo~~~'))} {ctx.author.mention}!")
        await ctx.message.delete()

    @command(name="dice", aliases=["roll"]) # roll dice ( contoh : klee roll 3 berarti kyk ngeroll 3 dadu )
    async def roll_dice(self, ctx, die_string: str):
        dice = (int(die_string))
        rolls = [randint(1, 6) for i in range(dice)]
        if rolls == []:
            await ctx.send(f"Garing lu!!!")
        elif len(rolls) == 1:
            await ctx.send(f"Hasil lemparan dadu oleh {ctx.author.display_name} adalah "+str(rolls[0]))
        elif 400 > len(rolls) > 5:
            await ctx.send(f"{ctx.author.display_name}, Kau hanya boleh melempar hingga 5 dadu saja.")
        elif len(rolls) >= 400:
            await ctx.send("Kyaaaaaa...... Banyak banget dadu nya. Aku tidak mau menghitung dadu sebanyak itu!!!")
        else:
            await ctx.send(f"Hasil lemparan dadu oleh {ctx.author.display_name} adalah " + " + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")
    
    @roll_dice.error
    async def roll_dice_error(self, ctx, exc):
        if isinstance(exc.original, HTTPException):
            await ctx.send("Kyaaaaaa...... Banyak banget dadu nya. Aku tidak bisa menghitung dadu sebanyak itu")

    @command(name="slap", aliases=["hit","tampol","tampar","gaplok", "tendang"])
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "pengen aja"):
        reason = reason.capitalize()
        reaction = ["memukul","menampar","menampol","menggaplok", "menendang"]
        await ctx.message.delete()
        await ctx.send(f"""Klee {random.choice(reaction)} {member.mention}
Alasan : {reason}""") # untuk {ctx.author.name}!

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.message.delete()
            await ctx.send("Aku tidak bisa melakukannya.")


    @command(name ="echo", aliases=["say","chat"])
    async def echo_message(self, ctx, *, message):
        message = message.capitalize()
        await ctx.message.delete()
        await ctx.send(message)
    
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")



def setup(bot):
    bot.add_cog(Fun(bot))
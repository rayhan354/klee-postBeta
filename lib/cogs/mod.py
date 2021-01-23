from asyncio import sleep
from datetime import datetime, timedelta
from re import search
from typing import Optional

import time

from discord import Embed, Member, NotFound, Object
from discord.utils import find 
from discord.ext.commands import Cog, Greedy, Converter
from discord.ext.commands import CheckFailure, BadArgument
from discord.ext.commands import command, has_permissions, bot_has_permissions

from ..db import db

# ^^^ I don't f ing know which exactly should I import

from better_profanity import profanity

profanity.load_censor_words_from_file("./data/profanity.txt")

kataKasar = 802457848311316490
joinLog = 802460205895254036
mutedRole = 763413977971032105
unmutedRole = 691558060820529162
general = 691557707269931088


class Mod(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="kick", aliases=["tendang"])
    @bot_has_permissions(kick_members=True)
    @has_permissions(manage_guild=True)
    async def kick_members(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "(Tidak tertulis)"):
        if not len(targets):
            await ctx.send("Gunakan `klee <kick|ban> <mention member>` untuk melakukan perintah tersebut")

        else:
            for target in targets:
                if not target.guild_permissions.administrator:
                    await target.kick(reason=reason)

                    embed = Embed(title=f"Traveler [ {target.display_name} ] **KICKED!!**",
                                  colour=0xFFFF00,
                                  timestamp=datetime.utcnow())

                    embed.set_thumbnail(url="https://cdn.glitch.com/9b304f27-f8a2-418f-9a53-7e1f301959f2%2F286a7dbcc956891335fa1df61fc16b5e_3065080245373623875.png?v=1602251899571")

                    fields = [("Member", f"{target.name}", False),
                              ("Ditendang oleh", ctx.author.display_name , False),
                              ("Sebab", reason , False)]
                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)

                    await self.welcome_channel.send(embed=embed)
                    await ctx.send(f"{target.display_name} berhasil di kick", delete_after = 30)
                else:
                    await ctx.send(f"Apa maksudmu melakukan itu? Klee tidak mau melakukannya!!!")

    @command(name="ban", aliases=["buang"])
    @bot_has_permissions(ban_members=True)
    @has_permissions(manage_guild=True)
    async def ban_members(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "(Tidak tertulis)"):
        if not len(targets):
            await ctx.send("Gunakan `klee <kick|ban> <mention member>` untuk melakukan perintah tersebut")

        else:
            for target in targets:
                if not target.guild_permissions.administrator:
                    await target.ban(reason=reason)

                    embed = Embed(title=f"Traveler [ {target.display_name} ] **BANNED!!!**",
                                  colour=0xFF0000,
                                  timestamp=datetime.utcnow())

                    embed.set_thumbnail(url="https://cdn.glitch.com/9b304f27-f8a2-418f-9a53-7e1f301959f2%2F286a7dbcc956891335fa1df61fc16b5e_3065080245373623875.png?v=1602251899571")

                    fields = [("Member", f"{target.name}", False),
                              ("Ditendang oleh", ctx.author.display_name , False),
                              ("Sebab", reason , False)]
                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)

                    await self.welcome_channel.send(embed=embed)
                    await ctx.send(f"{target.display_name} berhasil di ban", delete_after = 30)
                
                else:
                    await ctx.send(f"Apa maksudmu melakukan itu? Klee tidak mau melakukannya!!!")

    @command(name="mute")
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_guild=True)
    async def mute_members(self, ctx, target: Member, *,
                           reason: Optional[str] = "Tidak disebutkan"):
        await target.edit(roles=[self.mute_role])
        await ctx.send(f"Oke. Sementara {target.display_name} tidak boleh chat ya")

    @command(name="unmute")
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_guild=True)
    async def unmute_members(self, ctx, target: Member, *, reason: Optional[str] = "Tidak ditulis"):
        await target.edit(roles=[self.unmute_role])
        await ctx.send(f"Ok {target.display_name} boleh chat kembali")

    @command(name="larang", aliases=["kasar", "bahaya"])
    @has_permissions(manage_guild=True)
    async def add_profanity(self, ctx, *words):
        if words == "('',)":
            pass
        else:
            with open("./data/profanity.txt", "a", encoding="utf-8") as f:
                f.write("".join([f"{w}\n" for w in words]))

            profanity.load_censor_words_from_file("./data/profanity.txt")
            await ctx.send(str(*words)+" adalah kata terlarang")

    @command(name="delarang", aliases=["delkasar", "delbahaya"])
    @has_permissions(manage_guild=True)
    async def remove_profanity(self, ctx, *words):
        if words == "('',)":
            pass
        else:
            with open("./data/profanity.txt", "r", encoding="utf-8") as f:
                stored = [w.strip() for w in f.readlines()]

            with open("./data/profanity.txt", "w", encoding="utf-8") as f:
                f.write("".join([f"{w}\n" for w in stored if w not in words]))

            profanity.load_censor_words_from_file("./data/profanity.txt")
            await ctx.send(str(*words)+" bukan lagi kata terlarang")

    @Cog.listener()
    async def on_message(self, message):
        def _check(m):
            return (m.author == message.author
                    and len(m.author)
                    and (datetime.utcnow()-m.created_at).seconds < 60)

        if not message.author.bot:
            if profanity.contains_profanity(message.content):
                if message.content.startswith("klee larang"):
                    pass
                else:
                    await message.delete()
                    await message.channel.send(f"Traveler {message.author.mention}, kau tidak boleh berkata seperti itu!!!", delete_after = 10)
                    await self.bot.get_channel(kataKasar).send(f"""{message.author.mention} menggunakan kata terlarang dalam chatnya:
```
{str(message.content)}
```""")
            elif len(list(filter(lambda m: _check(m), self.bot.cached_messages))) >= 3:
                await message.channel.send("Don't spam mentions!", delete_after=10)

    @command(name="clear", aliases=["hapus"])
    @has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, targets: Greedy[Member], limit: Optional[int] = 100):
        def _check(message):
            return not len(targets) or message.author in targets

        if 0 < limit <= 100:
            with ctx.channel.typing():
                await ctx.message.delete()
                deleted = await ctx.channel.purge(limit=limit,
                                                  check=_check)

                await ctx.send(f"{len(deleted):,} pesan telah terhapus.", delete_after=5)

        else:
            await ctx.send("Klee tidak mau menghapus pesan terlalu banyak.")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.welcome_channel = self.bot.get_channel(joinLog)
            self.mute_role = self.bot.guild.get_role(mutedRole)
            self.unmute_role = self.bot.guild.get_role(unmutedRole)
            self.unmuted_yay = self.bot.get_channel(general)
            self.bot.cogs_ready.ready_up("mod")

def setup(bot):
	bot.add_cog(Mod(bot))
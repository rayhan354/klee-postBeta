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

from datetime import datetime

from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command

roleUpdate = 820630478578515988
botInteract = 820630385389600805
messageUpdate = 820630385389600805
avatarUpdate = 820630452003405834
userUpdate = 820630576901783592


class Log(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.role_update = self.bot.get_channel(roleUpdate)
			self.message_update = self.bot.get_channel(messageUpdate)
			self.avatar_update = self.bot.get_channel(avatarUpdate)
			self.user_update = self.bot.get_channel(userUpdate)
			self.bot.cogs_ready.ready_up("log")

	@Cog.listener()
	async def on_user_update(self, before, after):
		if before.name != after.name:
			embed = Embed(title="Username change",
						  colour=after.colour,
						  timestamp=datetime.utcnow())

			fields = [("Before", before.name, False),
					  ("After", after.name, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			await self.user_update.send(embed=embed)

		if before.discriminator != after.discriminator:
			embed = Embed(title="Discord tag change",
						  description= f"{before.display_name}",
						  colour=after.colour,
						  timestamp=datetime.utcnow())

			fields = [("Before", before.discriminator, False),
					  ("After", after.discriminator, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			await self.user_update.send(embed=embed)

		if before.avatar_url != after.avatar_url:
			embed = Embed(title=f"Avatar change ( {before.display_name} )",
						  description="New image is below, old is on right.",
						  colour=self.avatar_update.guild.get_member(after.id).colour,
						  timestamp=datetime.utcnow())

			embed.set_thumbnail(url=before.avatar_url)
			embed.set_image(url=after.avatar_url)

			await self.avatar_update.send(embed=embed)

	@Cog.listener()
	async def on_member_update(self, before, after):
		if before.display_name != after.display_name:
			embed = Embed(title="Nickname change",
						  colour=after.colour,
						  timestamp=datetime.utcnow())

			fields = [("Before", before.display_name, False),
					  ("After", after.display_name, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			await self.user_update.send(embed=embed)

		elif before.roles != after.roles:
			embed = Embed(title="Role updates",
						  description=f"{before.display_name}",
						  colour=after.colour,
						  timestamp=datetime.utcnow())

			fields = [("Before", ", ".join([r.mention for r in before.roles]), False),
					  ("After", ", ".join([r.mention for r in after.roles]), False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			await self.role_update.send(embed=embed)

	@Cog.listener()
	async def on_message_edit(self, before, after):
		if not after.author.bot:
			if before.content != after.content:
				embed = Embed(title="Message edit",
							  description=f"{after.author.display_name}",
							  colour=after.author.colour,
							  timestamp=datetime.utcnow())

				fields = [("Before", before.content, False),
						  ("After", after.content, False)]

				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)

				await self.message_update.send(embed=embed)

	@Cog.listener()
	async def on_message_delete(self, message):
		if not message.author.bot:
			if not message.attachments:
				embed = Embed(title="Message delete",
						  description=f"{message.author.display_name}.",
						  colour=message.author.colour,
						  timestamp=datetime.utcnow())

				fields = [("Content", message.content, False)]

				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)

				await self.message_update.send(embed=embed)

def setup(bot):
	bot.add_cog(Log(bot))

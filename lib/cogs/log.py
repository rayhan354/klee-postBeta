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

<<<<<<< Updated upstream
devArea = 743105610526097479
botInteract = 743100499393380426
=======
roleUpdate = 802456094529421363
botInteract = 781432485711446017
messageUpdate = 802456919293165569
avatarUpdate = 802457010707628032
userUpdate = 802457089103757353

rayhan352 = 606013036385271818
>>>>>>> Stashed changes

class Log(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.log_channel = self.bot.get_channel(devArea)
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

			await self.log_channel.send(embed=embed)

		if before.discriminator != after.discriminator:
			embed = Embed(title="Discriminator change",
						  colour=after.colour,
						  timestamp=datetime.utcnow())

			fields = [("Before", before.discriminator, False),
					  ("After", after.discriminator, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			await self.log_channel.send(embed=embed)

		if before.avatar_url != after.avatar_url:
			embed = Embed(title=f"Avatar change ( {before.display_name} )",
						  description="New image is below, old is on right.",
						  colour=self.log_channel.guild.get_member(after.id).colour,
						  timestamp=datetime.utcnow())

			embed.set_thumbnail(url=before.avatar_url)
			embed.set_image(url=after.avatar_url)

			await self.log_channel.send(embed=embed)

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

			await self.log_channel.send(embed=embed)

		elif before.roles != after.roles:
			embed = Embed(title="Role updates",
						  description=f"{before.display_name}",
						  colour=after.colour,
						  timestamp=datetime.utcnow())

			fields = [("Before", ", ".join([r.mention for r in before.roles]), False),
					  ("After", ", ".join([r.mention for r in after.roles]), False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			await self.log_channel.send(embed=embed)

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

				await self.log_channel.send(embed=embed)

	@Cog.listener()
	async def on_message_delete(self, message):
		if not message.author.bot:
			embed = Embed(title="Message delete",
						  description=f"{message.author.display_name}.",
						  colour=message.author.colour,
						  timestamp=datetime.utcnow())

			fields = [("Content", message.content, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			await self.log_channel.send(embed=embed)


def setup(bot):
	bot.add_cog(Log(bot))

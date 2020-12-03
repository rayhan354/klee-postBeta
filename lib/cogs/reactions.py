from discord.ext.commands import Cog

assignRole = 743333276826992672
three = 783731983858532392
four = 783731978851450930
five = 783731973591793685
six = 783731969019740180
seven = 783731599304818759
eight = 783731729105289287
helper = 778916278005399564
guider = 778916442493419521
traveler = 691558060820529162
asd = 0
miner = 784015529987932171

class Reactions(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.numbers = {
                "🌻": self.bot.guild.get_role(three), # WL3
                "4️⃣": self.bot.guild.get_role(four), # WL4
                "5️⃣": self.bot.guild.get_role(five), # WL5
                "6️⃣": self.bot.guild.get_role(six), # WL6
                "7️⃣": self.bot.guild.get_role(seven), # WL7
                "8️⃣": self.bot.guild.get_role(eight) # WL8
                }
            self.guidance = {
                "🤝": self.bot.guild.get_role(helper),
                "👨‍🏫": self.bot.guild.get_role(guider),
                "⛏": self.bot.guild.get_role(miner),
                "❌": self.bot.guild.get_role(None)
                }
            self.reaction_message = await self.bot.get_channel(assignRole).fetch_message(783732648862154752)
            self.reaction_message2 = await self.bot.get_channel(assignRole).fetch_message(784004227386179614)
            self.reaction_message3 = await self.bot.get_channel(assignRole).fetch_message(784011791042609173)
            self.bot.cogs_ready.ready_up("reactions")
    
    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == self.reaction_message.id:
            current_numbers = filter(lambda r: r in self.numbers.values(), payload.member.roles)
            await payload.member.remove_roles(*current_numbers, reason="role reaction.")
            await payload.member.add_roles(self.numbers[payload.emoji.name], reason="role reaction.")
            await self.reaction_message.remove_reaction(payload.emoji, payload.member)
        elif payload.message_id == self.reaction_message2.id:
            await payload.member.add_roles(self.guidance[payload.emoji.name], reason="role reaction.")
        elif payload.message_id == self.reaction_message3.id:
            current_guidance = filter(lambda r: r in self.guidance.values(), payload.member.roles)
            await payload.member.remove_roles(*current_guidance, reason="role reaction.")
            await payload.member.add_roles(self.guidance[payload.emoji.name], reason="role reaction.")
            await self.reaction_message.remove_reaction(payload.emoji, payload.member)

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        pass

def setup(bot):
	bot.add_cog(Reactions(bot))
import asyncio

import discord
from discord.ext import commands


class Chat(commands.Cog):
	def __init__(self, bot, config, chat):
		self.bot = bot
		self.config = config
		self.chat = chat
		self.embed = {}

	@commands.command(name="online")
	async def _online(self, message):
		users = self.chat.getOnline()
		messageContent = ""

		for user in users:
			messageContent += f"{user['username']}{' 📱' if user['mobile'] else ''} \n"
		embed=discord.Embed(title="Utilisateurs en ligne", url="https://tiplanet.org/forum/chat", description=f"```{messageContent}```", color=0x00ff00)
		embed.set_thumbnail(url="https://tiplanet.org/forum/styles/prosilver/theme/images/tiplanet_header_logo.png")
		reply = await message.reply(embed=embed, mention_author=False)

		await reply.add_reaction("🗑️")
		self.embed[reply.id] = 1

		# After 60 seconds, it deletes it from the storage dictionary
		await asyncio.sleep(60)
		self.embed.pop(reply.id)

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, reaction):
		# Ignore bots
		if self.bot.get_user(reaction.user_id).bot:
			return

		# If the reaction is "🗑️" and on a message stored in issue_embeds,
		# it deletes it and set it deleted in the storage dictionary
		if reaction.emoji.name == "🗑️" and self.embed.get(reaction.message_id):
			channel = self.bot.get_channel(reaction.channel_id)
			message = await channel.fetch_message(reaction.message_id)
			ref = message.reference

			if self.bot.get_user(reaction.user_id) == ref.resolved.author:
				await message.delete()
				self.embed[reaction.message_id] = 0
			else:
				return


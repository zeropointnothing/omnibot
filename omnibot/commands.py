import discord
import discord.ext.commands as commands
from bot import OmniBot

# Configure intents explicitly
intents = discord.Intents.default()
intents.message_content = True  # Enables reading message content
bot = OmniBot(command_prefix="0!", intents=intents)

@bot.command("ping", help="The ping.")
async def ping_command(ctx: commands.Context):
    await ctx.reply(f"Pong! {round(bot.latency, 4)}sec.")
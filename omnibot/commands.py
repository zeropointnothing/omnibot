import discord
import discord.ext.commands as commands
from bot import OmniBot

# Configure intents explicitly
intents = discord.Intents.default()
intents.message_content = True  # Enables reading message content
bot = OmniBot(command_prefix="o!", intents=intents)

@bot.command(name="ping", help="The ping.")
async def ping_command(ctx: commands.Context):
    await ctx.reply(f"Pong! {round(bot.latency, 4)}sec.")

@bot.command(name="about", help="About the bot.")
async def about_command(ctx: commands.Context):
    await ctx.reply(f"[OmniBot](https://github.com/zeropointnothing/omnibot) was created by ex11c0de (for no good reason) with love. <3")
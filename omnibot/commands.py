import discord
import discord.utils
import discord.ext.commands as commands
from bot import OmniBot
from utils import VoiceWatcher, voice_once_done_callback

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

@bot.command(name="join", help="Join a VC.")
async def join_command(ctx: commands.Context):
    voice = ctx.message.author.voice

    if not voice:
        await ctx.reply("You aren't in a voice channel!")
        return

    channel = ctx.message.author.voice.channel

    if not discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild):
        vc = await channel.connect()
        # bot.connections.update({ctx.message.guild.id: vc})
        vw = VoiceWatcher(ctx, vc, False)
        vc.start_recording(
                discord.sinks.WaveSink(),
                voice_once_done_callback,
                ctx.message.channel,
                vw,
                bot
            )
        bot.connections.update({ctx.message.guild.id: vw})
        await ctx.reply("Started recording!")
    else:
        await ctx.reply("I'm already in that channel!")
        return

@bot.command(name="leave", help="Stop it.")
async def stop_command(ctx: commands.Context):
    if ctx.message.guild.id in bot.connections:
        vc = bot.connections[ctx.message.guild.id]
        vc.channel.stop_recording()
        del bot.connections[ctx.message.guild.id]
    else:
        await ctx.reply("I am not recording!")

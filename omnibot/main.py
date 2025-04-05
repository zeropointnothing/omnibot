import json
import discord
import discord.ext.commands as commands
from discord import Message


class OmniBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        # self.command_prefix = "o!"

        super().__init__(*args, **kwargs)

        # register commands
        self.add_command(commands.Command(self.ping_command, name="ping", description="The ping."))

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message: Message):
        # print(f'Message from {message.author}: {message.content}')
        ctx: commands.Context = await self.get_context(message)

        if not message.author.bot and not message.is_system() and not ctx.valid:
            await message.reply("Are you sure?")

        await self.process_commands(message) # restore command capabilities

    async def ping_command(self, ctx: commands.Context):
        await ctx.reply(f"Pong! {round(self.latency, 4)}sec.")

with open("../token.json", "r") as f:
    # Configure intents explicitly
    intents = discord.Intents.default()
    intents.message_content = True  # Enables reading message content

    client = OmniBot(command_prefix="o!", intents=intents)
    client.run(json.load(f)["token"])
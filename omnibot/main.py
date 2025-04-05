import json
import discord
import discord.ext.commands as commands
import random
from difflib import SequenceMatcher
from discord import Message

class Database:
    def __init__(self):
        pass

def are_strings_similar(str1, str2, threshold=0.8):
    similarity_ratio = SequenceMatcher(None, str1, str2).ratio()
    return similarity_ratio >= threshold

class OmniBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        # self.command_prefix = "o!"
        self.rand_ceiling = 100
        self.rand_floor = 0
        self.rand_need = 60

        # what omnimand can reply with
        self.rand_replies = {
            "Are you sure?": 0.9,
            "THINK {user}, THINK!": 0.1
        }

        # 'meme' phrases that should always trigger a response
        self.always_replies = [
            "threw a trash bag",
            "threw a trash bag into space",
            "i had a pretty interesting day",
            "pretty sure",
            "at work",
            "into space",
            "guess who's finally getting his powers",
            "guess whos finally getting his powers"
        ]

        super().__init__(*args, **kwargs)

        # register commands
        self.add_command(commands.Command(self.ping_command, name="ping", description="The ping."))

    def get_reply(self) -> str:
        """
        Get a reply based on probability.
        """
        randnum = random.randint(0, 100)/100
        prob = None
        while not prob:
            prob = [_ for _ in self.rand_replies if self.rand_replies[_] >= randnum]

        return prob[0]

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message: Message):
        # print(f'Message from {message.author}: {message.content}')
        ctx: commands.Context = await self.get_context(message)

        if not message.author.bot and not message.is_system() and not ctx.valid:
            replynum = random.randint(self.rand_floor, self.rand_ceiling) # random trigger
            # meme trigger
            is_meme = any([are_strings_similar(_, message.content) for _ in self.always_replies])
            # response
            message_choice = self.get_reply() if not is_meme else "Are you sure?"

            if replynum >= self.rand_need or is_meme:
                await ctx.reply(message_choice.format(
                    user=ctx.message.author.name.upper()
                ))

                print(f"replied to {ctx.message.author}: {ctx.message.content} (num:{replynum}/meme:{is_meme}/choice:{message_choice})")

        await self.process_commands(message) # restore command capabilities

    async def ping_command(self, ctx: commands.Context):
        await ctx.reply(f"Pong! {round(self.latency, 4)}sec.")

with open("token.json", "r") as f:
    # Configure intents explicitly
    intents = discord.Intents.default()
    intents.message_content = True  # Enables reading message content

    client = OmniBot(command_prefix="o!", intents=intents)
    client.run(json.load(f)["token"])
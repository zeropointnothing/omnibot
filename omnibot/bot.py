import discord.ext.commands as commands
import discord.ext.tasks as tasks
import random
import discord
import asyncio
from utils import Reply, ReplyType, are_strings_similar, voice_once_done_callback, VoiceWatcher

class OmniBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        # self.command_prefix = "o!"
        self.rand_ceiling = 100
        self.rand_floor = 0
        self.rand_need = 60

        # what omnimand can reply with
        self.rand_replies = [
            Reply(ReplyType.MESSAGE, "Are you sure?", 0.9),
            Reply(ReplyType.GIF, "https://tenor.com/view/omni-man-omni-man-are-you-sure-are-you-sure-invincible-gif-3935116808772397515", 0.5),
            Reply(ReplyType.MESSAGE, "THINK {user_caps}, THINK", 0.01)
        ]

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

        self.connections: dict[str, VoiceWatcher] = {}

        super().__init__(*args, **kwargs)

    def get_reply(self) -> Reply:
        """
        Get a reply based on probability.
        """
        return random.choices(self.rand_replies, [_.probability for _ in self.rand_replies])[0]

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        self.task_loop.start()

    async def on_message(self, message: discord.Message):
        # print(f'Message from {message.author}: {message.content}')

        if (not message.author.bot and not message.is_system()) and not message.content.startswith(self.command_prefix):
            replynum = random.randint(self.rand_floor, self.rand_ceiling) # random trigger
            # meme trigger
            is_meme = any([are_strings_similar(_, message.content) for _ in self.always_replies])
            # response
            reply_choice = self.get_reply() if not is_meme else self.rand_replies[0]

            if reply_choice.reply_type == ReplyType.MESSAGE:
                if replynum >= self.rand_need or is_meme:
                    await message.reply(reply_choice.message.format(
                        user=message.author.name,
                        user_caps=message.author.name.upper()
                    ))

                    print(f"replied to {message.author}: {message.content} (num:{replynum}/meme:{is_meme}/choice:{reply_choice})")
            elif reply_choice.reply_type == ReplyType.GIF:
                if replynum >= self.rand_need or is_meme:
                    await message.reply(reply_choice.message)

                    print(f"replied (gif) to {message.author}: {message.content} (num:{replynum}/meme:{is_meme}/choice:{reply_choice})")

        await self.process_commands(message) # restore command capabilities
    
    @tasks.loop(seconds=5)
    async def task_loop(self):
        # print("Task Loop!")
        for task in self.connections:
            conn = self.connections[task]

            if conn.channel.recording:
                print(f"Toggling Connection: {conn} (recording:{conn.channel.recording})")
                conn.processing = True
                conn.channel.stop_recording()
                print("Begin Processing!")

            while True:
                if conn.processing == False:
                    break
                print(f"waiting... {conn.processing}")
                await asyncio.sleep(1)

            conn.channel.start_recording(
                discord.sinks.WaveSink(),
                voice_once_done_callback,
                conn.ctx.message.channel,
                conn,
                self
            )


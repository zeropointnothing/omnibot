from dataclasses import dataclass
from enum import Enum, auto
from difflib import SequenceMatcher
import discord
import discord.ext.commands
import discord.utils
import pydub.exceptions
import speech_recognition
import pydub
import json
import random

class ReplyType(Enum):
    MESSAGE = auto()
    GIF = auto()

@dataclass
class Reply:
    # def __init__(self, reply_type: ReplyType, message: str, probability: float):
    reply_type: ReplyType
    message: str = ""
    probability: float = 1.0

@dataclass
class VoiceWatcher:
    ctx: discord.ext.commands.Context
    channel: discord.VoiceClient
    processing: bool

def are_strings_similar(str1, str2, threshold=0.8):
    similarity_ratio = SequenceMatcher(None, str1, str2).ratio()
    return similarity_ratio >= threshold

async def voice_once_done_callback(sink: discord.sinks, channel: discord.TextChannel, conn: VoiceWatcher, bot: discord.ext.commands.Bot, *args):
    r = speech_recognition.Recognizer()

    # await sink.vc.disconnect()
    playing_sound = False

    out = []
    files = []
    for user_id, file in sink.audio_data.items():
        try:
            audio = pydub.AudioSegment.from_file(file.file)
        except pydub.exceptions.CouldntDecodeError:
            continue
        audio: pydub.AudioSegment
        converted_audio = audio.export(format="wav")
        # files.append(discord.File(converted_audio.file, f"{user_id}.{sink.encoding}"))
        with speech_recognition.AudioFile(converted_audio) as source:
            print(f"Attempting to recognize speech for user of ID '{user_id}'...")
            try:
                audio_data = r.record(source)
                text = json.loads(r.recognize_vosk(audio_data, language="en-US"))
                out.append(f"<@{user_id}> ({await bot.fetch_user(user_id)}): \"{text['text']}\"")

                if text:
                    reply_num = random.randint(bot.rand_floor, bot.rand_ceiling) # random trigger
                    # meme trigger
                    is_meme = any([are_strings_similar(_, text["text"], 0.5) for _ in bot.always_replies])
                    # response

                    if is_meme:
                        playing_sound = True

            except speech_recognition.UnknownValueError:
                print(f"Skipping {user_id} as Google did not understand them.")
            except speech_recognition.RequestError:
                print(f"Skipping {user_id} as Google rejected the request.")
        converted_audio.seek(0)

    if playing_sound:
        print("Playing sound!")
        conn.channel.play(discord.FFmpegPCMAudio('sound.wav'), after=lambda e: print("Done: ", e))

    conn.processing = False
    if out:
        print(f"Finished audio processing for : {', '.join(out)}.")

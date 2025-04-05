from dataclasses import dataclass
from enum import Enum, auto
from difflib import SequenceMatcher

class ReplyType(Enum):
    MESSAGE = auto()
    GIF = auto()

@dataclass
class Reply:
    # def __init__(self, reply_type: ReplyType, message: str, probability: float):
    reply_type: ReplyType
    message: str = ""
    probability: float = 1.0

def are_strings_similar(str1, str2, threshold=0.8):
    similarity_ratio = SequenceMatcher(None, str1, str2).ratio()
    return similarity_ratio >= threshold
from telegram import InlineKeyboardButton

from fun.configs.states import *
from general.configs.states import END

FUN_BUTTON = InlineKeyboardButton(text='Fun', callback_data=str(FUN))

MEME_BUTTON = InlineKeyboardButton(text='Programming meme', callback_data=str(FUN_MEME))
JOKE_BUTTON = InlineKeyboardButton(text='Joke', callback_data=str(FUN_JOKE))
BACK_BUTTON = InlineKeyboardButton(text='Back', callback_data=str(END))

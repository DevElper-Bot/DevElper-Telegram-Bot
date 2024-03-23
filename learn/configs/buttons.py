from telegram import InlineKeyboardButton

from general.configs.states import END
from learn.configs.states import *

LEARNING_BUTTON = InlineKeyboardButton(text='Learning', callback_data=str(LEARNING))
SEARCH_THE_WEB_BUTTON = InlineKeyboardButton(text='Search the web', callback_data=str(LEARNING_SEARCH))
ASK_AI_BUTTON = InlineKeyboardButton(text='Ask AI', callback_data=str(LEARNING_ASK_AI))
BACK_BUTTON = InlineKeyboardButton(text='Back', callback_data=str(END))

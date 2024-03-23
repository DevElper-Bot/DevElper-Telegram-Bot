from telegram import InlineKeyboardButton

from general.configs.states import END

END_BUTTON = InlineKeyboardButton(text='Done', callback_data=str(END))

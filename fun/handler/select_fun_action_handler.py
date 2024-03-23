from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from fun.configs.buttons import *
from fun.configs.messages import SELECT_FUN_ACTION_MESSAGE


async def select_fun_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Choose to receive a meme or a joke."""
    buttons = [
        [
            MEME_BUTTON,
            JOKE_BUTTON,
        ],
        [
            BACK_BUTTON,
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=SELECT_FUN_ACTION_MESSAGE, reply_markup=keyboard)

    return FUN

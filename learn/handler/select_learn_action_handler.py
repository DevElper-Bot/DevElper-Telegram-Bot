from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from learn.configs.buttons import *
from learn.configs.messages import SELECT_LEARN_ACTION_MESSAGE


async def select_learn_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Choose to search on the web or ask AI LLM tools."""
    buttons = [
        [
            SEARCH_THE_WEB_BUTTON,
            ASK_AI_BUTTON,
        ],
        [
            BACK_BUTTON,
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=SELECT_LEARN_ACTION_MESSAGE, reply_markup=keyboard)

    return LEARNING

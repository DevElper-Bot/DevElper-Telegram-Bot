from telegram import Update
from telegram.ext import ContextTypes

from general.configs.messages import END_TEXT
from general.configs.states import END


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End conversation from InlineKeyboardButton."""
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=END_TEXT)

    return END

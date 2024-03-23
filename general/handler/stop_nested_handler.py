from telegram import Update
from telegram.ext import ContextTypes

from general.configs.messages import STOP_CONVERSATION_TEXT
from general.configs.states import STOPPING


async def stop_nested(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Completely end conversation from within nested conversation."""
    await update.message.reply_text(STOP_CONVERSATION_TEXT)

    return STOPPING

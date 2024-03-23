from telegram import Update
from telegram.ext import ContextTypes

from general.configs.messages import STOP_CONVERSATION_TEXT
from general.configs.states import END


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End Conversation by command."""
    await update.message.reply_text(STOP_CONVERSATION_TEXT)

    return END

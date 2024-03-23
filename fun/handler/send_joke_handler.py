from telegram import Update
from telegram.ext import ContextTypes

from general.configs.states import END


async def send_joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='You are seeing a joke')

    return END

from telegram import Update
from telegram.ext import ContextTypes

from general.configs.states import END


async def add_new_pull_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='You are adding a new PR')

    return END

from telegram import Update
from telegram.ext import ContextTypes

from general.configs.states import END


async def search_the_web(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='You are searching the web')

    return END

from telegram import Update
from telegram.ext import ContextTypes

from general.configs.states import END


async def show_teams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='This is the teams info')

    return END

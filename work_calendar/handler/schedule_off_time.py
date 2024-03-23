from telegram import Update
from telegram.ext import ContextTypes

from general.configs.states import END


async def schedule_off_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='You are scheduling your off time')

    return END

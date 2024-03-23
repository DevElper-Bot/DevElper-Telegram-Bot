from telegram import Update
from telegram.ext import ContextTypes

from general.configs.states import START_OVER, END
from general.handler.start_handler import start


async def return_to_top_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Return to top level conversation."""
    context.user_data[START_OVER] = True
    await start(update, context)

    return END

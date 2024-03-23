from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from tasks_and_prs.configs.buttons import *
from tasks_and_prs.configs.messages import SELECT_TASKS_AND_PRS_ACTION_TEXT


async def select_task_and_prs_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Choose an action regarding tasks or prs."""
    buttons = [
        [
            NEW_REVIEW_BUTTON,
            REJECT_REVIEW_BUTTON,
        ],
        [
            FINISH_REVIEW_BUTTON,
            SHOW_PRS_BUTTON,
        ],
        [
            BACK_BUTTON,
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=SELECT_TASKS_AND_PRS_ACTION_TEXT, reply_markup=keyboard)

    return TASKS_AND_PRS

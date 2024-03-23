from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from general.configs.messages import SELECT_ACTION_TEXT, GREETING_TEXT
from general.configs.states import START_OVER, SELECTING_ACTION


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""

    from organization.configs.buttons import ORGANIZATION_BUTTON
    from tasks_and_prs.configs.buttons import TASKS_AND_PRS_BUTTON
    from learn.configs.buttons import LEARNING_BUTTON
    from fun.configs.buttons import FUN_BUTTON
    from work_calendar.configs.buttons import CALENDAR_BUTTON
    from general.configs.buttons import END_BUTTON

    buttons = [
        [
            ORGANIZATION_BUTTON,
            TASKS_AND_PRS_BUTTON,
        ],
        [
            LEARNING_BUTTON,
            FUN_BUTTON,
        ],
        [
            CALENDAR_BUTTON,
            END_BUTTON,
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    # If we're starting over we don't need to send a new message
    if context.user_data.get(START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=SELECT_ACTION_TEXT, reply_markup=keyboard)
    else:
        await update.message.reply_text(GREETING_TEXT)
        await update.message.reply_text(text=SELECT_ACTION_TEXT, reply_markup=keyboard)

    context.user_data[START_OVER] = False
    return SELECTING_ACTION

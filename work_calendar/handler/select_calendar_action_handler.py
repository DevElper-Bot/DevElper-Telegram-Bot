from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from work_calendar.configs.buttons import SET_MEETING_BUTTON, SET_OFF_TIME_BUTTON, SHOW_CALENDER_BUTTON, \
    CALENDAR_BACK_BUTTON
from work_calendar.configs.messages import SELECTING_CALENDAR_ACTION_MESSAGE
from work_calendar.configs.states import CALENDAR


async def select_calendar_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """You can manage your calendar and see the calendar of your teammates."""
    text = SELECTING_CALENDAR_ACTION_MESSAGE
    buttons = [
        [
            SET_MEETING_BUTTON,
            SET_OFF_TIME_BUTTON,
        ],
        [
            SHOW_CALENDER_BUTTON,
            CALENDAR_BACK_BUTTON,
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return CALENDAR

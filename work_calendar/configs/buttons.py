from telegram import InlineKeyboardButton

from work_calendar.configs.states import CALENDAR_SET_MEETING, CALENDAR_SET_OFF_TIME, CALENDAR_SHOW_SCHEDULE
from general.configs.states import END

SET_MEETING_BUTTON = InlineKeyboardButton(text='Schedule a meeting', callback_data=str(CALENDAR_SET_MEETING))
SET_OFF_TIME_BUTTON = InlineKeyboardButton(text='Schedule off-time', callback_data=str(CALENDAR_SET_OFF_TIME))
SHOW_CALENDER_BUTTON = InlineKeyboardButton(text='See calendars', callback_data=str(CALENDAR_SHOW_SCHEDULE))
CALENDAR_BACK_BUTTON = InlineKeyboardButton(text='Back', callback_data=str(END))

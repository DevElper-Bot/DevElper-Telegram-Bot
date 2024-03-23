from telegram import InlineKeyboardButton

from work_calendar.configs.states import *
from general.configs.states import END

CALENDAR_BUTTON = InlineKeyboardButton(text='Calendar', callback_data=str(CALENDAR))

SET_MEETING_BUTTON = InlineKeyboardButton(text='Schedule a meeting', callback_data=str(CALENDAR_SET_MEETING))
SET_OFF_TIME_BUTTON = InlineKeyboardButton(text='Schedule off-time', callback_data=str(CALENDAR_SET_OFF_TIME))
SHOW_CALENDER_BUTTON = InlineKeyboardButton(text='See calendars', callback_data=str(CALENDAR_SHOW_SCHEDULE))
CALENDAR_BACK_BUTTON = InlineKeyboardButton(text='Back', callback_data=str(END))

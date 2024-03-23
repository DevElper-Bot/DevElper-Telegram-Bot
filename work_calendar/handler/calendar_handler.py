from telegram.ext import ConversationHandler, CallbackQueryHandler, CommandHandler

from general.configs.states import END, STOPPING, SELECTING_ACTION
from general.handler.return_to_top_level_handler import return_to_top_level
from general.handler.stop_nested_handler import stop_nested
from work_calendar.configs.states import CALENDAR, CALENDAR_SET_MEETING, CALENDAR_SET_OFF_TIME, CALENDAR_SHOW_SCHEDULE
from work_calendar.handler.schedule_meeting_handler import schedule_meeting
from work_calendar.handler.schedule_off_time import schedule_off_time
from work_calendar.handler.select_calendar_action_handler import select_calendar_action
from work_calendar.handler.show_calendar_handler import show_calendar

calendar_conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(select_calendar_action, pattern='^' + str(CALENDAR) + '$')],
    states={
        CALENDAR: [
            CallbackQueryHandler(schedule_meeting, pattern='^' + str(CALENDAR_SET_MEETING) + '$'),
            CallbackQueryHandler(schedule_off_time, pattern='^' + str(CALENDAR_SET_OFF_TIME) + '$'),
            CallbackQueryHandler(show_calendar, pattern='^' + str(CALENDAR_SHOW_SCHEDULE) + '$'),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(return_to_top_level, pattern='^' + str(END) + '$'),
        CommandHandler('stop', stop_nested),
    ],
    map_to_parent={
        # Return to top level menu
        END: SELECTING_ACTION,
        # End conversation altogether
        STOPPING: END,
    },
)
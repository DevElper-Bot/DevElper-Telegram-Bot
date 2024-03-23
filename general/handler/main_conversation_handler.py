from telegram.ext import CommandHandler, ConversationHandler

from general.configs.states import STOPPING, SELECTING_ACTION
from general.handler.start_handler import start
from general.handler.stop_handler import stop


def get_main_conversation_handler():
    from fun.handler.fun_handler import fun_conv_handler
    from learn.handler.learn_handler import learn_conv_handler
    from organization.handler.organization_handler import organization_conv_handler
    from tasks_and_prs.handler.tasks_and_prs_handler import tasks_and_prs_conv_handler
    from work_calendar.handler.calendar_handler import calendar_conv_handler

    module_handlers = [
        organization_conv_handler,
        tasks_and_prs_conv_handler,
        learn_conv_handler,
        fun_conv_handler,
        calendar_conv_handler,
    ]
    return ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECTING_ACTION: module_handlers,
            STOPPING: [CommandHandler('start', start)],
        },
        fallbacks=[CommandHandler('stop', stop)],
    )

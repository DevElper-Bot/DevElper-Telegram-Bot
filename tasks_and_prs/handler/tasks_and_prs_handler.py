from telegram.ext import ConversationHandler, CallbackQueryHandler, CommandHandler

from general.configs.states import END, SELECTING_ACTION, STOPPING
from general.handler.return_to_top_level_handler import return_to_top_level
from general.handler.stop_nested_handler import stop_nested
from tasks_and_prs.configs.states import *
from tasks_and_prs.handler.add_new_pull_request_handler import add_new_pull_request
from tasks_and_prs.handler.finish_pull_request_handler import finish_pull_request
from tasks_and_prs.handler.reject_pull_request_handler import reject_pull_request
from tasks_and_prs.handler.select_tasks_and_prs_action_handler import select_task_and_prs_action
from tasks_and_prs.handler.show_pull_requests_handler import show_pull_requests

tasks_and_prs_conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(select_task_and_prs_action, pattern='^' + str(TASKS_AND_PRS) + '$')],
    states={
        TASKS_AND_PRS: [
            CallbackQueryHandler(add_new_pull_request, pattern='^' + str(TASKS_AND_PRS_REVIEW_REQ) + '$'),
            CallbackQueryHandler(reject_pull_request, pattern='^' + str(TASKS_AND_PRS_REJECT_REVIEW) + '$'),
            CallbackQueryHandler(finish_pull_request, pattern='^' + str(TASKS_AND_PRS_FINISH_REV) + '$'),
            CallbackQueryHandler(show_pull_requests, pattern='^' + str(TASKS_AND_PRS_SHOW_PRS) + '$'),
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

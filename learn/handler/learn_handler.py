from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

from general.configs.states import END, SELECTING_ACTION, STOPPING
from general.handler.return_to_top_level_handler import return_to_top_level
from general.handler.stop_nested_handler import stop_nested
from learn.configs.states import *
from learn.handler.ask_ai_handler import ask_ai
from learn.handler.search_the_web_handler import search_the_web
from learn.handler.select_learn_action_handler import select_learn_action

learn_conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(select_learn_action, pattern='^' + str(LEARNING) + '$')],
    states={
        LEARNING: [
            CallbackQueryHandler(search_the_web, pattern='^' + str(LEARNING_SEARCH) + '$'),
            CallbackQueryHandler(ask_ai, pattern='^' + str(LEARNING_ASK_AI) + '$'),
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

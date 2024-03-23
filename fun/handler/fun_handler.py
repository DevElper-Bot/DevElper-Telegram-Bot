from telegram.ext import ConversationHandler, CallbackQueryHandler, CommandHandler

from fun.configs.states import *
from fun.handler.select_fun_action_handler import select_fun_action
from fun.handler.send_joke_handler import send_joke
from fun.handler.send_programming_meme_handler import send_programming_meme
from general.configs.states import END, SELECTING_ACTION, STOPPING
from general.handler.return_to_top_level_handler import return_to_top_level
from general.handler.stop_nested_handler import stop_nested

fun_conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(select_fun_action, pattern='^' + str(FUN) + '$')],
    states={
        FUN: [
            CallbackQueryHandler(send_programming_meme, pattern='^' + str(FUN_MEME) + '$'),
            CallbackQueryHandler(send_joke, pattern='^' + str(FUN_JOKE) + '$'),
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

# import logging
# import os
# from typing import Any, Dict, Tuple
#
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
# from telegram.ext import (
#     Application,
#     CallbackQueryHandler,
#     CommandHandler,
#     ContextTypes,
#     ConversationHandler,
#     MessageHandler,
#     filters,
# )
#
# # Enable logging
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )
# # set higher logging level for httpx to avoid all GET and POST requests being logged
# logging.getLogger("httpx").setLevel(logging.WARNING)
#
# logger = logging.getLogger(__name__)
#
# # State definitions for top level conversation
# SELECTING_ACTION, ADDING_MEMBER, ADDING_SELF, DESCRIBING_SELF = map(chr, range(4))
# # State definitions for second level conversation
# SELECTING_LEVEL, SELECTING_GENDER = map(chr, range(4, 6))
# # State definitions for descriptions conversation
# SELECTING_FEATURE, TYPING = map(chr, range(6, 8))
# # Meta states
# STOPPING, SHOWING = map(chr, range(8, 10))
# # Shortcut for ConversationHandler.END
# END = ConversationHandler.END
#
#
# TOKEN = os.getenv('BOT_TOKEN')
# BOT_USERNAME = os.getenv('BOT_USERNAME')
#
#
# def main() -> None:
#     """Run the bot."""
#     # Create the Application and pass it your bot's token.
#     application = Application.builder().token('6981378055:AAFqkjpnFbOrS5OgYDqbeVstG48wCZ9RvRk').build()
#
#     # Set up third level ConversationHandler (collecting features)
#     description_conv = ConversationHandler(
#         entry_points=[
#             CallbackQueryHandler(
#                 select_feature, pattern="^" + str(MALE) + "$|^" + str(FEMALE) + "$"
#             )
#         ],
#         states={
#             SELECTING_FEATURE: [
#                 CallbackQueryHandler(ask_for_input, pattern="^(?!" + str(END) + ").*$")
#             ],
#             TYPING: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_input)],
#         },
#         fallbacks=[
#             CallbackQueryHandler(end_describing, pattern="^" + str(END) + "$"),
#             CommandHandler("stop", stop_nested),
#         ],
#         map_to_parent={
#             # Return to second level menu
#             END: SELECTING_LEVEL,
#             # End conversation altogether
#             STOPPING: STOPPING,
#         },
#     )
#
#     # Set up second level ConversationHandler (adding a person)
#     add_member_conv = ConversationHandler(
#         entry_points=[CallbackQueryHandler(select_level, pattern="^" + str(ADDING_MEMBER) + "$")],
#         states={
#             SELECTING_LEVEL: [
#                 CallbackQueryHandler(select_gender, pattern=f"^{PARENTS}$|^{CHILDREN}$")
#             ],
#             SELECTING_GENDER: [description_conv],
#         },
#         fallbacks=[
#             CallbackQueryHandler(show_data, pattern="^" + str(SHOWING) + "$"),
#             CallbackQueryHandler(end_second_level, pattern="^" + str(END) + "$"),
#             CommandHandler("stop", stop_nested),
#         ],
#         map_to_parent={
#             # After showing data return to top level menu
#             SHOWING: SHOWING,
#             # Return to top level menu
#             END: SELECTING_ACTION,
#             # End conversation altogether
#             STOPPING: END,
#         },
#     )
#
#     # Set up top level ConversationHandler (selecting action)
#     # Because the states of the third level conversation map to the ones of the second level
#     # conversation, we need to make sure the top level conversation can also handle them
#     selection_handlers = [
#         add_member_conv,
#         CallbackQueryHandler(show_data, pattern="^" + str(SHOWING) + "$"),
#         CallbackQueryHandler(adding_self, pattern="^" + str(ADDING_SELF) + "$"),
#         CallbackQueryHandler(end, pattern="^" + str(END) + "$"),
#     ]
#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler("start", start)],
#         states={
#             SHOWING: [CallbackQueryHandler(start, pattern="^" + str(END) + "$")],
#             SELECTING_ACTION: selection_handlers,
#             SELECTING_LEVEL: selection_handlers,
#             DESCRIBING_SELF: [description_conv],
#             STOPPING: [CommandHandler("start", start)],
#         },
#         fallbacks=[CommandHandler("stop", stop)],
#     )
#
#     application.add_handler(conv_handler)
#
#     # Run the bot until the user presses Ctrl-C
#     application.run_polling(allowed_updates=Update.ALL_TYPES)
#
#
# if __name__ == "__main__":
#     main()

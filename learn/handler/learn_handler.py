#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using nested ConversationHandlers.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from typing import Any, Dict, Tuple

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# State definitions for top level conversation
SELECTING_ACTION = map(chr, range(1))
ORGANIZATION, TASKS_AND_PRS, LEARNING, FUN, CALENDAR = map(chr, range(10, 15))

# State definitions for second level conversation
(ORGANIZATION_ADD_ORG, ORGANIZATION_ADD_TEAM, ORGANIZATION_ADD_MEMBER, ORGANIZATION_SHOW_ORG,
 ORGANIZATION_SHOW_TEAMS, ORGANIZATION_SHOW_MEMBERS) = map(chr, range(100, 106))
TASKS_AND_PRS_REVIEW_REQ, TASKS_AND_PRS_FINISH_REV, TASKS_AND_PRS_REJECT_REVIEW, TASKS_AND_PRS_SHOW_PRS = map(chr, range(200, 204))
LEARNING_ASK_AI, LEARNING_SEARCH = map(chr, range(300, 302))
FUN_MEME, FUN_JOKE = map(chr, range(400, 402))
CALENDAR_SET_OFF_TIME, CALENDAR_SHOW_SCHEDULE, CALENDAR_SET_MEETING = map(chr, range(500, 503))

# State definitions for descriptions conversation
SELECTING_FEATURE, TYPING = map(chr, range(1000, 1002))
# Meta states
STOPPING, SHOWING = map(chr, range(2, 4))
# Shortcut for ConversationHandler.END
END = ConversationHandler.END

# Different constants for this example
(
    PARENTS,
    CHILDREN,
    SELF,
    GENDER,
    MALE,
    FEMALE,
    AGE,
    NAME,
    START_OVER,
    FEATURES,
    CURRENT_FEATURE,
    CURRENT_LEVEL,
) = map(chr, range(10000, 10012))


# Helper
def _name_switcher(level: str) -> Tuple[str, str]:
    if level == PARENTS:
        return "Father", "Mother"
    return "Brother", "Sister"


# Top level conversation callbacks
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    text = (
        'You may choose to follow with the matters related to the organization, tasks and PRs, learning, fun, '
        'or calendar. To abort, simply type /stop.'
    )

    buttons = [
        [
            InlineKeyboardButton(text='Organization', callback_data=str(ORGANIZATION)),
            InlineKeyboardButton(text='Tasks and PRs', callback_data=str(TASKS_AND_PRS)),
        ],
        [
            InlineKeyboardButton(text='Learning', callback_data=str(LEARNING)),
            InlineKeyboardButton(text='Fun', callback_data=str(FUN)),
        ],
        [
            InlineKeyboardButton(text='Calendar', callback_data=str(CALENDAR)),
            InlineKeyboardButton(text='Done', callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    # If we're starting over we don't need to send a new message
    if context.user_data.get(START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        await update.message.reply_text(
            "Hi, I'm Developer Helper Bot and I'm here to help you with all your developer needs."
        )
        await update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False
    return SELECTING_ACTION

#
# async def adding_self(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
#     """Add information about yourself."""
#     context.user_data[CURRENT_LEVEL] = SELF
#     text = "Okay, please tell me about yourself."
#     button = InlineKeyboardButton(text="Add info", callback_data=str(MALE))
#     keyboard = InlineKeyboardMarkup.from_button(button)
#
#     await update.callback_query.answer()
#     await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
#
#     return DESCRIBING_SELF
#
#
# async def show_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
#     """Pretty print gathered data."""
#
#     def pretty_print(data: Dict[str, Any], level: str) -> str:
#         people = data.get(level)
#         if not people:
#             return "\nNo information yet."
#
#         return_str = ""
#         if level == SELF:
#             for person in data[level]:
#                 return_str += f"\nName: {person.get(NAME, '-')}, Age: {person.get(AGE, '-')}"
#         else:
#             male, female = _name_switcher(level)
#
#             for person in data[level]:
#                 gender = female if person[GENDER] == FEMALE else male
#                 return_str += (
#                     f"\n{gender}: Name: {person.get(NAME, '-')}, Age: {person.get(AGE, '-')}"
#                 )
#         return return_str
#
#     user_data = context.user_data
#     text = f"Yourself:{pretty_print(user_data, SELF)}"
#     text += f"\n\nParents:{pretty_print(user_data, PARENTS)}"
#     text += f"\n\nChildren:{pretty_print(user_data, CHILDREN)}"
#
#     buttons = [[InlineKeyboardButton(text="Back", callback_data=str(END))]]
#     keyboard = InlineKeyboardMarkup(buttons)
#
#     await update.callback_query.answer()
#     await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
#     user_data[START_OVER] = True
#
#     return SHOWING


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End Conversation by command."""
    await update.message.reply_text('Okay, bye.')

    return END


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End conversation from InlineKeyboardButton."""
    await update.callback_query.answer()

    text = 'See you around!'
    await update.callback_query.edit_message_text(text=text)

    return END


# Second level conversation callbacks
async def select_organization_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """You can see or change the information regarding your organization."""
    text = (
        'You can choose to add a new organization, team, or member, or you can show the information about '
        'your organization, teams, or members of a team.'
    )
    buttons = [
        [
            InlineKeyboardButton(text='Add new organization', callback_data=str(ORGANIZATION_ADD_ORG)),
            InlineKeyboardButton(text='Add new team', callback_data=str(ORGANIZATION_ADD_TEAM)),
        ],
        [
            InlineKeyboardButton(text='Add member', callback_data=str(ORGANIZATION_ADD_MEMBER)),
            InlineKeyboardButton(text='Show organization info', callback_data=str(ORGANIZATION_SHOW_ORG)),
        ],
        [
            InlineKeyboardButton(text='Show your teams', callback_data=str(ORGANIZATION_SHOW_TEAMS)),
            InlineKeyboardButton(text='Show members', callback_data=str(ORGANIZATION_SHOW_MEMBERS)),
        ],
        [
            InlineKeyboardButton(text='Back', callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return ORGANIZATION


async def add_new_organization(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='You are adding a new organization')

    return END


async def add_new_team(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='You are adding a new team')

    return END


async def add_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='You are adding a new member')

    return END


async def show_organization(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='This is the organization info')

    return END


async def show_teams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='This is the teams info')

    return END


async def show_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='This is members info')

    return END


async def select_task_and_prs_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Choose an action regarding tasks or prs."""
    text = (
        'You can choose to ask for a PR review, reject a review request, finish a review request, or '
        'see the PRs of your team based on your filter criteria.'
    )
    buttons = [
        [
            InlineKeyboardButton(text='Request for PR review', callback_data=str(TASKS_AND_PRS_REVIEW_REQ)),
            InlineKeyboardButton(text='Reject PR review', callback_data=str(TASKS_AND_PRS_REJECT_REVIEW)),
        ],
        [
            InlineKeyboardButton(text='Finish PR review', callback_data=str(TASKS_AND_PRS_FINISH_REV)),
            InlineKeyboardButton(text='Show PRs', callback_data=str(TASKS_AND_PRS_SHOW_PRS)),
        ],
        [
            InlineKeyboardButton(text='Back', callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return TASKS_AND_PRS


async def add_new_pull_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='You are adding a new PR')

    return END


async def reject_pull_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='You are rejecting a PR')

    return END


async def finish_pull_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='You are finishing a PR')

    return END


async def select_learning_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Choose to search on the web or ask AI LLM tools."""
    text = 'Do you want to search on the web or ask an AI model?'
    buttons = [
        [
            InlineKeyboardButton(text='Search the web', callback_data=str(LEARNING_SEARCH)),
            InlineKeyboardButton(text='Ask AI', callback_data=str(LEARNING_ASK_AI)),
        ],
        [
            InlineKeyboardButton(text='Back', callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return LEARNING


async def search_the_web(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='You are searching the web')

    return END


async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='You are asking AI')

    return END


async def select_fun_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Choose to receive a meme or a joke."""
    text = 'Do you want to look at a programming meme or read a joke?'
    buttons = [
        [
            InlineKeyboardButton(text='Programming meme', callback_data=str(FUN_MEME)),
            InlineKeyboardButton(text='Joke', callback_data=str(FUN_JOKE)),
        ],
        [
            InlineKeyboardButton(text='Back', callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return FUN


async def send_programming_meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='You are seeing a meme')

    return END


async def send_joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='You are seeing a joke')

    return END


async def select_calendar_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """You can manage your calendar and see the calendar of your teammates."""
    text = 'You can schedule a meeting, announce your off-time, or see your or your teammate\'s schedule.'
    buttons = [
        [
            InlineKeyboardButton(text='Schedule a meeting', callback_data=str(CALENDAR_SET_MEETING)),
            InlineKeyboardButton(text='Schedule off-time', callback_data=str(CALENDAR_SET_OFF_TIME)),
        ],
        [
            InlineKeyboardButton(text='See calendars', callback_data=str(CALENDAR_SHOW_SCHEDULE)),
            InlineKeyboardButton(text='Back', callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return CALENDAR


async def schedule_meeting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='You are scheduling a meeting')

    return END


async def schedule_off_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='You are scheduling your off time')

    return END


async def show_calendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='You are seeing your calendar')

    return END

#
# async def select_gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
#     """Choose to add mother or father."""
#     level = update.callback_query.data
#     context.user_data[CURRENT_LEVEL] = level
#
#     text = "Please choose, whom to add."
#
#     male, female = _name_switcher(level)
#
#     buttons = [
#         [
#             InlineKeyboardButton(text=f"Add {male}", callback_data=str(MALE)),
#             InlineKeyboardButton(text=f"Add {female}", callback_data=str(FEMALE)),
#         ],
#         [
#             InlineKeyboardButton(text="Show data", callback_data=str(SHOWING)),
#             InlineKeyboardButton(text="Back", callback_data=str(END)),
#         ],
#     ]
#     keyboard = InlineKeyboardMarkup(buttons)
#
#     await update.callback_query.answer()
#     await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
#
#     return SELECTING_GENDER
#
#
# async def end_second_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Return to top level conversation."""
#     context.user_data[START_OVER] = True
#     await start(update, context)
#
#     return END
#
#
# # Third level callbacks
# async def select_feature(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
#     """Select a feature to update for the person."""
#     buttons = [
#         [
#             InlineKeyboardButton(text="Name", callback_data=str(NAME)),
#             InlineKeyboardButton(text="Age", callback_data=str(AGE)),
#             InlineKeyboardButton(text="Done", callback_data=str(END)),
#         ]
#     ]
#     keyboard = InlineKeyboardMarkup(buttons)
#
#     # If we collect features for a new person, clear the cache and save the gender
#     if not context.user_data.get(START_OVER):
#         context.user_data[FEATURES] = {GENDER: update.callback_query.data}
#         text = "Please select a feature to update."
#
#         await update.callback_query.answer()
#         await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
#     # But after we do that, we need to send a new message
#     else:
#         text = "Got it! Please select a feature to update."
#         await update.message.reply_text(text=text, reply_markup=keyboard)
#
#     context.user_data[START_OVER] = False
#     return SELECTING_FEATURE
#
#
# async def ask_for_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
#     """Prompt user to input data for selected feature."""
#     context.user_data[CURRENT_FEATURE] = update.callback_query.data
#     text = "Okay, tell me."
#
#     await update.callback_query.answer()
#     await update.callback_query.edit_message_text(text=text)
#
#     return TYPING
#
#
# async def save_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
#     """Save input for feature and return to feature selection."""
#     user_data = context.user_data
#     user_data[FEATURES][user_data[CURRENT_FEATURE]] = update.message.text
#
#     user_data[START_OVER] = True
#
#     return await select_feature(update, context)
#
#
# async def end_describing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """End gathering of features and return to parent conversation."""
#     user_data = context.user_data
#     level = user_data[CURRENT_LEVEL]
#     if not user_data.get(level):
#         user_data[level] = []
#     user_data[level].append(user_data[FEATURES])
#
#     # Print upper level menu
#     if level == SELF:
#         user_data[START_OVER] = True
#         await start(update, context)
#     else:
#         await select_learning_action(update, context)
#
#     return END
#
#
async def stop_nested(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Completely end conversation from within nested conversation."""
    await update.message.reply_text('Okay, bye.')

    return STOPPING


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token('6981378055:AAFqkjpnFbOrS5OgYDqbeVstG48wCZ9RvRk').build()

    # Set up third level ConversationHandler (collecting features)
    # description_conv = ConversationHandler(
    #     entry_points=[
    #         CallbackQueryHandler(
    #             select_feature, pattern="^" + str(MALE) + "$|^" + str(FEMALE) + "$"
    #         )
    #     ],
    #     states={
    #         SELECTING_FEATURE: [
    #             CallbackQueryHandler(ask_for_input, pattern="^(?!" + str(END) + ").*$")
    #         ],
    #         TYPING: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_input)],
    #     },
    #     fallbacks=[
    #         CallbackQueryHandler(end_describing, pattern="^" + str(END) + "$"),
    #         CommandHandler("stop", stop_nested),
    #     ],
    #     map_to_parent={
    #         # Return to second level menu
    #         END: SELECTING_LEVEL,
    #         # End conversation altogether
    #         STOPPING: STOPPING,
    #     },
    # )
    #
    # # Set up second level ConversationHandler (adding a person)
    # add_member_conv = ConversationHandler(
    #     entry_points=[CallbackQueryHandler(select_level, pattern="^" + str(ADDING_MEMBER) + "$")],
    #     states={
    #         SELECTING_LEVEL: [
    #             CallbackQueryHandler(select_gender, pattern=f"^{PARENTS}$|^{CHILDREN}$")
    #         ],
    #         SELECTING_GENDER: [description_conv],
    #     },
    #     fallbacks=[
    #         CallbackQueryHandler(show_data, pattern="^" + str(SHOWING) + "$"),
    #         CallbackQueryHandler(end_second_level, pattern="^" + str(END) + "$"),
    #         CommandHandler("stop", stop_nested),
    #     ],
    #     map_to_parent={
    #         # After showing data return to top level menu
    #         SHOWING: SHOWING,
    #         # Return to top level menu
    #         END: SELECTING_ACTION,
    #         # End conversation altogether
    #         STOPPING: END,
    #     },
    # )

    organization_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(select_organization_action, pattern="^" + str(ORGANIZATION) + "$")],
        states={
            ORGANIZATION: [
                CallbackQueryHandler(add_new_organization, pattern="^" + str(ORGANIZATION_ADD_ORG) + "$"),
                CallbackQueryHandler(add_new_team, pattern="^" + str(ORGANIZATION) + "$"),
                CallbackQueryHandler(add_member, pattern="^" + str(ORGANIZATION) + "$"),
                CallbackQueryHandler(show_organization, pattern="^" + str(ORGANIZATION) + "$"),
                CallbackQueryHandler(show_teams, pattern="^" + str(ORGANIZATION) + "$"),
                CallbackQueryHandler(show_members, pattern="^" + str(ORGANIZATION) + "$"),
            ],
        },
        fallbacks=[
            CommandHandler("stop", stop_nested),
        ],
        map_to_parent={
            # After showing data return to top level menu
            # SHOWING: SHOWING,
            # Return to top level menu
            END: SELECTING_ACTION,
            # End conversation altogether
            STOPPING: END,
        },
    )

    tasks_and_prs_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(select_task_and_prs_action, pattern="^" + str(TASKS_AND_PRS) + "$")],
        states={
            TASKS_AND_PRS: [
                CallbackQueryHandler(add_new_pull_request, pattern="^" + str(TASKS_AND_PRS_REVIEW_REQ) + "$"),
                CallbackQueryHandler(reject_pull_request, pattern="^" + str(TASKS_AND_PRS_REJECT_REVIEW) + "$"),
                CallbackQueryHandler(finish_pull_request, pattern="^" + str(TASKS_AND_PRS_FINISH_REV) + "$"),
            ],
        },
        fallbacks=[
            # CallbackQueryHandler(show_data, pattern="^" + str(SHOWING) + "$"),
            # CallbackQueryHandler(end_second_level, pattern="^" + str(END) + "$"),
            CommandHandler("stop", stop_nested),
        ],
        map_to_parent={
            # After showing data return to top level menu
            # SHOWING: SHOWING,
            # Return to top level menu
            END: SELECTING_ACTION,
            # End conversation altogether
            STOPPING: END,
        },
    )

    # Set up top level ConversationHandler (selecting action)
    # Because the states of the third level conversation map to the ones of the second level
    # conversation, we need to make sure the top level conversation can also handle them
    module_handlers = [
        organization_conv_handler,
        tasks_and_prs_conv_handler,
        # learn_conv_handler,
        # fun_conv_handler,
        # calendar_conv_handler,
        # add_member_conv,
        # CallbackQueryHandler(show_data, pattern="^" + str(SHOWING) + "$"),
        # CallbackQueryHandler(adding_self, pattern="^" + str(ADDING_SELF) + "$"),
        # CallbackQueryHandler(end, pattern="^" + str(END) + "$"),
    ]
    main_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECTING_ACTION: module_handlers,
            # SHOWING: [CallbackQueryHandler(start, pattern="^" + str(END) + "$")],
            # SELECTING_ACTION: selection_handlers,
            # SELECTING_LEVEL: selection_handlers,
            # DESCRIBING_SELF: [description_conv],
            STOPPING: [CommandHandler('start', start)],
        },
        fallbacks=[CommandHandler('stop', stop)],
    )

    application.add_handler(main_conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

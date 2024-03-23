from telegram import Update
from telegram.ext import ContextTypes


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
            LEARNING_BUTTON,
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
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from organization.configs.buttons import *
from organization.configs.messages import SELECT_ORGANIZATION_ACTION_TEXT


async def select_organization_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """You can see or change the information regarding your organization."""
    buttons = [
        [
            ADD_ORG_BUTTON,
            ADD_TEAM_BUTTON,
        ],
        [
            ADD_MEMBER_BUTTON,
            SHOW_ORG_BUTTON,
        ],
        [
            SHOW_TEAMS_BUTTON,
            SHOW_MEMBERS_BUTTON,
        ],
        [
            BACK_BUTTON,
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=SELECT_ORGANIZATION_ACTION_TEXT, reply_markup=keyboard)

    return ORGANIZATION

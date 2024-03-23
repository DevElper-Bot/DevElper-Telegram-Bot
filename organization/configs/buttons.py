from telegram import InlineKeyboardButton

from general.configs.states import END
from organization.configs.states import *

ADD_ORG_BUTTON = InlineKeyboardButton(text='Add new organization', callback_data=str(ORGANIZATION_ADD_ORG))
ADD_TEAM_BUTTON = InlineKeyboardButton(text='Add new team', callback_data=str(ORGANIZATION_ADD_TEAM))
ADD_MEMBER_BUTTON = InlineKeyboardButton(text='Add member', callback_data=str(ORGANIZATION_ADD_MEMBER))
SHOW_ORG_BUTTON = InlineKeyboardButton(text='Show organization info', callback_data=str(ORGANIZATION_SHOW_ORG))
SHOW_TEAMS_BUTTON = InlineKeyboardButton(text='Show your teams', callback_data=str(ORGANIZATION_SHOW_TEAMS))
SHOW_MEMBERS_BUTTON = InlineKeyboardButton(text='Show members', callback_data=str(ORGANIZATION_SHOW_MEMBERS))
BACK_BUTTON = InlineKeyboardButton(text='Back', callback_data=str(END))

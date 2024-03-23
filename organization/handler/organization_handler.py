from telegram.ext import ConversationHandler, CallbackQueryHandler, CommandHandler

from general.configs.states import SELECTING_ACTION, END, STOPPING
from general.handler.return_to_top_level_handler import return_to_top_level
from general.handler.stop_nested_handler import stop_nested
from organization.configs.states import *
from organization.handler.add_member_handler import add_member
from organization.handler.add_new_team_handler import add_new_team
from organization.handler.add_organization_handler import add_new_organization
from organization.handler.select_organization_action_handler import select_organization_action
from organization.handler.show_members_handler import show_members
from organization.handler.show_organization_handler import show_organization
from organization.handler.show_teams_handler import show_teams

organization_conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(select_organization_action, pattern='^' + str(ORGANIZATION) + '$')],
    states={
        ORGANIZATION: [
            CallbackQueryHandler(add_new_organization, pattern='^' + str(ORGANIZATION_ADD_ORG) + '$'),
            CallbackQueryHandler(add_new_team, pattern='^' + str(ORGANIZATION_ADD_TEAM) + '$'),
            CallbackQueryHandler(add_member, pattern='^' + str(ORGANIZATION_ADD_MEMBER) + '$'),
            CallbackQueryHandler(show_organization, pattern='^' + str(ORGANIZATION_SHOW_ORG) + '$'),
            CallbackQueryHandler(show_teams, pattern='^' + str(ORGANIZATION_SHOW_TEAMS) + '$'),
            CallbackQueryHandler(show_members, pattern='^' + str(ORGANIZATION_SHOW_MEMBERS) + '$'),
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

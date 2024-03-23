from telegram import InlineKeyboardButton

from general.configs.states import END
from tasks_and_prs.configs.states import *

TASKS_AND_PRS_BUTTON = InlineKeyboardButton(text='Tasks and PRs', callback_data=str(TASKS_AND_PRS))

NEW_REVIEW_BUTTON = InlineKeyboardButton(text='Request for PR review', callback_data=str(TASKS_AND_PRS_REVIEW_REQ))
REJECT_REVIEW_BUTTON = InlineKeyboardButton(text='Reject PR review', callback_data=str(TASKS_AND_PRS_REJECT_REVIEW))
FINISH_REVIEW_BUTTON = InlineKeyboardButton(text='Finish PR review', callback_data=str(TASKS_AND_PRS_FINISH_REV))
SHOW_PRS_BUTTON = InlineKeyboardButton(text='Show PRs', callback_data=str(TASKS_AND_PRS_SHOW_PRS))
BACK_BUTTON = InlineKeyboardButton(text='Back', callback_data=str(END))

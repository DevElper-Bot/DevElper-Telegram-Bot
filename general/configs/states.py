# Meta states
from telegram.ext import ConversationHandler

SELECTING_ACTION, STOPPING = map(chr, range(1, 3))
# Shortcut for ConversationHandler.END
END = ConversationHandler.END

# constants
START_OVER = chr(1000)

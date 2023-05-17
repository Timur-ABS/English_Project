from .start import start_command
from .echo import echo_message
from .help import help_command
from .text_message import message
from .leaderboard import leaderboard_command
from .game import callback_query_handler


def register_handlers(dp):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(leaderboard_command, commands=['leaderboard'])
    dp.register_message_handler(message)
    dp.register_callback_query_handler(callback_query_handler)

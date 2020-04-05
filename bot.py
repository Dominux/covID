import time
import datetime.datetime

from read_config import DATA
from action import Action
from errors import error_handler

# TODO продумать datetime

# @error_handler


def bot_run():
    # if datetime.now() == datetime.datetime():
    action = Action(DATA['regions'])
    action.post_statistic()


if __name__ == "__main__":
    while True:
        bot_run()
        time.sleep(DATA['relay_in_seconds'])

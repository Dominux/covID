import time

from action import Action
from errors import error_handler


@error_handler
def bot_run():
    action = Action(["Московская область"])
    action.execute()


if __name__ == "__main__":
    while True:
        bot_run()
        time.sleep(10)

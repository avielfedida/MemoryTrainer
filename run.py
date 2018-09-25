import os

from constants import DEFAULT_CATEGORY, AVAILABLE_MODES, SELF_PACE_MODE_POOL, SPEED_MODE_LIMIT, DEFAULT_STATS_DAYS
from db_manager import DbManager
from helpers import print_current_menu, get_digit
from keys import KEYS
from main import Main
from states import STTS
from terms_manager import TermsManager

STATE = STTS.MAIN  # Default state.
CATEGORY = DEFAULT_CATEGORY
MODE = AVAILABLE_MODES[0]

# DB manager object
dbManager = DbManager()


# Intermediaries functions
def set_mode_ret_state():
    global MODE
    state, mode = Main.move_to_mode_switch(AVAILABLE_MODES)
    if mode is not None:
        MODE = mode
    return state


def set_category_ret_state():
    global CATEGORY
    state, category = Main.move_to_category_switch(dbManager)
    if category is not None:
        CATEGORY = category
    return state


# Keys actions
keys_actions = {
    STTS.MAIN: {
        KEYS.ESC: lambda: Main.esc(dbManager),
        KEYS.ONE: lambda: Main.move_to_study_manager(dbManager, MODE, CATEGORY, SELF_PACE_MODE_POOL, SPEED_MODE_LIMIT),
        KEYS.TWO: Main.move_to_terms_manager,
        KEYS.THREE: lambda: Main.show_stats(dbManager, DEFAULT_STATS_DAYS),
        KEYS.FOUR: set_mode_ret_state,
        KEYS.FIVE: set_category_ret_state
    },
    STTS.TERMS_MANAGER: {
        KEYS.ONE: lambda: TermsManager.new_edit_term(dbManager, CATEGORY),
        KEYS.TWO: lambda: TermsManager.search(dbManager, CATEGORY),
        KEYS.ESC: TermsManager.esc
    }
}


def main():
    global STATE
    global CATEGORY
    mcc = dbManager.get_most_common_category()
    if mcc is not None:
        CATEGORY = mcc[0]
    while True:
        os.system('cls')
        print_current_menu(CATEGORY, MODE, STATE)
        key = get_digit(to=len(keys_actions.get(STTS.MAIN)), key=True)
        STATE = keys_actions.get(STATE).get(key, lambda: print('Some handler failed to return state'))()


if __name__ == '__main__':
    main()

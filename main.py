import os
import random

import matplotlib.pyplot as plt

from color_util import ColorUtil
from constants import MODE_SELF_PACE, MODE_SPEED
from helpers import enter_pause, ynq_esc, ynq, get_digit, get_text_char
from keys import KEYS
from states import STTS


class Main:
    @staticmethod
    def esc(db):
        # Insert Total weights / number of terms
        db.statistic_tick()
        exit()

    @staticmethod
    def show_stats(db, default_stats_days):
        os.system('cls')
        data = db.get_stats(default_stats_days)
        if len(data) == 0:
            enter_pause(
                ColorUtil.red(
                    'No data found, if data was added\n, statistics will update as soon as software closes\nBe advised that in order to see any tendency statistics require at least 2 days\npress Enter to continue',
                    string_only=True))
            return STTS.MAIN
        reversed_data = data[::-1]  # To iterate from oldest date to newest
        x_dates = []
        y_stats = []
        for o in reversed_data:
            x_dates.append(o[1])
            y_stats.append(o[0])
        plt.plot(x_dates, y_stats)
        plt.xticks(rotation=90)
        plt.xlabel('Date')
        plt.ylabel('Learning')
        plt.title('Statistics')
        plt.show()
        return STTS.MAIN

    @staticmethod
    def fetch_random_terms(db, global_category, how_many):
        terms = db.get_terms(global_category, how_many=how_many)
        ratios = [obj.get('ratio') for obj in terms]
        return random.choices(
            population=terms, weights=ratios, k=how_many)

    @staticmethod
    def print_responses(responses):
        wrap_text = ColorUtil.red('Enter to exit', string_only=True)
        # The wrapping with set is to remove duplicates in case single term appears more then once.
        enter_pause(wrap_text + '\n' + '\n'.join(set(responses)) + '\n' + wrap_text)

    @staticmethod
    def cls_and_esc_option():
        os.system('cls')
        print('Esc to finish\n')

    @staticmethod
    def move_to_study_manager(db, global_mode, global_category, self_pace_mode_pool, speed_mode_limit):
        if global_mode == MODE_SELF_PACE:
            Main.cls_and_esc_option()
            # Important note, I take the term_object in advance as they might not be here after the update because the
            # state might get update and the term won't exists anymore, hence I won't be able to fetch it's data
            term_object = Main.fetch_random_terms(db, global_category, self_pace_mode_pool)[0]
            category, term, answer = term_object.get('category'), term_object.get('term'), term_object.get('answer')
            response = ColorUtil.green('The answer is: \n', string_only=True) + answer
            q = ynq_esc('Remember {}?'.format(ColorUtil.yellow(term, string_only=True)))
            if q == KEYS.ESC:
                return STTS.MAIN
            elif q:
                db.update_appeared(category, term)
            else:
                db.update_wrong_and_appeared(category, term)
            print(response)
            if ynq(ColorUtil.red('\nNext?', string_only=True)):
                return Main.move_to_study_manager(db, global_mode, global_category, self_pace_mode_pool,
                                                  speed_mode_limit)
        elif global_mode == MODE_SPEED:
            terms = Main.fetch_random_terms(db, global_category, how_many=speed_mode_limit)
            responses = []
            wrong_terms = []
            appeared_terms = []
            for term_object in terms:
                Main.cls_and_esc_option()
                category, term, answer = term_object.get('category'), term_object.get('term'), term_object.get('answer')
                q = ynq_esc('Remember {}?'.format(ColorUtil.yellow(term, string_only=True)))
                if q == KEYS.ESC:
                    db.update_many_wrong_appeared(global_category, appeared_terms, wrong_terms)
                    if len(responses) > 0:
                        Main.print_responses(responses)
                    return STTS.MAIN
                elif not q:
                    wrong_terms.append(term)
                    responses.append(
                        ColorUtil.green('The answer for {} is: \n'.format(term), string_only=True) + answer)
                appeared_terms.append(term)
            db.update_many_wrong_appeared(global_category, appeared_terms, wrong_terms)
            if len(responses) > 0:
                Main.print_responses(responses)
            return STTS.MAIN
        else:
            raise Exception('Invalid mode: {}'.format(global_mode))
        return STTS.MAIN

    @staticmethod
    def move_to_mode_switch(available_modes):
        os.system('cls')
        print('\n'.join('{}) {}'.format(str(i + 1), mode) for i, mode in enumerate(available_modes)))
        d = get_digit(to=len(available_modes))
        mode = None
        if d != KEYS.ESC:
            mode = available_modes[d - 1]
        return STTS.MAIN, mode

    @staticmethod
    def move_to_category_switch(db, category='', msg='', idx=0,
                                prev_call_results=None):  # The default is to prevent having to specify it within the key_actions
        os.system('cls')
        if len(msg) > 0:
            ColorUtil.red(msg)
        print('Type(ESC to return, Enter to switch category): {}'.format(category))
        search_results = prev_call_results or [cols[0] for cols in db.search_category(category)]
        if len(search_results) > 0:
            print('\n--------------Categories--------------\n')
            if 0 <= idx < len(search_results):
                for i, v in enumerate(search_results):
                    if i != idx:
                        print(v)
                    else:
                        ColorUtil.yellow(v)

        elif len(category) == 0:
            ColorUtil.red('There are no categories at all(no terms at all)')
        else:
            ColorUtil.red('There are no matching categories')

        c = get_text_char(up_down_arrows=True)
        if c == KEYS.SPACE:
            return Main.move_to_category_switch(db, category=category + ' ')
        elif c == KEYS.DA:
            return Main.move_to_category_switch(db, category=category,
                                                idx=idx + 1 if idx + 1 < len(search_results) else idx,
                                                prev_call_results=search_results)
        elif c == KEYS.UA:
            return Main.move_to_category_switch(db, category=category, idx=idx - 1 if idx - 1 >= 0 else idx,
                                                prev_call_results=search_results)
        elif c == KEYS.BACKSPACE:
            return Main.move_to_category_switch(db, category=category[0:-1])
        elif c == KEYS.ESC:
            return STTS.MAIN, None
        elif c == KEYS.ENTER:
            if len(search_results) > 0:
                return STTS.MAIN, search_results[idx]
            else:
                return Main.move_to_category_switch(db, category=category, idx=idx, prev_call_results=search_results)
        else:
            return Main.move_to_category_switch(db, category=category + c)

    @staticmethod
    def move_to_terms_manager():
        return STTS.TERMS_MANAGER

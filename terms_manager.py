import os

from color_util import ColorUtil
from helpers import trimmer, sfi, print_category_list, print_alike_terms, ynq, multiline_input, enter_pause, \
    get_text_char
from keys import KEYS
from states import STTS


class TermsManager:
    @staticmethod
    def new_edit_term(db, global_category, term_object=None):
        os.system('cls')
        change = False
        if term_object is not None:
            print(trimmer("""
            Blank fields won't update the field.
            Category: {}
            Term: {}
            Answer:
            ------------
            {}
            ------------
            """).format(term_object.get('category'), term_object.get('term'), term_object.get('answer')))

        default_category = global_category if term_object is None else term_object.get('category')
        categories = db.get_categories_list()
        if len(categories) > 0:
            print_category_list(categories)
        category = sfi('Category[leave blank for {}]: '.format(default_category))
        if category:
            change = True
        else:
            category = default_category

        term = sfi(
            'Term[leave blank {}]: '.format('to abort' if term_object is None else 'for ' + term_object.get('term')))
        if term:
            alike_terms = db.terms_list(term, category)
            at_len = len(alike_terms)
            if at_len > 0:
                print_alike_terms(alike_terms)
            change = True
        elif term_object is None:
            return STTS.TERMS_MANAGER
        else:
            term = term_object.get('term')

        if change:
            term_category_exists = db.get_term(category, term)
            if term_category_exists:
                if ynq('{}@{} already exists, edit this term(term typo fix/change category/reset interaction stats)?'
                               .format(term, category)):
                    return TermsManager.new_edit_term(db, global_category,
                                                      term_object=term_category_exists)  # Restart the update for this object
                else:
                    return STTS.TERMS_MANAGER
        answer = multiline_input('Answer[leave blank to {}]: '
                                 .format('abort' if term_object is None else 'keep current answer'))
        if answer:
            change = True
        elif term_object is None:
            return STTS.TERMS_MANAGER
        else:
            answer = term_object.get('answer')

        if term_object is None:
            inserted = db.insert(category, term, answer)
            if not inserted:
                print('Insertion failed, please check logs')
                enter_pause('Press ENTER to continue')
        else:
            q = ynq('Would you like to reset {}@{} stats?'.format(term, category))
            if change:
                update_succeeded = db.update_term(term_object.get('rowid'), category,
                                                         term, answer, reset_stats=q)
                if not update_succeeded:
                    print('Update failed, please check logs')
                    enter_pause('Press ENTER to continue')

        return STTS.TERMS_MANAGER

    @staticmethod
    def search(db, global_category, search_for='', msg='', idx=0, prev_call_results=None):
        os.system('cls')
        if len(msg) > 0:
            ColorUtil.red(msg)
        print('Type(ESC to return, Enter to edit, Del to delete): {}'.format(search_for))
        search_results = []
        if len(search_for) > 0:
            print('\n--------------Results--------------\n')
            search_results = prev_call_results or [cols[0] for cols in
                                                   db.search_term(search_for, global_category)]
            if 0 <= idx < len(search_results):
                for i, v in enumerate(search_results):
                    if i != idx:
                        print(v)
                    else:
                        ColorUtil.yellow(v)
        c = get_text_char(with_delete=True, up_down_arrows=True)
        if c == KEYS.SPACE:
            return TermsManager.search(db, global_category, search_for=search_for + ' ')
        elif c == KEYS.DA:
            return TermsManager.search(db, global_category, search_for=search_for,
                                       idx=idx + 1 if idx + 1 < len(search_results) else idx,
                                       prev_call_results=search_results)
        elif c == KEYS.UA:
            return TermsManager.search(db, global_category, search_for=search_for, idx=idx - 1 if idx - 1 >= 0 else idx,
                                       prev_call_results=search_results)
        elif c == KEYS.BACKSPACE:
            return TermsManager.search(db, global_category, search_for=search_for[0:-1])
        elif c == KEYS.DELETE:  # Del keypress
            err_msg = ''
            if search_results is not None and len(search_results) == 0:
                err_msg = 'Nothing to delete'
            elif not db.delete_term(search_results[idx], global_category):
                err_msg = 'Failed to delete {}@{}, please check logs'.format(search_for, global_category)
            return TermsManager.search(db, global_category, search_for=search_for, msg=err_msg)
        elif c == KEYS.ESC:
            return STTS.TERMS_MANAGER
        elif c == KEYS.ENTER:
            if search_results is not None and len(search_results) == 0:
                return TermsManager.search(db, global_category, search_for=search_for, msg='Nothing to edit')
            return TermsManager.new_edit_term(db, global_category, term_object=db.get_term(global_category, search_results[idx]))
        else:
            return TermsManager.search(db, global_category, search_for=search_for + c)

    @staticmethod
    def esc():
        return STTS.MAIN

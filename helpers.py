import re
# Remove the spaces got me to write string such as:
from msvcrt import getch

from keys import KEYS, Num2Key, Key2Num
from menus import MENUS

"""
Prevent using printing functions:
STUCK TO THE LEFT :(
to prevent tabs
"""


def trimmer(s):
    return re.sub('^ +', '', s, flags=re.MULTILINE)


def print_current_menu(global_category, global_mode, state):
    print('category: {}, mode: {}'.format(str.capitalize(global_category), str.capitalize(global_mode)))
    print(trimmer(MENUS.get(state)))


# Skip 0 or the special 224
# Special keys (arrows, f keys, ins, del, etc.) so I need
# to get the key again(https://stackoverflow.com/questions/12175964/python-method-for-reading-keypress).
# The default lambda is used for example for arrow keys used in the terms manager
def get_char_key():
    key = KEYS.ZERO
    while key == KEYS.ZERO or key == KEYS.SPECIAL:
        key = ord(getch())
    return key


def get_char():
    key = KEYS.ZERO
    c = None
    while key == KEYS.ZERO or key == KEYS.SPECIAL:
        c = getch()
        key = ord(c)
    return c.decode("utf-8")


# Esc to exit, key is used to return the digit or digit key.
def get_digit(fr=1, to=9, key=False):
    if to < 1 or to > 9 or fr < 1 or fr > 9 or fr > to:
        raise Exception('Invalid parameters')
    k = get_char_key()
    # the to+1 is because range will go from start to end-1, so range(1,3) is 1 and 2 only!
    rng = [Num2Key.get(s) for s in range(fr, to + 1)]
    rng.append(KEYS.ESC)
    while k not in rng:
        k = get_char_key()
    if key or k == KEYS.ESC:
        return k
    return Key2Num.get(k)


# If key is not returned, then decoded bytes returned as text(char A-z is returned).
def get_text_char(with_delete=False, up_down_arrows=False):
    # The last_key is used due to special characters go into the character range but proceed with 224 key before,
    # for example, Delete=224,83 is within A-Z range, so just checking
    # 83 will go into the A-z if, so I have to check 224
    last_key = None
    key = None
    c = None
    while key is None or key == KEYS.ZERO or key == KEYS.SPECIAL:
        c = getch()
        last_key = key
        key = ord(c)
    if last_key != KEYS.SPECIAL and (
            KEYS.A2z[0][0] <= key <= KEYS.A2z[0][1] or KEYS.A2z[1][0] <= key <= KEYS.A2z[1][1]):
        return c.decode("utf-8")
    elif key == KEYS.BACKSPACE:
        return KEYS.BACKSPACE
    elif key == KEYS.SPACE:
        return KEYS.SPACE
    elif key == KEYS.ESC:
        return KEYS.ESC
    elif last_key == KEYS.SPECIAL and key == KEYS.DELETE and with_delete:
        return KEYS.DELETE
    elif key == KEYS.ENTER:
        return KEYS.ENTER
    elif last_key == KEYS.SPECIAL and (key == KEYS.UA or key == KEYS.DA) and up_down_arrows:
        return key
    else:
        return get_text_char(with_delete=with_delete, up_down_arrows=up_down_arrows)


def enter_pause(msg):
    input(msg)


def multiline_input(pretext):
    print(pretext + '(Double Enter end): ')
    contents = []
    try:
        inp = input()
        while inp.strip():
            contents.append(inp)
            inp = input()
        fin = ('\n'.join(contents)).strip()
        return fin if len(fin) > 0 else False
    except KeyboardInterrupt:
        return False


def print_alike_terms(terms_list):
    print('Alike terms: ' + ', '.join(cols[0] for cols in terms_list))


def print_category_list(categories_list):
    print('Known categories: ' + ', '.join(cols[0] for cols in categories_list))


# Here Esc is the same as no=left arrow
def ynq(txt):
    print(txt)
    while True:
        key = get_char_key()
        if key in (KEYS.RA, KEYS.LA, KEYS.ESC):
            break
    return key == KEYS.RA


# Similar to ynq, here I return Esc
def ynq_esc(txt):
    print(txt)
    while True:
        key = get_char_key()
        if key in (KEYS.RA, KEYS.LA, KEYS.ESC):
            break
    if key == KEYS.RA:
        return True
    if key == KEYS.LA:
        return False
    return KEYS.ESC


# Stripped False input
def sfi(msg):
    i = input(msg).strip()
    return i if len(i) > 0 else False

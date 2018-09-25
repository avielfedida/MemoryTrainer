class KEYS:
    DELETE = 83
    ENTER = 13
    ESC = 27
    ONE = 49
    TWO = 50
    THREE = 51
    FOUR = 52
    FIVE = 53
    SIX = 54
    SEVEN = 55
    EIGHT = 56
    NINE = 57
    SPECIAL = 224
    ZERO = 0
    LA = 75
    RA = 77
    UA = 72
    DA = 80
    A2z = [(65, 90), (97, 122)]
    BACKSPACE = 8
    SPACE = 32


Key2Num = {
    KEYS.ONE: 1,
    KEYS.TWO: 2,
    KEYS.THREE: 3,
    KEYS.FOUR: 4,
    KEYS.FIVE: 5,
    KEYS.SIX: 6,
    KEYS.SEVEN: 7,
    KEYS.EIGHT: 8,
    KEYS.NINE: 9
}
# Create the reverse
Num2Key = {v: k for k, v in Key2Num.items()}
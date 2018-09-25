class ColorUtil:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    LIGHT_PURPLE = '\033[94m'
    PURPLE = '\033[95m'
    END = '\033[0m'

    @staticmethod
    def main(color, s, string_only=False):
        cs = color + s + ColorUtil.END
        if string_only:
            return cs
        print(cs)

    @staticmethod
    def red(s, string_only=False):
        return ColorUtil.main(ColorUtil.RED, s, string_only=string_only)

    @staticmethod
    def green(s, string_only=False):
        return ColorUtil.main(ColorUtil.GREEN, s, string_only=string_only)

    @staticmethod
    def yellow(s, string_only=False):
        return ColorUtil.main(ColorUtil.YELLOW, s, string_only=string_only)

    @staticmethod
    def light_purple(s, string_only=False):
        return ColorUtil.main(ColorUtil.LIGHT_PURPLE, s, string_only=string_only)

    @staticmethod
    def purple(s, string_only=False):
        return ColorUtil.main(ColorUtil.PURPLE, s, string_only=string_only)

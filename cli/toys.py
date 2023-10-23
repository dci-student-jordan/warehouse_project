# toys
import time, sys


def glued_string(add_glue):
    """Takes a string and returns it prefixed with 'A' or 'An'
    according to the first character being a vowel or an h or not."""
    vowels = "aeiouh"
    return f"An {add_glue.lower()}" if add_glue[0].lower() in vowels else f"A {add_glue.lower()}"


class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALIC = '\x1B[3m'
    END = '\033[0m'


class PrinterToy():

    def __init__(self, speed: float) -> None:
        self.print_speed = speed

    def print_like_typed(self, message:str):
        for i in range(len(message)):
            sys.stdout.write(message[i])
            sys.stdout.flush()
            time.sleep(self.print_speed)

    def set_print_speed(self, speed: float):
        """takes a string an prints it letter by letter
        at the given print speed"""
        self.print_speed = speed

    def print_line_by_line(self, lines: list):
        """takes a list of strings and prints them one after another
        at the given print speed"""
        for line in lines:
            print(line)
            time.sleep(self.print_speed)
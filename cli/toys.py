# toys
import time, sys, getch

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
        """takes a string an prints it letter by letter
        at the given print speed"""
        for i in range(len(message)):
            sys.stdout.write(message[i])
            sys.stdout.flush()
            time.sleep(self.print_speed)

    def set_print_speed(self, speed: float):
        """sets the time for the pause between prints."""
        self.print_speed = speed

    def print_line_by_line(self, lines: list):
        """takes a list of strings and prints them one after another
        at the given print speed"""
        for line in lines:
            print(line)
            time.sleep(self.print_speed)

    def print_error(self):
        print(Color.FAIL + "\nError: The operation you entered is not valid." + Color.END)

def option_or_login_input(mess, employee_candidate):
    """An alternative input for y or n or a potential password for the Employee class.
    Takes a message string to be printed and an Employee object.
    When input ends with new line, returns 'y', 'n', None or the successfully authenticated Employee object."""
    print(mess, end="", flush=True)
    observe_input = True
    log_in = ""
    while observe_input:
        log_in = log_in+getch.getch()
        if log_in == "y" or log_in == "n":
            print(log_in, end="", flush=True)
        elif log_in == "y\n" or log_in == "n\n":
            log_in = log_in[:1]
            observe_input = False
            print("") # stop inline print
            return log_in
        else:
            if log_in[-1:] == "\n":
                if employee_candidate.authenticate(log_in[:-1]):
                    print("\n") # stop inline print
                    return employee_candidate
                else:
                    observe_input = False
                    print("\n") # stop inline print
                    return None
            else:
                print("*", end="", flush=True)
"""Provides the classes Item, Warehouse, User and Employee."""

from datetime import datetime as dt
from toys import Color, PrinterToy, glued_string, option_or_login_input
import time
from load_jsons import Loader
import pwinput as pw
import os

printer = PrinterToy(0.0005)


class Item():
    """Class for the items in a warehouse."""

    def __init__(self, state: str, category: str,
                 warehouse: int, date_of_stock: dt) -> None:
        """Initialize the obligate information."""
        self.state = state
        self.category = category
        self.warehouse = warehouse
        self.date_of_stock = date_of_stock

    # Make the items comparable as strings
    def __str__(self) -> str:
        """Return a string of state and category."""
        return f"{self.state} {self.category}"


class Warehouse():
    """Class for each warehouse."""

    def __init__(self, id=0) -> None:
        """Initialize with id, else it's None."""
        if int(id) > 0:
            self.id = id
        else:
            self.id = None
        self.stock = []
        self.items_of_interest = {}

    def occupancy(self) -> int:
        """Return the number of items in the stock."""
        return len(self.stock)

    def add_item(self, item: Item):
        """Add an Item to the stock."""
        self.stock.append(item)

    def search(self, search_term: str) -> list:
        """Take a search term and return matches as list."""
        if search_term not in self.items_of_interest:
            # clear
            self.items_of_interest = {}
            # recreate (I do so to prevent recreation in
            # case of twice the same interest entered without order)
            self.items_of_interest[search_term] = \
                [x for x in self.stock
                    if search_term.lower() in str(x).lower()]
        return self.items_of_interest[search_term]

    def __str__(self) -> str:
        """Return a name as string."""
        return f"Warehouse{self.id}"

    def list_warehouse(self):
        """Print the stock items and their afterwards."""
        print(Color.OKBLUE + "Here's a list of our products" +
              f"in", str(self), ":\n" + Color.END)
        printer.print_line_by_line(self.stock)
        print(Color.OKGREEN + f"\nTotal amount of items in " +
              f"{str(self)}: {self.occupancy()}.\n" + Color.END)
        time.sleep(printer.print_speed*600)

    def print_interest_with_days_in_stock(self, interest):
        """
        Print each item of interest.

        Information of its location
        and the days it is in the stock is added.
        """
        if self.items_of_interest[interest]:
            today = dt.now()
            for match in self.items_of_interest[interest]:
                days_in_stock = today - \
                    dt.strptime(match.date_of_stock, "%Y-%m-%d %H:%M:%S")
                print(f" {glued_string(str(match))} located in " +
                      Color.UNDERLINE + str(self) + Color.END +
                      f" (in stock for {days_in_stock.days} days)")
                time.sleep(printer.print_speed)


class User():
    """Class for creating a user."""

    def __init__(self, user_name: str, *args) -> None:
        """I no name given, name will be 'Anonymous'."""
        self._name = "Anonymous" \
            if not len(user_name) else user_name
        self.is_authenticated = False

    def authenticate(self, password: str):
        """Will always return False for users."""
        return False

    def validate_user(self, *args):
        """
        Log in as Employee.

        Takes a User class, compares the name
        with the registered users,
        offers the option to change the name if not
        and asks for the password.
        Returns Employee if successfully authenticated
        or None
        """
        personnel = Loader(model="personnel") \
            if len(args) < 1 else args[0]
        print("PERSONNEL:", *personnel)
        personnel_names = \
            [str(x) for x in personnel] if len(args) < 2 else args[1]
        print("\nNAMES:", personnel_names)
        employee_candidate = None

        def ask_password(mess):
            """
            Log in function.

            If authentication succeeds,
            returns an authenticated Employee class.
            """
            nonlocal self, employee_candidate
            printer.print_like_typed(mess)
            password = pw.pwinput(mask="*")
            if not employee_candidate:
                for staff in personnel:
                    if staff.is_named(str(self)):
                        employee_candidate = staff
                        if staff.authenticate(password):
                            # here we return an authenticated Employee
                            return staff
                        break
            # wrong password, try again
            invite = Color.FAIL + f"Sorry, {str(self)}, that wasn't right." + \
                Color.END + "\nWanna try again? (y/n/pwd): "
            ask_again = option_or_login_input(invite, employee_candidate)
            if isinstance(ask_again, Employee):
                return ask_again
            elif ask_again == "y":
                return ask_password("Please enter your correct password, " +
                                    f"{str(self)}: ")
            elif not ask_again == "n":
                # wrong input or refusal
                printer.print_error()
                return None
        if str(self) in personnel_names:
            # login
            return ask_password("Please log in with your password, " +
                                f"{str(self)}. ")
        else:
            # option to change name
            change_name = input(f"You're not registered, {str(self)}, " +
                                "wanna change your name? (y/n): ")
            if change_name == "y":
                # recreate User object with new name
                self = User(input("Ok, whats your login-name, then? "))
                return self.validate_user()
            elif change_name in personnel_names:
                # also accept a name if in personnel
                # and retry validation with new User object
                self = User(change_name)
                return self.validate_user()
            elif not change_name == "n":
                # invalid input, get out of here
                printer.print_error()
                return None

    def is_named(self, name: str):
        """
        Compare with the classes name variable.

        Take a name as string and return a boolean
        comparing it with the objects name variable.
        """
        return name == self._name

    def greet(self):
        """Print a greeting for the user."""
        greeting = "\n" + Color.ITALIC + f"Hello, {self._name}!\n" + \
            "Welcome to our Warehouse Database.\n" + \
            "If you don't find what you are looking for,\n" + \
            "please ask one of our staff members to assist you." + \
            Color.END + "\n"
        printer.print_like_typed(greeting)

    def bye(self, actions: list):
        """
        Finish the shopping session.

        Takes a list of actions to be stored in log/User.log
        """
        # Thank the user for the visit
        print(Color.WARNING + f"\nOk then, {self._name}, " +
              "thanks for your visit, we hope to see you soon!" +
              Color.END)
        # store actions in log file
        log_file_name = self.__class__.__name__+".log"
        # check for log folder to be present
        if "log" not in os.listdir("."):
            os.makedirs("log")
        # create line to append to logfile:
        action_string = str(self)+": "
        for action in actions:
            action_string = action_string+action+" "
        # write to file
        with open(os.path.join("log", log_file_name), "a") as writer:
            writer.write(action_string+f"({dt.now()})\n")

    def __str__(self) -> str:
        """Make the class printable."""
        return self._name

    def __repr__(self) -> str:
        """Make the class callable as string."""
        return self._name


class Employee(User):
    """Class for authenticated Employees."""

    def __init__(self, user_name: str, password: str, **args) -> None:
        """Password required for initialization."""
        if password:
            self.__password = password
        if "head_of" in args:
            self.head_of = \
                [Employee(**employee) for employee in args["head_of"]]
        else:
            self.head_of = None if not password else []
        super().__init__(user_name)

    def authenticate(self, password: str):
        """
        Authenticate with password.

        Takes a string and
        returns a boolean comparing it
        with the objects private password string
        """
        if not password == "":
            self.is_authenticated = (password == self.__password)
        return self.is_authenticated

    # def potential_authentication(self, pwd):
    #     return pwd == self.__password[:len(pwd)]

    # def order(self, item: Item, amount: int):
    #     """print successful order with amount only."""
    #     # print successful order
    #     items = "item" if amount == 1 else "items"
    #     mess = Color.OKGREEN + \
    #         f"\nThe order for {amount} {item} {items} " + \
    #             "has ben placed." + Color.END
    #     print(mess)

    def greet(self):
        """Print a different greeting for the Employee."""
        greeting = "\n" + Color.ITALIC + f"Hello, {self._name}!\n" + \
            "If you experience a problem with the system,\n" + \
            "please contact technical support." + Color.END + "\n"
        printer.print_like_typed(greeting)

    def bye(self, actions: list):
        """
        Finish the shopping session.

        Takes a list of actions to be stored in log/Employee.log
        """
        super().bye(actions)
        print(Color.ITALIC + "In this session you have", end="")
        if actions:
            print(":" + Color.END)
            printer.print_line_by_line(actions)
        else:
            print(" done nothing special." + Color.END)

    def order_item(self, max_items, order, interest):
        """
        Order items if available.

        Takes an int for the maximum available items,
        a string representing either the number of items to be ordered
        or simply the request to do so ('y')
        and the users interest as string
        and places the order.
        Returns an int of the successful ordered items.
        """
        # order needs amount:
        if not order.isdigit():
            order = input(f"How many {interest} items " +
                            "do you want to purchase? (number): ")
        if not order.isdigit():
            # invalid input
            printer.print_error()
            return 0
        else:
            # try to order either requested amount...
            if int(order) > max_items:
                order = max_items
                try_again = Color.FAIL + \
                    "Error: Your requested too many items, " + \
                    "do you want to order the maximum " + \
                    f"of {max_items} {interest} items " + \
                    "instead? (y/n): " + Color.END
                reorder = input(try_again)
                if not reorder.lower() == "y":
                    # ... or give up
                    return 0
            # print successful order
            items = "item" if order == "1" else "items"
            congrats = Color.OKGREEN + "\nCongratulation! Your order " + \
                f"for {order} {interest} {items} has ben placed." + Color.END
            print(congrats)
            return int(order)

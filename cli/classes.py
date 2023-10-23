from datetime import datetime as dt
from toys import Color, PrinterToy, glued_string
import time

printer = PrinterToy(0.0005)

class WarehouseItem():

    def __init__(self, state: str, category: str, warehouse: int, date_of_stock: dt) -> None:
        self.state = state
        self.category = category
        self.warehouse = warehouse
        self.date_of_stock = date_of_stock

    # Make the items comparable as strings
    def __str__(self) -> str:
        return f"{self.state} {self.category}"
    

class Warehouse():

    def __init__(self, id: int) -> None:
        self.id = id
        self.stock = []
        self.items_of_interest = {}

    def occupancy(self) -> int:
        '''Return the number of items in the stock.'''
        return len(self.stock)
    
    def add_item(self, item: WarehouseItem):
        '''Add an Item to the stock.'''
        self.stock.append(item)

    def search(self, search_term: str) -> list:
        '''Take a search term and return matches as list.'''
        if not search_term in self.items_of_interest:
            # clear
            self.items_of_interest = {}
            # recreate
            self.items_of_interest[search_term] = [x for x in self.stock if search_term.lower() in str(x).lower()]
        return self.items_of_interest[search_term]
    
    def __str__(self) -> str:
        return f"Warehouse{self.id}"
    
    def list_warehouse(self):
        """Prints the stock items
        and the sum of items afterwards."""
        print(Color.OKBLUE + "Here's a list of our products in", str(self), ":\n" + Color.END)
        printer.print_line_by_line(self.stock)
        print(Color.OKGREEN + f"\nTotal amount of items in {str(self)}: {self.occupancy()}\n" + Color.END)

    def print_interest_with_days_in_stock(self, interest):
        """Prints each item of interest with its location
        and the days it is in the stock"""
        if self.items_of_interest[interest]:
            today = dt.now()
            for match in self.items_of_interest[interest]:
                    days_in_stock = today - dt.strptime(match.date_of_stock, "%Y-%m-%d %H:%M:%S")
                    print(f" {glued_string(str(match))} located in " +Color.UNDERLINE + "Warehouse"+str(self) + Color.END + f" (in stock for {days_in_stock.days} days)")
                    time.sleep(printer.print_speed)
    

class User():

    def __init__(self, user_name: str) -> None:
        self._name = "Anonymous" if not len(user_name) else user_name
        self.is_authenticated = False

    def authenticate(self, password: str):
        return False
    
    def is_named(self, name: str):
        return name == self._name
    
    def greet(self):
        printer.print_like_typed("\n" + Color.ITALIC + f"Hello, {self._name}!\n"+\
        "Welcome to our Warehouse Database.\n"+\
        "If you don't find what you are looking for,\n"+\
        "please ask one of our staff members to assist you." + Color.END + "\n")

    def bye(self, actions:list):
        # Thank the user for the visit
        print(Color.WARNING + f"\nOk then, {self._name}, thanks for your visit, we hope to see you soon!" + Color.END)

    def __str__(self) -> str:
        return self._name

class Employee(User):

    def __init__(self, user_name: str, password: str, **args) -> None:
        self.__password = password
        if "head_of" in args:
            self.head_of = args["head_of"]
        super().__init__(user_name)

    def authenticate(self, password: str):
        # print("trying to log in")
        return password == self.__password
    
    def order(item: WarehouseItem, amount: int):
        # print successful order
        items = "item" if amount == 1 else "items"
        print(Color.OKGREEN + f"\nThe order for {amount} {item} {items} has ben placed." + Color.END)

    def greet(self):
        printer.print_like_typed("\n" + Color.ITALIC + f"Hello, {self._name}!\n"+\
        "If you experience a problem with the system,\n"+\
        "please contact technical support." + Color.END + "\n")

    def bye(self, actions: list):
        super().bye(actions)
        if actions:
            print(Color.ITALIC + "In this session you have:" + Color.END)
            printer.print_line_by_line(actions)
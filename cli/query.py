"""Command line interface to query the stock.

To iterate the source data you can use the following structure:

for item in warehouse1:
    # Your instructions here.
    # The `item` name will contain each of the strings (item names) in the list.
"""

import time, sys, datetime
from classes import User, Employee
from loader import Loader
from toys import Color, PrinterToy, glued_string


printer = PrinterToy(0.0005)

stock = Loader(model="stock")

# Show the menu and ask to pick a choice
def get_selected_operation():
    """Shows a menu of options and asks for input,
    returns the choice as string"""
    printer.print_like_typed("\nHere you can chose from one of three options:\n\n1. List items by warehouse,\n2. Search an item and place an order\n3. Browse items by category\n4. Quit.\n\n")
    return input("Which of these options do you want to chose? (1/2/3/4): ")


def print_search_results(interest):
    """Takes a string, prints out matching search results
    and returns the number of matches in all warehouses"""
    total_items = 0
    most_items_warehouse = ""
    max_items = 0
    num_warehouses = 0
    for warehouse in stock:
        warehouse.search(interest)
        length = len(warehouse.items_of_interest[interest])
        max_items = max_items if max_items > length else length
        total_items += length
        most_items_warehouse = most_items_warehouse if length < max_items else str(warehouse)

    if total_items == 0:
        # not found
        print("Sorry, but that's not in stock.")
    else:
        for warehouse in stock:
            warehouse.print_interest_with_days_in_stock(interest)
        print(Color.BOLD + f"\nWe have {total_items} offers for you", end="")
        if num_warehouses == 1:
            # only in one warehouse
            print(" in", most_items_warehouse)
        else:
            print(" in our warehouses!")
            print(Color.BOLD + f"In {most_items_warehouse} you find the most ({max_items}):\n" + Color.END)
    return total_items


def search_item():
    """Asks user to input his interest,
    makes a call to print matching results,
    asks whether to place an order and starts it in case,
    finally returns the interest as string or None if order is refused"""
    # ask for interest
    interest = input("What are you looking for? (eg. Monitor, elegant, Second Hand...): ")
    # print all matches
    search_results = print_search_results(interest)
    order_successful = False
    if search_results:
        # ask whether to place an order
        if_order = input("Do you want to place an offer? (y/n): ")
        # a number is also accepted...
        if (if_order == "y" or if_order.isdigit()):
            global username
            if not username.is_authenticated:
                validation = username.validate_user()
                if (validation):
                    username = validation
                else:
                    return
            # start the order
            order_successful = username.order_item(search_results, if_order, interest)
            if order_successful:
                return f"Ordered {order_successful} {interest} items." if order_successful > 1 else f"Ordered {glued_string(interest).lower()} item."
        elif not if_order == "n":
            printer.print_error()
    if not order_successful:
        return f"Searched {glued_string(interest).lower()} item." if not (interest == "n") else None

def browse_by_category():
    """sorts items in all warehouses by category,
    prints the category as list of options to search,
    takes an input to search a category
    prints out the asked items
    and returns the asked category name as string"""
    # create categories dictionary
    categories = {}
    def create_categories(warehouse_stock):
        for item in warehouse_stock:
            category_dict_item = str(item) + ", found in Warehouse " + str(item.warehouse)
            if not item.category in categories:
                num_categories = len(categories) + 1
                # key = category name
                # value = [input_selection_number, [list_with_item_string for later use]]
                # BEWARE: first category-dictionary-item is the input selection!
                categories[item.category] = [num_categories, [category_dict_item]]
            else:
                categories[item.category][1].append(category_dict_item)

    for warehouse in stock:
        create_categories(warehouse.stock)
    # print out the options for searching a category
    options = "("
    print(Color.OKCYAN + "\nHere's a list of available categories:\n" + Color.END)
    for category in categories:
        option = categories[category][0]
        options = options + (str(option) + "..." if option == 1 else "" if not option == len(categories) else str(option) + "): ")
        print(f"{option}. {category} ({len(categories[category][1])})")
    # aks for input (number) which category to search
    browse = input(Color.OKCYAN + "\n" + f"Which category do you want to browse? {options}" + Color.END)
    # print items in the category or let an error be shown for invalid input
    if browse.isdigit() and int(browse) <= len(categories) and int(browse) > 0:
        # first get the category name
        category = ""
        for cat in categories:
            if categories[cat][0] == int(browse):
                category = cat
                break
        # print out he items
        print(Color.BOLD + f"\nHere is a list of all items in category '{category.lower()}' of all our warehouses:\n" + Color.END)
        for item in categories[category][1]:
            print(glued_string(str(item)))
        return category
    else:
        printer.print_error()


#### the shopping loop ####

shopping_actions = []
def go_shopping():
    shopping = True
    # Get the user selection
    operation = get_selected_operation()
    # If they pick 1
    if operation == "1":
        total_items = 0
        for warehouse in stock:
            total_items += warehouse.occupancy()
            warehouse.list_warehouse()
        print(f"Listed {total_items} items of our {len(list(stock))} warehouses.")
        shopping_actions.append(f"Listed the {total_items} items of our {len(list(stock))} warehouses.")
    # Else, if they pick 2
    elif operation == "2":
        search = search_item()
        if search:
            shopping_actions.append(search)
    # Else, if they pick 3
    elif operation == "3":
        category = browse_by_category()
        if category:
            shopping_actions.append(f"Browsed the category {category}.")
    # Else quit, with error in case of invalid input
    elif not operation == "4":
        printer.print_error()
    else:
        shopping = False

    if shopping:
        shop_on = input(Color.OKCYAN + "\nDo you want to explore our warehouse 2.0 some more? (y/n): " + Color.END)
        if shop_on.lower() == "y":
            go_shopping()
        elif shop_on == "n":
            pass
        else:
            printer.print_error()
            go_shopping()


################## HERE WE GO: ##################

# Get the user name
username = User(input("Please enter your name here: "))
# Greet him
username.greet()
# send him into nirvana:
go_shopping()
# Thank the user for the visit
username.bye(shopping_actions)
"""Command line interface to query the stock."""

from classes import User, Employee
from load_jsons import Loader
from save_jsons import write_stock_to_json, create_jsons_from_data
from toys import Color, PrinterToy, glued_string, option_or_login_input


def check_for_globals():
    # needed for testing actually the hardcoded data.py values
    if not "printer" in globals():
        # first make sure the json data is available
        globals()["printer"] = PrinterToy(0.0005)
    if not "stock" in globals():
        # first make sure the json data is available
        create_jsons_from_data()
        globals()["stock"] = Loader(model="stock", from_data=True)

# Show the menu and ask to pick a choice
def get_selected_operation():
    """Shows a menu of options and asks for input,
    returns the choice as string"""
    # needed for testing:
    check_for_globals()
    printer.print_like_typed("\nHere you can chose from one of three options:\n\n\
                             1. List items by warehouse,\n\
                             2. Search an item and place an order\n\
                             3. Browse items by category\n\
                             4. Quit.\n\n")
    return input("Which of these options do you want to chose? (1/2/3/4): ")

def list_items_per_warehouse():
    # needed for testing:
    check_for_globals()
    total_items = 0
    for warehouse in stock:
        total_items += warehouse.occupancy()
        warehouse.list_warehouse()
    print(f"Listed {total_items} items of our {len(list(stock))} warehouses.")
    return total_items

def print_search_results(interest):
    """Takes a string, prints out matching search results
    and returns the number of matches in all warehouses"""
    # needed for testing:
    check_for_globals()
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
        num_warehouses += 1

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
            print(Color.BOLD + f"In {most_items_warehouse} you find the most ({max_items}).\n" + Color.END)
    return total_items

def ask_for_placing_order(search_results, interest):
    """
    Asks whether to place an order, checks or asks for authentication
    and starts the order it in case.
    Returns the successful order or None if refused"""
    order_successful = False
    # ask whether to place an order
    if_order = input("Do you want to place an offer? (y/n): ")
    # a number is also accepted...
    if (if_order == "y" or if_order.isdigit()):
        global username
        if not username.is_authenticated:
            # this will either return an authenticated Employee class or None
            validation = username.validate_user()
            if validation and not validation == username:
                # Make our user an Employee
                username = validation
            else:
                # validation failed, get out of here
                return
        # start the order
        order_successful = username.order_item(search_results, if_order, interest)
        if order_successful:
            # remove order from warehouses
            remove_items_from_warehouses(order_successful, interest)
            # return order as shopping action
            return f"Ordered {order_successful} {interest} items." if order_successful > 1 else f"Ordered {glued_string(interest).lower()} item."
    elif not if_order == "n":
        # invalid input, get out o' here
        printer.print_error()
    return order_successful

def remove_items_from_warehouses(num_items, item_name):
    for warehouse in stock:
        if not num_items:
            # we're done...
            break
        available_items = warehouse.search(item_name)
        if num_items > len(available_items):
            # take as much as we can from this warehouse
            num_items -= len(available_items)
            for item in available_items:
                warehouse.stock.remove(item)
        else:
            # take the rest needed from this warehouse
            while num_items > 0:
                num_items-= 1
                warehouse.stock.remove(available_items[num_items])
        # we also have to make sure a new search for the same interest won't return the same:
        warehouse.items_of_interest = {}
    write_stock_to_json(stock.to_dict())
    


def search_item():
    """Asks user to input his interest,
    makes a call to print matching results
    and a call whether to place an order,
    finally returns the order if successful or the search interest as string"""
    # ask for interest
    interest = input("What are you looking for? (eg. Monitor, elegant, Second Hand...): ")
    # print all matches
    search_results = print_search_results(interest)
    order_successful = False
    if search_results:
        order_successful = ask_for_placing_order(search_results, interest)
        if order_successful:
            return order_successful
    if not order_successful:
        # return search as shopping action
        return f"Searched {glued_string(interest).lower()} item." if not (interest == "n") else None

def browse_by_category():
    """sorts items in all warehouses by category,
    prints the category as list of options to search,
    takes an input to search a category
    prints out the asked items
    and returns a list with the the asked category name as string
    and an eventual order as string"""
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
    if (browse.isdigit() and int(browse) <= len(categories) and int(browse) > 0) or browse in categories:
        # first get the category name
        category = ""
        for cat in categories:
            # also accept category names
            if not browse.isdigit() and cat == browse:
                category = cat
                break
            # option number
            elif browse.isdigit():
                if categories[cat][0] == int(browse):
                    category = cat
                    break
        # print out he items
        print(Color.BOLD + f"\nHere is a list of all items in category '{category.lower()}' of all our warehouses:\n" + Color.END)
        for item in categories[category][1]:
            print(glued_string(str(item)))
        print("\n")
        order = ask_for_placing_order(len(categories[category][1]), category)
        if not order:
            return [category]
        else:
            return [category, order]
    else:
        printer.print_error()

def check_for_employee(user:User):
    '''Takes a User, compares his name with the names of Employees
    and provides the option to login'''
    personnel = Loader(model="personnel")
    personnel_names = [str(x) for x in personnel]
    if str(user) in personnel_names:
        # log_option = input(f"It seems you're an Employee, {str(user)}, do you want to log in now? (y/n): ")
            # get employee 
        employee_candidate = None
        for employee in personnel:
            if str(employee) == str(user):
                employee_candidate = employee
                break
        log_in = option_or_login_input(f"It seems you're an Employee, {str(user)}, do you want to log in now? (y/n/pwd): ", employee_candidate)
        if isinstance(log_in, Employee):
            return log_in
        elif log_in == "y":
            employee = user.validate_user(personnel, personnel_names) # we pass these to prevent unnecessary loading
            if employee:
                user = employee
        elif not log_in == "n":
            printer.print_error()
    return user

#### the shopping loop ####

def go_shopping(actions):
    '''The actual shopping function:
    Takes and returns a list of previously made shopping actions
    and runs recursively until the user interrupts it'''
    shopping = True
    # offer options menu
    operation = get_selected_operation()
    # If they pick 1
    if operation == "1":
        total_items = list_items_per_warehouse()
        actions.append(f"Listed the {total_items} items of our {len(list(stock))} warehouses.")
    # Else, if they pick 2
    elif operation == "2":
        search = search_item()
        if search:
            actions.append(search)
    # Else, if they pick 3
    elif operation == "3":
        category = browse_by_category()
        if category:
            actions.append(f"Browsed the category {category[0]}.")
            if len(category) > 1:
                # possible order
                actions.append(category[1])
    # Else quit, with error in case of invalid input
    elif not operation == "4":
        printer.print_error()
    else:
        # user interruption from options menu
        shopping = False
        return actions

    if shopping:
        shop_on = input(Color.OKCYAN + "\nDo you want to explore our warehouse 2.0 some more? (y/n): " + Color.END)
        if shop_on.lower() == "y":
            return go_shopping(actions)
        elif shop_on == "n":
            # user interruption
            return actions
        else:
            # wrong input
            printer.print_error()
            return go_shopping(actions)
        
def get_user() -> User:
    return User(input("Please enter your name here: "))

################## HERE WE GO: ##################

def main():
    # first make sure the json data is available
    create_jsons_from_data()
    global printer, stock, username
    stock = Loader(model="stock")
    # load the typewriter
    printer = PrinterToy(0.0005)
    # Get the user name
    username= get_user()
    # in case of employee offer log in option
    username = check_for_employee(username)
    # Greet him
    username.greet()
    # send him into nirvana
    shopping_actions = go_shopping([])
    # print a goodbye afterwards and store log
    username.bye(shopping_actions)

if __name__ == "__main__":
    main()
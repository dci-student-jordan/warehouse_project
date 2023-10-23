"""Command line interface to query the stock.

To iterate the source data you can use the following structure:

for item in warehouse1:
    # Your instructions here.
    # The `item` name will contain each of the strings (item names) in the list.
"""

from data import stock, personnel
import time, sys, datetime
import pwinput as pw

# toys
print_speed = 0.0005
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Get the user name
def get_user_name():
    return input("Please enter your name here: ")

# guess...
def greet_user():
    print(f"\nHello {username}.\nWelcome to 'shopping 2.0'")


# Show the menu and ask to pick a choice
def get_selected_operation():
    menu_message = "\nHere you can chose from one of three options:\n\n1. List items by warehouse,\n2. Search an item and place an order\n3. Browse items by category\n4. Quit.\n\n"
    for i in range(len(menu_message)):
        sys.stdout.write(menu_message[i])
        sys.stdout.flush()
        time.sleep(print_speed)
    return input("Which of these options do you want to chose? (1/2/3/4): ")

class warehouse_item():
    def __init__(self, item) -> None:
        self.item = item
    # Make the items compareable as strings
    def __str__(self) -> str:
        return self.item["state"] + " " + self.item["category"]
    def category(self):
        return self.item["category"]
    
# create the warehouses_dict
warehouses_dict = {}

def read_stock():
    for item in stock:
        warehouse = "warehouse" + str(item["warehouse"])
        add_item = warehouse_item(item)
        if not warehouse in warehouses_dict:
            warehouses_dict[warehouse] = [add_item]
        else:
            warehouses_dict[warehouse].append(add_item)

#fill the warehouses:
read_stock()
show_error = False

def list_warehouse(warehouse, name):
    print(bcolors.OKBLUE + "Here's a list of our products in", name, ":\n" + bcolors.END)
    items = 0
    for item in warehouse:
        items += 1
        print(item)
        time.sleep(print_speed)
    print(bcolors.OKGREEN + f"\nTotal amount of items in {name}: {len(warehouse)}\n" + bcolors.END)
    return items

def glued_string(add_glue):
    vowels = "aeiouh"
    return f"An {add_glue.lower()}" if add_glue[0].lower() in vowels else f"A {add_glue.lower()}"

def print_days_in_stock(warehouse, name):
    for match in warehouse:
            today = datetime.datetime.now()
            days_in_stock = today - datetime.datetime.strptime(match.item["date_of_stock"], "%Y-%m-%d %H:%M:%S")
            print(f" {glued_string(str(match))} located in " +bcolors.UNDERLINE + name + bcolors.END + f" (in stock for {str(days_in_stock.days)} days)")

def search_item():
    return input("What are you looking for? (eg. Monitor, elegant, Second Hand...): ")

def print_search_results(interest):
    total_items = 0
    most_items_warehouse = ""
    max_items = 0
    matches_per_warehouse = {}
    for warehouse in warehouses_dict:
        matches = [x for x in warehouses_dict[warehouse] if interest.lower() in str(x).lower()]
        matches_per_warehouse[warehouse] = matches
        length = len(matches)
        max_items = max_items if max_items > length else length
        total_items += length
        most_items_warehouse = most_items_warehouse if length < max_items else warehouse

    if total_items == 0:
        # not found
        print("Sorry, but that's not in stock.")
        if_order = "n"
    else:
        for matches in matches_per_warehouse:
            print_days_in_stock(matches_per_warehouse[matches], matches)
        print(bcolors.BOLD + f"\nWe have {total_items} offers for you", end="")
        if len(matches_per_warehouse) == 0:
            # only in one warehouse
            w_name = matches_per_warehouse.keys[0]
            print(" in", w_name)
        else:
            print(" in our warehouses!")
            print(bcolors.BOLD + f"In {most_items_warehouse} you find the most ({max_items}):\n" + bcolors.END)
        if_order = input("Do you want to place an offer? (y/n): ")
    return total_items, if_order

def validate_user():
    global username
    user_dict = {}
    def unpack_personnel(personnel_dict):
        nonlocal user_dict
        for p_item in personnel_dict:
            if user_dict:
                break
            if p_item["user_name"] == username:
                user_dict = p_item
                break
            elif "head_of" in p_item.keys():
                unpack_personnel(p_item["head_of"])
        return user_dict
    uname_dict = unpack_personnel(personnel)
    def ask_password(mess):
        print(mess)
        password = pw.pwinput(mask="*")
        if uname_dict["password"] == password:
            return True
        else:
            ask_again = input(bcolors.FAIL + f"Sorry, {username}, that wasn't right." + bcolors.END + "\nWanna try again? (y/n): ")
            if ask_again == "y":
                ask_password(f"please enter your correct password, {username}: ")
            else:
                return False
    if uname_dict:
        auth = ask_password(f"please log in with your password, {username}: ")
        return auth
    else:
        change_name = input(f"You're not registered, {username}, wanna change your name? (y/n): ")
        if change_name == "y":
            username = input("Ok, whats your login-name, then? ")
            validate_user()
        else:
            return False

def login(func):
    logged_in = False

    def wrapper(*args):
        nonlocal logged_in
        if not logged_in:
            print("login needed")
            logged_in = validate_user()
            if logged_in:
                return func(*args)
            else:
                return None
        else:
            print("user already logged in")
            return func(*args)
    
    return wrapper

@login
def order_item(search_results, interest):
        max_items, if_order = search_results[0], search_results[1]
        global show_error
        if if_order.lower() == "y" or if_order.isdigit():
            if if_order.isdigit():
                order = if_order
            else:
                order = input("how many do you want to purchase? (number): ")
            if not order.isdigit():
                    show_error = True
            else:
                if int(order) >= max_items:
                    reorder = input(bcolors.FAIL + f"Error: Your requested too many items, do you want to order the maximum of {max_items} {interest} items instead? (y/n): " + bcolors.END)
                    if not reorder.lower() == "y":
                        return
                items = "item" if order == "1" else "items"
                print(bcolors.OKGREEN + f"\nCongratulation! Your order for {order} {interest} {items} has ben placed." + bcolors.END)


def search_and_order_item():
    interest = search_item()
    search_results = print_search_results(interest)
    if search_results[0] and (search_results[1] == "y" or search_results[1].isdigit()):
        order_item(search_results, interest)
    return interest if not (interest == "n") else None

def browse_by_category():
    categories = {}
    def create_categories(warehouse):
        for item in warehouse:
            category_dict_item = str(item) + ", Warehouse " + str(item.item["warehouse"])
            if not item.category() in categories:
                num_categories = len(categories) + 1
                # key = category name
                # value = [input_selection_number, [list_with_item_string for later use]]
                # BEWARE: first category-dictionary-item is the input selection!
                categories[item.category()] = [num_categories, [category_dict_item]]
            else:
                categories[item.category()][1].append(category_dict_item)

    for warehouse in warehouses_dict:
        create_categories(warehouses_dict[warehouse])
    options = "("
    print(bcolors.OKCYAN + "\nHere's a list of available categories:\n" + bcolors.END)
    for category in categories:
        option = categories[category][0]
        options = options + (str(option) + "..." if option == 1 else "" if not option == len(categories) else str(option) + "): ")
        print(f"{option}. {category} ({len(categories[category][1])})")    
    browse = input(bcolors.OKCYAN + "\n" + f"Which category do you want to browse? {options}" + bcolors.END)
    if browse.isdigit():
        category = ""
        for cat in categories:
            if categories[cat][0] == int(browse):
                category = cat
                break
        print(bcolors.BOLD + f"\nHere is a list of all items in category '{category.lower()}' of all our warehouses:\n" + bcolors.END)
        for item in categories[category][1]:
            print(glued_string(str(item)))
        return category
    else:
        global show_error
        show_error = True



#### the shopping loop ####

shopping_actions = []
def go_shopping():
    shopping = True
    global show_error
    def print_error():
        print(bcolors.FAIL + "\nError: The operation you entered is not valid." + bcolors.END)
    # Get the user selection
    operation = get_selected_operation()
    # If they pick 1
    if operation == "1":
        total_items = 0
        for warehouse in warehouses_dict:
            total_items += list_warehouse(warehouses_dict[warehouse], warehouse)
        print(f"Listed {total_items} items of all our {len(warehouses_dict)} warehouses.")
        shopping_actions.append(f"Listed the {total_items} items of all our warehouses.")
    # Else, if they pick 2
    elif operation == "2":
        search = search_and_order_item()
        if search:
            shopping_actions.append(f"Searched {glued_string(search).lower()} item.")
    # Else, if they pick 3
    elif operation == "3":
        category = browse_by_category()
        if category:
            shopping_actions.append(f"Browsed the category {category}.")
    # Else quit, with error in case of invalid input
    elif not operation == "4":
        show_error = True
    else:
        shopping = False
    
    if show_error:
        print_error()

    if shopping:
        shop_on = input(bcolors.OKCYAN + "\nDo you want to explore our warehouse 2.0 some more? (y/n): " + bcolors.END)
        if shop_on.lower() == "y":
            show_error = False
            go_shopping()
        elif shop_on == "n":
            pass
        else:
            print_error()
            go_shopping()


################## HERE WE GO: ##################

# Get the user name
username = get_user_name()
# Greet him
greet_user()
# send him into nirvana:
go_shopping()
# Thank the user for the visit
print(bcolors.WARNING + f"\nOk then, {username}, thanks for your visit, we hope to see you soon!" + bcolors.END)
if shopping_actions:
    print("In this session you have:")
    for i in range(len(shopping_actions)):
        print(f"{i+1}. {shopping_actions[i]}")
"""Command line interface to query the stock.

To iterate the source data you can use the following structure:

for item in warehouse1:
    # Your instructions here.
    # The `item` name will contain each of the strings (item names) in the list.
"""

from data import stock
import time, sys, datetime

# YOUR CODE STARTS HERE
print_speed = 0.003
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
username = input("Please enter your name here:")

# Greet the user
print(f"\nHello {username}.\nWelcome to 'shopping 2.0'")

# Show the menu and ask to pick a choice
menu_message = "Here you can chose from one of three options:\n\n1. List items by warehouse,\n2. Search an item and place an order\n3. Browse items by category\n4. Quit.\n\n"
for i in range(len(menu_message)):
    sys.stdout.write(menu_message[i])
    sys.stdout.flush()
    time.sleep(print_speed)
user_input = input("Which of these options do you want to chose? (1/2/3/4): ")

class warehouse_item():
    def __init__(self, item) -> None:
        self.item = item
    
    # Make the items compareable as strings
    def __str__(self) -> str:
        return self.item["state"] + " " + self.item["category"]
    
    def category(self):
        return self.item["category"]
    
# create the warehouses
warehouse1 = []
warehouse2 = []
show_error = False

def read_stock():
    for item in stock:
        warehouse = item["warehouse"]
        add_item = warehouse_item(item)
        house = eval(f"warehouse{warehouse}")
        house.append(add_item)
#fill the warehouses:
read_stock()

def list_warehouse(warehouse, name):
    print(bcolors.OKBLUE + "Here's a list of our products in", name, ":\n" + bcolors.END)
    for item in warehouse:
        print(item)
        time.sleep(print_speed)
    print(bcolors.OKGREEN + f"\nTotal amount of items in {name}: {len(warehouse)}\n" + bcolors.END)

def print_days_in_stock(warehouse, name):
    for match in warehouse:
            vowels = "aeiouh"
            glue = "An" if str(match)[0].lower() in vowels else "A"
            today = datetime.datetime.now()
            days_in_stock = today - datetime.datetime.strptime(match.item["date_of_stock"], "%Y-%m-%d %H:%M:%S")
            print(f" {glue} {str(match)} located in " +bcolors.UNDERLINE + name + bcolors.END + f" (in stock for {str(days_in_stock.days)} days)")

def search_warehouses(interest):
    matches_in_w1 = [x for x in warehouse1 if interest.lower() in str(x).lower()]
    matches_in_w2 = [x for x in warehouse2 if interest.lower() in str(x).lower()]
    num_w1 = len(matches_in_w1)
    num_w2 = len(matches_in_w2)
    if num_w1 + num_w2 == 0:
        # not found
        print("Sorry, but that's not in stock.")
    else:
        sum_num = num_w1 + num_w2
        print(bcolors.BOLD + f"\nWe have {sum_num} offers for you", end="")
        if num_w1 == 0 or num_w2 == 0:
            # only in one warehouse
            w_name = "warehouse"+"1\n" if num_w2 == 0 else "2\n"
            print(" in", w_name)
        else:
            print(" in both warehouses:")
            print(bcolors.BOLD + f"In warehouse{1 if num_w1 > num_w2 else 2} you find the most ({num_w1 if num_w1 > num_w2 else num_w2}):\n" + bcolors.END)
        print_days_in_stock(matches_in_w1, "Warehouse 1")
        print_days_in_stock(matches_in_w2, "Warehouse 2")
        if_order = input("Do you want to place an offer? (y/n): ")
        if if_order.lower() == "y" or if_order.isdigit():
            order = input("how many do you want to purchase? (n): ") if not if_order.isdigit() else if_order
            if int(order) >= sum_num:
                print("Error:")
                reorder = input(f"Your requested too many items, do you want to order the maximum of {sum_num} {interest} items instead? (y/n): ")
                if not reorder.lower() == "y":
                    return
            items = "item" if order == "1" else "items"
            print(bcolors.OKGREEN + f"\nCongratulation! Your order for {order} {interest} {items} has ben placed." + bcolors.END)

def browse_by_category():
    categories = {}
    def create_categories(warehouse):
        for item in warehouse:
            category_dict_item = str(item) + ", Warehouse " + str(item.item["warehouse"])
            if not item.category() in categories:
                num_categories = len(categories) + 1
                # key = category name
                # value = [input_selection_number, [dict_with_item_string for later use]]
                # BEWARE: first category-dictionary-item is the input selection!
                categories[item.category()] = [num_categories, [category_dict_item]]
            else:
                categories[item.category()][1].append(category_dict_item)
    create_categories(warehouse1)
    create_categories(warehouse2)
    options = "("
    print(bcolors.OKCYAN + "\nHere's a list of available categories:\n" + bcolors.END)
    for category in categories:
        option = categories[category][0]
        options = options + str(option) + ("/" if not option == len(categories) else "): ")
        print(f"{option}. {category} ({len(categories[category][1])})")    
    browse = input(bcolors.OKCYAN + "\n" + f"Which category do you want to browse? {options}" + bcolors.END)
    if browse.isdigit():
        for category in categories:
            if categories[category][0] == int(browse):
                for item in categories[category][1]:
                    print(item)
                break
    else:
        global show_error
        show_error = True


# If they pick 1
if user_input == "1":
    list_warehouse(warehouse1, "warehouse 1")
    list_warehouse(warehouse2, "warehouse 2")

# Else, if they pick 2
elif user_input == "2":
    interest = input("What are you looking for? (eg. Monitor, elegant, Second Hand...): ")
    search_warehouses(interest)
# Else, if they pick 3
elif user_input == "3":
    browse_by_category()
# Else quit, with error in case of invalid input
elif not user_input == "4":
    show_error = True
if show_error:
    print(bcolors.FAIL + "\nError:The operation you entered is not valid." + bcolors.END)

# Thank the user for the visit
print(bcolors.WARNING + f"\nOk then, {username}, thanks for your visit, we hope to see you soon!" + bcolors.END)
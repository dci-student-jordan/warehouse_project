"""Command line interface to query the stock.

To iterate the source data you can use the following structure:

for item in warehouse1:
    # Your instructions here.
    # The `item` name will contain each of the strings (item names) in the list.
"""

from data import warehouse1, warehouse2
import time, sys

# YOUR CODE STARTS HERE
print_speed = 0.001

# Get the user name
username = input("Please enter your name here:")

# Greet the user
print(f"Hello {username}.\nWelcome to 'shopping 2.0'")

# Show the menu and ask to pick a choice
menu_message = "Here you can chose from one of three options:\n\n1. List items by warehouse,\n2. Search an item and place an order\n3. Quit.\n\n"
for i in range(len(menu_message)):
    sys.stdout.write(menu_message[i])
    sys.stdout.flush()
    time.sleep(print_speed)
user_input = input("Which of these options do you want to chose? (1/2/3): ")

def list_warehouse(warehouse, name):
    print("Here's a list of our products in", name, ":\n")
    for item in warehouse1:
        print(item)
        time.sleep(print_speed)

def search_warehouses(interest):
    matches_in_w1 = [x for x in warehouse1 if interest.lower() in x.lower()]
    matches_in_w2 = [x for x in warehouse2 if interest.lower() in x.lower()]
    num_w1 = len(matches_in_w1)
    num_w2 = len(matches_in_w2)
    if num_w1 + num_w2 == 0:
        # not found
        print("Sorry, but that's not in stock.")
    else:
        sum_num = num_w1 + num_w2
        print(f"We have {sum_num} offers for you", end="")
        if num_w1 == 0 or num_w2 == 0:
            # only in one warehouse
            w_name = "warehouse"+"1" if num_w2 == 0 else "2"
            print(" in", w_name)
        else:
            print(" in both warehouses:")
            print(f"In warehouse{1 if num_w1 > num_w2 else 2} you find the most ({num_w1 if num_w1 > num_w2 else num_w2}).")
        if_order = input("Do you want to place an offer? (y/n): ")
        if if_order.lower() == "y" or if_order.isdigit():
            order = input("how many do you want to purchase? (n): ") if not if_order.isdigit() else if_order
            if int(order) >= sum_num:
                print("Error:")
                reorder = input(f"Your requested too many items, do you want to order the maximum of {sum_num} {interest} items instead? (y/n): ")
                if not reorder.lower() == "y":
                    return
            items = "item" if order == "1" else "items"
            print(f"Congratulation! Your order for {order} {interest} {items} has ben placed.")

# If they pick 1
if user_input == "1":
    list_warehouse(warehouse1, "warehouse 1")
    list_warehouse(warehouse2, "warehouse 2")

# Else, if they pick 2
elif user_input == "2":
    interest = input("What are you looking for? (eg. Monitor, elegant, Second Hand...): ")
    search_warehouses(interest)
# Else, if they pick 3
#
# Else
elif not user_input == "3":
    print("Error:\nThe operation you entered is not valid.")

# Thank the user for the visit
print(f"Ok then, {username}, thanks for your visit, we hope to see you soon!")



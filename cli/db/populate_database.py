from sys import argv, path
path.append("../")
from warehouses.models import Warehouse, Item, Employee, populate_emp_working_hours
import sqlite3

def connect():
    """Connect to the database."""
    connection = sqlite3.connect("db.sqlite3")
    cur = connection.cursor()
    return connection, cur

def populate_warehouses(items):
    # populating the databases warehouse table:
    for item in items:
        wh, create = Warehouse.objects.get_or_create(name=f"Warehouse {item['warehouse']}")
        Item.objects.create(state=item["state"],
                            category=item["category"],
                            warehouse=wh,
                            date_of_stock=item["date_of_stock"])

def populate_employees(employees_list):
    def unpack_employees(el_to_unpack):
        if type(el_to_unpack) == tuple:
            return el_to_unpack
        else:
            if type(el_to_unpack) == list:
                return [unpack_employees(emp) for emp in el_to_unpack]
            elif type(el_to_unpack) == dict:
                if "head_of" not in el_to_unpack:
                    emp, create = Employee.objects.get_or_create(name=el_to_unpack["user_name"], password=el_to_unpack["password"])
                    return emp
                else:
                    headed = unpack_employees(el_to_unpack["head_of"])
                    emp, create = Employee.objects.get_or_create(name=el_to_unpack["user_name"], password=el_to_unpack["password"])
                    for head in headed:
                        emp.head_of.add(head)
                        emp.save()
                    return emp

    unpacked_employees = unpack_employees(employees_list)
    print(unpacked_employees)

def main(mode):
    try:
        #first create warehouses
        personnel_list, stock_list = None, None
        if mode == "--initial":
            from ..data import personnel, stock
            personnel_list = personnel
            stock_list = stock
        elif mode == "--json":
            from ..load_jsons import load_json_file
            if "personnel" in argv[2]:
                personnel_list = load_json_file(argv[2])
            if "stock" in argv[2]:
                stock_list = load_json_file(argv[2])
        else:
            raise IndexError
        
        # prepare sql queries
        if stock_list:
            populate_warehouses(stock_list)
        if personnel_list:
            populate_employees(personnel_list)
        populate_emp_working_hours()


    except IndexError as e:
        print(e, f"""USAGE:
    'python populate_database.py --initial':
        loads initial values from data.py
    'python populate_database.py --json path/to/json_file.json':
        loads the data from json_file.json,
            -> where 'json_file' is either 'personnel' or 'stock'""")

if __name__ == "__main__":
    mode = "--initial"
    if len(argv) > 1:
        mode = argv[1]
    main(mode)
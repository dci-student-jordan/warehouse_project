from sys import argv, path
path.append("../")
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os

def populate_warehouses(warehouses_ids):
    # create the statement for populating the databases warehouse table:
    pop_statement = "INSERT INTO warehouse (\nVALUES\n\t"
    for i in range(len(warehouses_ids)):
        # we put the serial too to make sure it fits to items...
        pop_statement = pop_statement + \
            f"({warehouses_ids[i]}, 'Warehouse {warehouses_ids[i]}')" + \
            ("," if not i == len(warehouses_ids) - 1 \
                else "\n);\n")
    # writing the statement to file
    with open("pop_warehouse_table.sql", "w") as writer:
        writer.write(pop_statement)
        
def read_and_populate_items(items_list):
    # for gathering the number of warehouses:
    warehouses = []
    # create the statement for populating the databases items table:
    pop_statement = "INSERT INTO item (state, category, warehouse_id, date_of_stock) (\n\tVALUES\n"
    for i in range(len(items_list)):
        item = items_list[i]
        pop_statement = pop_statement + \
            f"\t{item['state'], item['category'], str(item['warehouse']), item['date_of_stock']}" \
            + (",\n" if not i == len(items_list) - 1 \
                else "\n);\n")
        # fill warehouses list
        if not str(item['warehouse']) in warehouses:
            warehouses.append(str(item['warehouse']))
    # writing the statement to file
    with open("pop_item_table.sql", "w") as writer:
        writer.write(pop_statement)
    # populate warehouses
    populate_warehouses(warehouses)

def populate_employees(employees_list):
    def unpack_employees(el_to_unpack):
        if type(el_to_unpack) == tuple:
            return el_to_unpack
        else:
            if type(el_to_unpack) == list:
                return [unpack_employees(emp) for emp in el_to_unpack]
            elif type(el_to_unpack) == dict:
                if "head_of" not in el_to_unpack:
                    return (el_to_unpack["user_name"], el_to_unpack["password"])
                else:
                    return (el_to_unpack["user_name"], el_to_unpack["password"], unpack_employees(el_to_unpack["head_of"]))

    unpacked_employees = unpack_employees(employees_list)
    # create the statement for populating the databases employee table:
    # meanwhile collect head_ofs
    heads = {}
    def append_to_pop(pop, vals, last=False):
        if len(vals) < 3:
            pop = pop + f"\t('{vals[0]}', '{vals[1]}')"
        else:
            for popper in vals[2]:
                pop = append_to_pop(pop, popper)
                tuple_vals = (vals[0], vals[1])
                if tuple_vals not in heads.keys():
                    heads[tuple_vals] = [(popper[0], popper[1])]
                else:
                    heads[tuple_vals].append((popper[0], popper[1]))
            pop = pop + f"\t('{vals[0]}', '{vals[1]}')"
        return pop + (",\n" if not last else "\n);\n")
    pop_statement = "INSERT INTO employee (name, password) (\n\tVALUES\n"
    for i in range(len(unpacked_employees)):
        employee = unpacked_employees[i]
        pop_statement = append_to_pop(pop_statement, employee, last=(not i < len(unpacked_employees) - 1))
    # writing the statement to file
    with open("pop_employee_table.sql", "w") as writer:
        writer.write(pop_statement)
    with open("heads_of_dict.py", "w") as writer:
        writer.write("head_ofs = "+str(heads))

def connect():
    load_dotenv()
    user = os.getenv('POSTGRESQL_USER')
    pw = os.getenv('POSTGRESQL_PASSWORD')
    connection = psycopg2.connect(user=user,
                                  password=pw,
                                  host="localhost",
                                  port="5432",
                                  database="warehouses")
    cur = connection.cursor()
    return connection, cur

def execute_sqls(test, pop_personnel:bool, pop_stock:bool):
    connection, cur = None, None
    try:
        connection, cur = connect()
        # first populate our tables:
        pop_list = []
        if pop_stock:
            pop_list.append("pop_warehouse_table.sql")
            pop_list.append("pop_item_table.sql")
        if pop_personnel:
            pop_list.append("pop_employee_table.sql")
        for file in pop_list:
            with open(file, "r") as reader:
                sql = reader.read()
                cur.execute(sql)
                connection.commit()
        # now assign the head_of informations with the emloyee ids
        from heads_of_dict import head_ofs
        for head in head_ofs:
            head_id_sql = "SELECT id FROM employee WHERE name = %s and password = %s"
            cur.execute(head_id_sql, head)
            head_id = cur.fetchall()[0][0]
            headed_id = []
            for headed in head_ofs[head]:
                cur.execute(head_id_sql, headed)
                headed_id.append(cur.fetchall()[0][0])
            assign_sql = "UPDATE employee SET head_of = COALESCE(head_of, ARRAY[]::int[]) || %s WHERE id = %s"
            cur.execute(assign_sql, (headed_id, head_id))
            connection.commit()
    except (Exception, Error) as error:
        connection.rollback()
        print("Error while querying with database:", error)
    else:
        print("Successfully filled the warehouses database.")
        # just some checks
        if test:
            print("Testing...")
            cur.execute("SELECT COUNT(*) FROM item WHERE category = 'Smartphone'")
            connection.commit()
            result = cur.fetchall()
            print(f"\tCould fetch {result[0][0]} Smarthones from the stock.")
            cur.execute("SELECT COUNT(*) FROM item WHERE state = 'Blue' AND warehouse_id = 1")
            connection.commit()
            result = cur.fetchall()
            print(f"\tCould fetch {result[0][0]} 'blue' items from the stock in warehouse 1.")
            cur.execute("""SELECT e.name , h.name AS head
                        FROM employee e
                        RIGHT JOIN employee h ON e.id = ANY(h.head_of)
                        WHERE e.name IS NOT NULL""")
            connection.commit()
            result = cur.fetchall()
            if result:
                print("\n\tEmployees with head:\n\t  name  |  HEAD\n\t"+"-"*8+"+"+"-"*7)
                for res in result:
                    print("\t" +res[0] + "\t|  "+str(res[1]))
            cur.execute("""SELECT warehouse.name, COUNT(item.id) AS count
                        FROM warehouse
                        RIGHT JOIN item ON warehouse.id = item.warehouse_id
                        GROUP BY warehouse.name ORDER BY count DESC""")
            connection.commit()
            result = cur.fetchall()
            if result:
                print("\n\tTotal items per warehouse:\n\t    name    | count\n\t"+"-"*12+"+"+"-"*7)
                for res in result:
                    print("\t" +res[0] + " |  "+str(res[1]))

    finally:
        if connection:
            cur.close()
            connection.close()

if __name__ == "__main__":
    try:
        personnel_list, stock_list = None, None
        mode = argv[1]
        if mode == "--initial":
            from data import personnel, stock
            personnel_list = personnel
            stock_list = stock
        elif mode == "--json":
            from load_jsons import load_json_file
            if "personnel" in argv[2]:
                personnel_list = load_json_file(argv[2])
            if "stock" in argv[2]:
                stock_list = load_json_file(argv[2])
        else:
            raise IndexError
        
        # prepare sql queries
        if personnel_list:
            populate_employees(personnel_list)
        if stock_list:
            read_and_populate_items(stock_list)
        
        # now execute them
        execute_sqls(mode == "--initial", personnel_list != None, stock_list != None)

    except IndexError as e:
        print(e, f"""USAGE:
    'python populate_database.py --initial':
        loads initial values from data.py
    'python populate_database.py --json path/to/json_file.json':
        loads the data from json_file.json,
            -> where 'json_file' is either 'personnel' or 'stock'""")
import json
from psycopg2 import Error
from db.populate_database import connect


class MissingClassError(Exception):
    """Missing class exception."""

    def __init__(self, name=None, message="Missing class."):
        """Constructor."""
        if name:
            self.class_name = name
            self.message = f"Missing class {name}."
        super().__init__(self.message)


class MissingArgument(Exception):
    pass


class Loader:
    """Main data loader class."""

    model = None
    objects = None

    def __init__(self, *args, **kwargs):
        """Constructor."""
        if "model" not in kwargs:
            raise MissingArgument("The loader requires a " +
                                  "`model` keyword argument to work.")
        self.model = kwargs["model"]
        self.from_data = False
        if "from_data" in kwargs:
            self.from_data = kwargs["from_data"]
        self.parse()

    def parse(self):
        """Instantiate objects from the data."""
        if self.model == "personnel":
            self.objects = self.__parse_personnel()
        if self.model == "stock":
            self.objects = self.__parse_stock()

    def __load_class(self, name):
        """Return a class."""
        classes = __import__("classes")
        if not hasattr(classes, name):
            raise MissingClassError(name)
        return getattr(classes, name)

    def __parse_personnel(self):
        """Parse the personnel list."""
        Employee = self.__load_class("Employee")

        if not self.from_data:
            employees = load_data("employees")
        else:
            import data
            employees = data.personnel
        return [Employee(**employee) for employee in employees]

    def __parse_stock(self):
        """Parse the stock."""
        Item = self.__load_class("Item")
        Warehouse = self.__load_class("Warehouse")
        warehouses = {}
        if not self.from_data:
            items = load_data("stock")
        else:
            import data
            items = data.stock
        for item in items:
            warehouse_id = str(item["warehouse"])
            if warehouse_id not in warehouses.keys():
                warehouses[warehouse_id] = Warehouse(warehouse_id)
            warehouses[warehouse_id].add_item(Item(**item))
        return list(warehouses.values())

    def __iter__(self, *args, **kwargs):
        """Iterate through the objects."""
        yield from self.objects

    # make objects subscriptable
    def __getitem__(self, num):
        return self.objects[num]

    def to_dict(self):
        """Return a dictionary."""
        data = None
        if self.model == "stock":
            data = []
            for warehouse in self.objects:
                for item in warehouse.stock:
                    item_dict = vars(item)
                    item_dict["warehouse"] = warehouse.id
                    data.append(item_dict)
        return data


def load_json_file(file_path):
    """Load all data of stock and personnel
    from jsons into memory."""
    with open(file_path, "r") as reader:
        content = reader.read()
        return json.loads(content)


def load_data(what):
    """Load all data of stock and personnel
    from sql database into memory."""
    connection, cur = None, None
    try:
        connection, cur = connect()
        sql = ""
        if what == "stock":
            sql = "SELECT state, category, \
                warehouse_id, date_of_stock FROM item"
        elif what == "personnel":
            sql = "SELECT id, name, password, \
                head_of FROM employee"
        cur.execute(sql)
    except (Exception, Error) as error:
        connection.rollback()
        print("Error while querying with database:", error)
    else:
        data = cur.fetchall()
        if what == "stock":
            data_list = []
            keys_list = \
                ["state", "category", "warehouse", "date_of_stock"]
            for item in data:
                # also convert datetime to string
                dt = item[-1].strftime("%Y-%m-%d %H:%M:%S")
                item_dict = dict(zip(keys_list, [*item[:-1], dt]))
                data_list.append(item_dict)
            return data_list
        elif what == "personnel":
            keys_list = ["user_name", "password", "head_of"]

            # first replace head_ofs recursively
            def emp_from_id(id):
                emp = dict(zip(keys_list, id_dict[id]))
                if emp["head_of"]:
                    head_of = []
                    for h_id in emp["head_of"]:
                        headed_emp = emp_from_id(h_id)
                        head_of.append(headed_emp)
                # uncomment for original behaviour of loader class
                # including only top level employees
                        # if h_id in e_keys_list:
                        #     e_keys_list.remove(h_id)
                    emp["head_of"] = head_of
                else:
                    # drop empty head_ofs
                    emp.pop("head_of")
                return emp
            e_replaced_dict = {}
            e_keys_list = [x[0] for x in data]
            e_data_list = [x[1:] for x in data]
            id_dict = dict(zip(e_keys_list, e_data_list))
            for id in id_dict:
                emp = emp_from_id(id)
                e_replaced_dict[id] = emp
            # now return left dicts as list
            data_list = [e_replaced_dict[x] for x in e_keys_list]
            return data_list

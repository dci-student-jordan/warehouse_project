import json

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
            raise MissingArgument("The loader requires a `model` keyword argument to work.")
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

        employees = load_json_file("data/personnel.json")
        return [Employee(**employee) for employee in employees]

    def __parse_stock(self):
        """Parse the stock."""
        Item = self.__load_class("Item")
        Warehouse = self.__load_class("Warehouse")
        warehouses = {}
        if not self.from_data:
            items = load_json_file("data/stock.json")
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
    def __getitem__ (self, num):
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
    with open(file_path, "r") as reader:
        content = reader.read()
        return json.loads(content)
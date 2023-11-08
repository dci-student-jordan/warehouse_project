import os, json
import data

def write_data_to_json(file_path, data_list):
    with open(file_path, "w") as writer:
        writer.write(json.dumps(data_list, indent=4))


def create_jsons_from_data():
    """Store the stock and personnel lists from data.py as json files in data directory
    if not already present."""

    # create data dir if not present
    if not "data" in os.listdir("."):
        os.makedirs("data")

        # create stock.json from data.py
        write_data_to_json(os.path.join("data", "stock.json"), data.stock)

        # create personnel.json from data.py
        write_data_to_json(os.path.join("data", "personnel.json"), data.personnel)

def write_stock_to_json(stock):
    write_data_to_json(os.path.join("data", "stock.json"), stock)

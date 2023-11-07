import unittest
from contextlib import contextmanager
import builtins
from query import get_user, get_selected_operation, list_items_per_warehouse, search_item
from classes import User, Employee, Warehouse, Item
from loader import Loader
from unittest.mock import patch, MagicMock
from toys import PrinterToy

@contextmanager
def mock_input(mock):
    original_input = builtins.input
    builtins.input = lambda _: mock
    yield
    builtins.input = original_input


@contextmanager
def mock_output(mock):
    original_print = builtins.print
    # for these tests it is ok to exclude prints with argument end = ""
    builtins.print = lambda *value, end="\n": [mock.append(val) for val in value if not end == ""]
    yield
    builtins.print = original_print


class TestQuery (unittest.TestCase):
    def setUp(self) -> None:
        self.personnel = Loader(model="personnel")
        self.stock = Loader(model="stock")
        return super().setUp()
    
    @patch('pwinput.pwinput')
    def test_get_user(self, overridden_pwinput):
        with mock_input("Unknown"):
            # ensure unknown user to be only User class
            unknown_user = get_user()
            self.assertEqual(unknown_user._name, "Unknown")
            self.assertEqual(type(unknown_user), type(User("")))
            self.assertFalse(isinstance(unknown_user, Employee))
        with mock_input("Jeremy"):
            # ensure a known user remains User only...
            known_user = get_user()
            self.assertEqual(str(known_user), "Jeremy")
            self.assertEqual(type(unknown_user), type(User("")))
            # ... until locked in
            overridden_pwinput.return_value = "coppers" # mock pwinput for login
            known_user = known_user.validate_user()
            self.assertTrue(known_user.is_authenticated)
            self.assertEqual(type(known_user), type(Employee("Samuel", "peters"))) # Samuel is also registered...
            self.assertTrue(isinstance(known_user, User))
            self.assertTrue(isinstance(known_user, Employee))


    def print_like_print(self, mess):
        print(mess)

    @patch("toys.PrinterToy.print_like_typed")
    def test_get_selected_operation(self, print_untyped):
        # have to mock the printer toys...
        print_untyped.side_effect = self.print_like_print
        with mock_input("4"):
            printed_answer = []
            with mock_output(printed_answer):
                # test the returned operation
                input_answer = get_selected_operation()
                self.assertEqual(input_answer[0], "4")
                # check if all options were printed
                self.assertIn("1. List", printed_answer[0])
                self.assertIn("2. Search", printed_answer[0])
                self.assertIn("3. Browse", printed_answer[0])
                self.assertIn("4. Quit", printed_answer[0])
    
    @patch("toys.PrinterToy.print_line_by_line")
    def test_warehouse_items_print(self, print_untyped):
        # have to mock the printer toys...
        print_untyped.side_effect = self.print_like_print
        printed_answer = []
        with mock_output(printed_answer):
            list_items_per_warehouse()
            self.assertIn("Listed 5000 items of our 4 warehouses.", printed_answer[-1])
            # we'll have to seek for the following lines:
            check_item_nums = ["Total amount of items in Warehouse1: 1346.",
                            "Total amount of items in Warehouse2: 1258.",
                            "Total amount of items in Warehouse3: 1173.",
                            "Total amount of items in Warehouse4: 1223."]
            for printed in printed_answer[:-1]:
                if not check_item_nums:
                    # 4: all found, done
                    break
                if check_item_nums[0] in printed:
                    # 1, 2, 3:
                    # First we check for the number to be equal the length of the warehouses' stock...
                    check_item_house = int(check_item_nums[0].split()[-2][-2:-1])-1
                    num_items = int(check_item_nums[0].split()[-1][:-1])
                    self.assertEqual(num_items, self.stock[check_item_house].occupancy())
                    # ...then we remove what we found
                    check_item_nums.remove(check_item_nums[0])
            # check if all were found:
            self.assertEqual(len(check_item_nums), 0)

    def sort_dict(self, list_to_sort):
        sorted_dict ={
            "Warehouse1":[],
            "Warehouse2":[],
            "Warehouse3":[],
            "Warehouse4":[]
        }
        # sort the result per warehouse
        for line in list_to_sort:
            for key in sorted_dict:
                if key in line:
                    # We have to exclude the most items warehouse print
                    if not "you find the most" in line:
                        sorted_dict[key].append(line)
                        break
                    # This is for testing list_warehouses:
        return sorted_dict
    
    def test_search_item(self):
        with mock_input("ios"):
            all_ios_items = []
            with mock_output(all_ios_items):
                search_item()
            sorted = self.sort_dict(all_ios_items)
            for warehouse in self.stock:
                # now we can do the actual testing
                self.assertEqual(len(sorted[str(warehouse)]), len(warehouse.search("ios")))


    def test_print_warehouse_list(self):
        # have a look above...
        pass      
        

if __name__ == '__main__':
    unittest.main()
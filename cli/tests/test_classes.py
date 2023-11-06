import unittest

class TestClasses (unittest.TestCase):

    def test_naming(self):
        from classes import User, Employee, Warehouse, Item
        self.assertIsNotNone(User)
        self.assertIsNotNone(Employee)
        self.assertIsNotNone(Warehouse)
        self.assertIsNotNone(Item)

    def test_inheritance(self):
        from classes import User, Employee
        self.assertEqual(Employee.__base__, User)

    def test_user_class(self):
        from classes import User
        test_user = User("")
        self.assertEqual(str(test_user), "Anonymous")
        self.assertFalse(test_user.is_authenticated)
        test_user = User("Conny")
        self.assertEqual(test_user._name, "Conny")
        self.assertFalse(test_user.is_authenticated)
        test_user = User("Jon", "unused_password")
        self.assertFalse(test_user.is_authenticated)
        test_user.authenticate("")
        self.assertFalse(test_user.is_authenticated)

    def test_employee_class(self):
        from classes import Employee
        test_employee = Employee("", "")
        test_employee.authenticate("")
        self.assertFalse(test_employee.is_authenticated)
        self.assertIsNone(test_employee.head_of)
        test_employee = Employee("Bob", "Dylan")
        test_employee.authenticate("Dylan")
        self.assertTrue(test_employee.is_authenticated)
        test_employee = Employee("Samuel", "peters", head_of=[{"user_name": "Boris", "password": "docker"}])
        self.assertEqual(str(test_employee.head_of), str([Employee(**{"user_name": "Boris", "password": "docker"})]))

    def test_warehouse_class(self):
        from classes import Warehouse, Item
        from datetime import datetime as dt
        self.assertIsNone(Warehouse().id)
        self.assertEqual(Warehouse(id=9).id, 9)
        self.assertEqual([], Warehouse().stock)
        test_warehouse = Warehouse(id=3)
        test_warehouse.add_item(Item("sweet", "cat", 3, dt.now()))
        self.assertEqual(test_warehouse.occupancy(), len(test_warehouse.stock))
        for pet in ["cat", "rat", "dog", "chicken"]:
            test_warehouse.add_item(Item("stupid", pet, 3, dt.now()))
        search = test_warehouse.search("cat")
        for cat_item in search:
            # excluded other categories
            self.assertNotIn("dog", str(cat_item))
            self.assertNotIn("rat", str(cat_item))
            self.assertNotIn("chicken", str(cat_item))
            # included cat-egory
            self.assertIn("cat", str(cat_item))
            # included states
            self.assertIn(cat_item.state, ["sweet", "stupid"])
        same_search = test_warehouse.search("cat")
        self.assertEqual(search, same_search)

    def test_item_class(self):
        from classes import Item
        from datetime import datetime as dt
        now = dt.now()
        test_item = Item("awesome", "code", 12, now)
        self.assertTrue(test_item.__getattribute__("state") == "awesome")
        self.assertTrue(test_item.__getattribute__("category") == "code")
        self.assertTrue(test_item.__getattribute__("date_of_stock") == now)
        self.assertIn(test_item.state, str(test_item))
        self.assertIn(test_item.category, str(test_item))



if __name__ == '__main__':
    unittest.main()
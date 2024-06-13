# warehouse_project
This is a project for the python-backend-developer course made the [DCI](https://digitalcareerinstitute.org/).
There is nothing to order, it is just for practising purpose. A preview you can find [here](https://dci-student-jordan.github.io/warehouse_project/).

It has become a fully functional prototype web application for a Warehouse Management System.

### Features:
- A user system with roles and permissions for listing and placing orders.
- Maintain the stock of a warehouse.
- Order items from the warehouse.
- Log actions from users.
- Messaging.

The project uses python version > 3.10 and the [commandlinetool](https://github.com/dci-student-jordan/warehouse_project/blob/main/cli/query.py) requires the pwinput and getch modules.

# Setup
In the branch "dockered" you can run "docker compose up" in order to test, assuming you have docker and docker compose installed.

If you want to test the whole system locally create and activate a virtual environment and install requirements from the file. (If you get "ERROR: Could not build wheels for getch, which is required to install pyproject.toml-based projects" run "sudo apt-get update", "sudo apt-get install build-essential" and "sudo apt-get install python3-dev").
To avoid setting up a postgres table the system uses the db.sqlite and you should be able to test at this stage.

If you want to run with postgres, you would have to install it, unless you don't have already, then setup the database by first changing the djangowhp/settings.py file, lines 82 to 98, to use postgres, create the db manually and an .env file with your credentials, change lines 86-88 in settings file accordingly and finally run the file cli/db/populate_database.py from the manage.py shell

This project is published under the [MIT-Licence](https://github.com/dci-student-jordan/warehouse_project/blob/main/LICENSE.txt)

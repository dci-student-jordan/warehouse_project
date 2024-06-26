# warehouse_project
This is a project for the python-backend-developer course made the [DCI](https://digitalcareerinstitute.org/).

It has become a fully functional prototype web application for a Warehouse Management System.

### Features:
- A user system with roles and permissions for listing and placing orders.
- Maintain the stock of a warehouse.
- Order items from the warehouse.
- Log actions from users.
- Messaging.

The project uses python version > 3.11 and the [commandlinetool](https://github.com/dci-student-jordan/warehouse_project/blob/main/cli/query.py) requires the pwinput and getch modules.

## Setup
In the branch "dockered" you can run "docker compose up" in order to test, assuming you have docker and docker compose installed.

If you want to test the whole system locally clone the repo, create and activate a virtual environment and install requirements from the file. (If you get "ERROR: Could not build wheels for getch, which is required to install pyproject.toml-based projects" run "sudo apt-get update", "sudo apt-get install build-essential" and "sudo apt-get install python3-dev").
To avoid setting up a postgres table the repo by default uses the db.sqlite and you should be able to test at this stage: Log in as "Bob", pw "bgt56789" or sign up as a new user, or log in as "Jeremy", pw "ju7890ßü" who is a staff member and thus has different privileges. You can also create a new staff user by chosing one of the "Personnel" in cli/data, to see how the system guides you through the proces of becoming a staff member.

If you want to run with postgres, you would have to install it, unless you don't have already, then setup the database by first changing the djangowhp/settings.py file, lines 85 to 101, to use postgres, create the db manually and an .env file with your credentials and finally run the file cli/db/populate_database.py from the manage.py shell


## CLI
The task started as a cli tool, which you can also test by running "python query.py" from within the /cli folder - credentials for placing an order here you find in the above mentioned "Personnel" list (create and activate a venv first and run "pip install -r requirements" first).

This project is published under the [MIT-Licence](https://github.com/dci-student-jordan/warehouse_project/blob/main/LICENSE.txt)

Python Flask application (ShoppingList)

To be able to get the application working:
- clone the repository
- make sure that you have Python3 installed (recommended to use virtualenv)
- source to the virtual environment (source venv/bin/activate)
- make sure that env.sh is executable (chmod +x env.sh)
- run command . env.sh (The shell script will source to a folder called venv/bin/activate, if you will not use this method ignore the message and do the following commands: export FLASK_APP=shopping_app.py, export FLASK_ENV=development)
- install the required dependencies from the requirements file (pip install -r requirements.txt OR pip3 install -r requirements.txt)
- make sure that writting permissions is added to the app.db (otherwise you will not be able to create new user, new shoppingitems or do any modifications at all) (ls -l app.db)

Voila, you are good to go.
run command: flask run

If you are new to using Python with virtualenv, read more about it here: https://docs.python-guide.org/dev/virtualenvs/




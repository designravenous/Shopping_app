Python Flask application (ShoppingList)

To be able to get the application working:
- clone the repository
- make sure that you have Python3 installed (recommended to use virtualenv)
- source to the virtual environment (source venv/bin/activate)
- make sure that env.sh is executable (chmod +x env.sh)
- run command . env.sh (The shell script will source to a folder called venv/bin/activate, if you will not use this method ignore the message and do the following commands: export FLASK_APP=shopping_app.py, export FLASK_ENV=development)
- install the required dependencies from the requirements file (pip install -r requirements.txt OR pip3 install -r requirements.txt)
- make sure that writting permissions is added to the app.db (otherwise you will not be able to create new user, new shoppingitems or do any modifications at all) (ls -l app.db)
- Update Configuration to be able to use the SMTP functions.

Voila, you are good to go.
run command: flask run

Manual searches in DB for example, and testing:
run command: flask shell

If you are new to using Python with virtualenv, read more about it here: https://docs.python-guide.org/dev/virtualenvs/

Configuration For Production:
Before making this an production applications there is a few things to consider.

- Make sure you have added a new SECRET_KEY in the configuration
- Make sure that you have added SMTP information correctly.
- Depending on how you will host the application, make sure that external URLs work. for example you might need to change the url in the application/template/emails. Otherwise the url will point to http://localhost/reset_user_password/{{ token }}. For example I am hosting with nginx pointing to port 5000 in the nginx.conf (/etc/nginx/nginx.conf)

if you are using the env.sh script. Make sure to change the FLASK_ENV variable to Production instead of development.

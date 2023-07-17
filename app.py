from flask import Flask, request, render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB connection string
db = client['mydatabase']  # Update with your database name
collection = db['users']  # Update with your collection name

# @app.route('/user_list')
# def user_list():
#     users = collection.find()
#     print(users)
#     return render_template('user_list.html', users=users)

@app.route('/', methods=['GET', 'POST'])
def user_form():
    if request.method == 'POST':
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        data = {
            'first_name': first_name,
            'last_name': last_name
        }
        collection.insert_one(data)
        return '!!! Data stored successfully' 

    
    return render_template('user_form.html')

@app.route('/add_user', methods=['GET'])
def add_user():
    first_name = request.args.get('firstname')
    last_name = request.args.get('lastname')
    print('first_name= ', first_name)
    print('last_name= ', last_name)
    data = {
        'first_name': first_name,
        'last_name': last_name
    }
    print ('data=', data)
    collection.insert_one(data)
    messsage = f'!!! Using GET data stored successfully for user: {first_name}, {last_name}'
    return messsage
    
    # return render_template('user_form.html')

# Work properly
@app.route('/user_list', methods=['GET'])
def user_list():
    search_query = request.args.get('search', '')
    if search_query:
        users = collection.find({
            '$or': [
                {'first_name': {'$regex': search_query, '$options': 'i'}},
                {'last_name': {'$regex': search_query, '$options': 'i'}}
            ]
        })
    else:
        users = collection.find()
    _first_name = ''
    _last_name = ''
    for user in users:
        # print ('!!! USER = ', user)
        _first_name = user["first_name"]
        _last_name = user["last_name"]         
    
    print('_first_name', _first_name)
    print('_last_name', _last_name)
    # return render_template('user_list.html', users=myusers)
    return render_template('user_list.html', first_name=_first_name, last_name = _last_name, users = users)

# this work 
# @app.route('/user_list', methods=['POST'])
# def user_list():
#     search_query =request.form.get('search')
#     if search_query:
#         users = collection.find({
#             '$or': [
#                 {'first_name': {'$regex': search_query, '$options': 'i'}},
#                 {'last_name': {'$regex': search_query, '$options': 'i'}}
#             ]
#         })
#     else:
#         users = collection.find()

#     for user in users:
#         print ('!!! USER = ', user) 
#         _first_name = user["first_name"]
#         _last_name = user["last_name"]       
    
#     # _first_name = myusers[0]["first_name"]
#     # _last_name = myusers[0]["last_name"]
#     print('_first_name', _first_name)
#     print('_last_name', _last_name)
#     # return render_template('user_list.html', first_name=_first_name, last_name = _last_name)
#     return render_template('user_list.html', first_name=_first_name, last_name = _last_name, users = users)

@app.route('/process', methods=['POST'])
def process():
    # Retrieve the HTTP POST request parameter value from 'request.form' dictionary
    _username = request.form.get('username')  # get(attr) returns None if attr is not present
 
    # Validate and send response
    if _username:
        return render_template('hello.html', username=_username)
    else:
        return 'Please go back and enter your name...', 400  # 400 Bad Request
    
if __name__ == '__main__':
    app.debug = True
    app.run()

# from flask import Flask  # From 'flask' module import 'Flask' class
# app = Flask(__name__)    # Construct an instance of Flask class for our webapp

# @app.route('/')   # URL '/' to be handled by main() route handler (or view function)
# def main():
#     """Say hello"""
#     return 'Hello, world!'

# if __name__ == '__main__':  # Script executed directly (instead of via import)?
#     app.debug = True
#     app.run()  # Launch built-in web server and run this Flask webapp
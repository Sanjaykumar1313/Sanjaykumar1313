from flask import Flask, request, jsonify

import jwt

import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'

# Dummy user data

users = {

    'john': 'password123',

    'susan': 'flask456'

}

# Sign-up route

@app.route('/signup', methods=['POST'])

def signup():

    username = request.json.get('username')

    password = request.json.get('password')

    if username and password:

        users[username] = password

        return jsonify({'message': 'User created successfully!'}), 201

    else:

        return jsonify({'message': 'Invalid username or password!'}), 400

# Sign-in route

@app.route('/signin', methods=['POST'])

def signin():

    username = request.json.get('username')

    password = request.json.get('password')

    if username in users and users[username] == password:

        # Generate JWT token

        token = jwt.encode({

            'username': username,

            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

        }, app.config['SECRET_KEY'])

        

        return jsonify({'token': token.decode('utf-8')})

    else:

        return jsonify({'message': 'Invalid username or password!'}), 401

# Protected route example

@app.route('/protected', methods=['GET'])

def protected():

    token = request.headers.get('Authorization')

    if not token:

        return jsonify({'message': 'Missing token!'}), 401

    

    try:

        decoded_token = jwt.decode(token, app.config['SECRET_KEY'])

        username = decoded_token['username']

        return jsonify({'message': f'Welcome, {username}! This is a protected route.'}), 200

    except jwt.ExpiredSignatureError:

        return jsonify({'message': 'Token has expired!'}), 401

    except jwt.InvalidTokenError:

        return jsonify({'message': 'Invalid token!'}), 401

if __name__ == '__main__':

    app.run()


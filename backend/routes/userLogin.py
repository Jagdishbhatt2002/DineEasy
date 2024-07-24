from flask import request, Blueprint, jsonify
from .models import LoginUser
import bcrypt
import jwt
import datetime
from bson import ObjectId
# Importing the Flask app instance

user_blueprint = Blueprint('login', __name__)
secret_key = '123456789'

#Fetch Users
@user_blueprint.route('/api/user', methods=['GET'])
def get_data():
    users = LoginUser.objects.all()
    transformed_users = []

    for user in users:
        transformed_user = {
            'id': str(user.id),
            'email':user.email,
        }
        transformed_users.append(transformed_user)

    return jsonify(transformed_users), 200

#Add User

@user_blueprint.route('/api/user', methods=['POST'])
def add_user():
    data = request.json
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Email and password are required'}), 400

    email = data['email']
    password = data['password']

    if LoginUser.objects(email=email).first():
        return jsonify({'message': 'User already exists'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    new_user = LoginUser(email=email, password=hashed_password)
    try:
        new_user.save()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    # Return success response
    return jsonify({'message': 'User added successfully'}), 201

# Login route

@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Email and password are required'}), 400

    email = data['email']
    password = data['password']
    user = LoginUser.objects(email=email).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        token = jwt.encode({'user_id': str(user.id),'email':user.email,'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           'your_secret_key', algorithm='HS256')
        return jsonify({'token': token,'status':200 })
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    
#Delete User
    
@user_blueprint.route('/api/user/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user_id = ObjectId(user_id)
    except Exception as e:
        return jsonify({'error': 'Invalid user ID format'}), 400  # Bad Request
    
    # Find the user by ID
    user = LoginUser.objects(id=user_id).first()
    
    # Check if the user exists
    if not user:
        return jsonify({'error': 'user not found'}), 404  # Not Found

    # Delete the user from the database
    try:
        user.delete()
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Internal Server Error
    
    # Return success response
    return jsonify({'message': 'user deleted successfully'}), 200

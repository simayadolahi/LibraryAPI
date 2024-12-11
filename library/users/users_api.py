from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from library import db
from library.models import UserModel
from werkzeug.security import generate_password_hash

users_api = Blueprint('users_api', __name__)
api = Api(users_api)

# Define fields for user response
user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'role': fields.String
}

class UserListResource(Resource):
    @marshal_with(user_fields)
    def get(self):
        """Get a list of all users"""
        users = UserModel.query.all()
        return users
    @marshal_with(user_fields)
    def post(self):
        """Create a new user"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help="Name cannot be blank")
        parser.add_argument('email', type=str, required=True, help="Email cannot be blank")
        parser.add_argument('password', type=str, required=True, help="Password cannot be blank")
        parser.add_argument('role', type=str, default='user', help="Role of the user, default is 'user'")
        
        args = parser.parse_args()

        # Check if the email already exists
        if UserModel.query.filter_by(email=args['email']).first():
            abort(400, message="Email already exists")

        # Hash the password
        hashed_password = generate_password_hash(args['password'])

        # Create the new user
        new_user = UserModel(
            name=args['name'],
            email=args['email'],
            password_hash=hashed_password,
            role=args['role']
        )

        db.session.add(new_user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201

class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        """Get a user by ID"""
        user = UserModel.query.get(user_id)
        if user is None:
            abort(404, message="User not found")
        return user

    @marshal_with(user_fields)
    def put(self, user_id):
        """Update an existing user"""
        user = UserModel.query.get(user_id)
        if user is None:
            abort(404, message="User not found")

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('role', type=str)
        
        args = parser.parse_args()

        # Update fields if they are provided
        if args['name']:
            user.name = args['name']
        if args['email']:
            # Optionally, check if the new email already exists
            if UserModel.query.filter_by(email=args['email']).first():
                abort(400, message="Email already exists")
            user.email = args['email']
        if args['password']:
            user.password_hash = generate_password_hash(args['password'])
        if args['role']:
            user.role = args['role']

        db.session.commit()
        return user
    @marshal_with(user_fields)
    def delete(self, user_id):
        """Delete a user"""
        user = UserModel.query.get(user_id)
        if user is None:
            abort(404, message="User not found")

        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users

# Add resources to API
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')


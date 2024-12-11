from flask import Blueprint, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from library import db
from library.models import AuthorModel, BookModel

authors_api = Blueprint('authors_api', __name__)
api = Api(authors_api)

# Define fields to marshal the output
author_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'books': fields.List(fields.String(attribute='title'))  # List of book titles by the author
}

# Class to handle collection of authors
class AuthorListResource(Resource):
    @marshal_with(author_fields)
    def get(self):
        """Fetch all authors"""
        authors = AuthorModel.query.all()
        return authors
    @marshal_with(author_fields)
    def post(self):
        """Create a new author"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help="Name cannot be blank")
        
        args = parser.parse_args()

        # Check if the author already exists
        existing_author = AuthorModel.query.filter_by(name=args['name']).first()
        if existing_author:
            abort(400, message="Author with this name already exists")

        # Create a new author instance
        new_author = AuthorModel(name=args['name'])

        db.session.add(new_author)
        db.session.commit()
        authors = AuthorModel.query.all()

        return authors, 201


# Class to handle a specific author
class AuthorResource(Resource):
    @marshal_with(author_fields)
    def get(self, author_id):
        """Fetch a specific author by ID"""
        author = AuthorModel.query.get(author_id)
        if not author:
            abort(404, message="Author not found")
        return author
    @marshal_with(author_fields)
    def put(self, author_id):
        """Update a specific author's details"""
        author = AuthorModel.query.get(author_id)
        if not author:
            abort(404, message="Author not found")

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)

        args = parser.parse_args()

        if args['name']:
            # Check if another author with the same name already exists
            existing_author = AuthorModel.query.filter_by(name=args['name']).first()
            if existing_author:
                abort(400, message="Author with this name already exists")
            author.name = args['name']

        db.session.commit()

        return author
    @marshal_with(author_fields)
    def delete(self, author_id):
        """Delete a specific author"""
        author = AuthorModel.query.get(author_id)
        if not author:
            abort(404, message="Author not found")

        # Ensure the author does not have any books before deletion
        if author.books:
            abort(400, message="Cannot delete author because they have books associated")

        db.session.delete(author)
        db.session.commit()
        authors = AuthorModel.query.all()
        return authors


# Add resources to API
api.add_resource(AuthorListResource, '/authors')
api.add_resource(AuthorResource, '/authors/<int:author_id>')


from flask import Blueprint, jsonify
from flask_restful import Api, Resource, reqparse, marshal_with, fields, abort
from library import db
from library.models import BookModel, UserModel, AuthorModel

# Create a Blueprint for books
books_api = Blueprint('books_api', __name__)
api = Api(books_api)

# Define fields to marshal the output
book_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'author_id': fields.Integer,
    'author': fields.String(attribute='author.name'),  # Fetching author name from AuthorModel
    'borrowing_date': fields.DateTime,
    'is_available': fields.Boolean,
    'user_id': fields.Integer,
    'borrower': fields.String(attribute='borrower.name')  # Fetching borrower name from UserModel
}

# Class to handle collection of books
class BookListResource(Resource):
    @marshal_with(book_fields)
    def get(self):
        """Fetch all books"""
        books = BookModel.query.all()
        return books
    @marshal_with(book_fields)
    def post(self):
        """Create a new book"""
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help="Title cannot be blank")
        parser.add_argument('author_id', type=int, required=True, help="Author ID is required")
        parser.add_argument('borrowing_date', type=str, help="Date the book was borrowed")
        parser.add_argument('is_available', type=bool, default=True, help="Book availability status")
        
        args = parser.parse_args()

        # Check if the author exists
        author = AuthorModel.query.get(args['author_id'])
        if not author:
            abort(404, message="Author not found")

        # Create a new book instance
        new_book = BookModel(
            title=args['title'],
            author_id=args['author_id'],
            borrowing_date=args['borrowing_date'],
            is_available=args['is_available']
        )

        db.session.add(new_book)
        db.session.commit()
        books = BookModel.query.all()

        return books, 201

# Class to handle a specific book
class BookResource(Resource):
    @marshal_with(book_fields)
    def get(self, book_id):
        """Fetch a specific book"""
        book = BookModel.query.get(book_id)
        if not book:
            abort(404, message="Book not found")
        return book
    @marshal_with(book_fields)
    def put(self, book_id):
        """Update a specific book"""
        book = BookModel.query.get(book_id)
        if not book:
            abort(404, message="Book not found")

        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('author_id', type=int)
        parser.add_argument('borrowing_date', type=str)
        parser.add_argument('is_available', type=bool)
        parser.add_argument('user_id', type=int)  # This field can be used for borrowing or returning the book

        args = parser.parse_args()

        if args['title']:
            book.title = args['title']
        if args['author_id']:
            # Check if the author exists
            author = AuthorModel.query.get(args['author_id'])
            if not author:
                abort(404, message="Author not found")
            book.author_id = args['author_id']
        if args['borrowing_date']:
            book.borrowing_date = args['borrowing_date']
        if args['is_available'] is not None:
            book.is_available = args['is_available']
        if args['user_id']:
            user = UserModel.query.get(args['user_id'])
            if not user:
                abort(404, message="User not found")
            book.user_id = args['user_id']

        db.session.commit()

        return book
    @marshal_with(book_fields)
    def delete(self, book_id):
        """Delete a specific book"""
        book = BookModel.query.get(book_id)
        if not book:
            abort(404, message="Book not found")

        db.session.delete(book)
        db.session.commit()
        books = BookModel.query.all()

        return books


# Add resources to API
api.add_resource(BookListResource, '/books')
api.add_resource(BookResource, '/books/<int:book_id>')


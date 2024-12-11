from flask import render_template, Blueprint
from flask_login import login_required
from library import db
from library.models import AuthorModel, BookModel

authors_bp = Blueprint('authors_bp', __name__)

@authors_bp.route('/authors')
def authors():
    # Retrieve all authors from the database
    authors_list = AuthorModel.query.all()
    
    # Render the authors in an HTML template (you will create the template next)
    return render_template('authors.html', authors=authors_list, title='Authors')

@authors_bp.route('/author/<int:author_id>')
@login_required
def author_books(author_id):
    author = AuthorModel.query.get_or_404(author_id)  # Get the author by ID
    books = BookModel.query.filter_by(author_id=author.id).all()  # Get all books by this author
    return render_template('author_books.html', author=author, books=books)
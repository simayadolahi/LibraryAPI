
from flask import render_template, url_for, flash, redirect, request, Blueprint
from library import  db
from library.models import AuthorModel, BookModel, UserModel
from datetime import datetime
from flask_login import login_required, current_user



books_bp = Blueprint('books_bp', __name__)


@books_bp.route('/books')
def books():
    # Retrieve all books from the database
    books_list = BookModel.query.all()
    
    # Render the authors in an HTML template (you will create the template next)
    return render_template('books.html', books=books_list, title='Books')



@books_bp.route('/borrow/<int:book_id>', methods=['GET', 'POST'])
@login_required
def borrow_book(book_id):
    book = BookModel.query.get_or_404(book_id)  # Find the book by ID
    
    if not book.is_available:  # If the book is not available
        flash("This book is already borrowed.", "danger")
        return redirect(url_for('users_bp.user_dashboard'))  # Redirect back to the home page
    
    # If the book is available, borrow it
    book.is_available = False  # Mark as not available
    book.user_id = current_user.id  # Associate the book with the current user
    book.borrowing_date = datetime.utcnow()  # Set the borrowing date to now
    
    db.session.commit()  # Save changes to the database
    
    flash(f"You have successfully borrowed '{book.title}'.", "success")
    return redirect(url_for('users_bp.user_dashboard'))  # Redirect to the user's dashboard


@books_bp.route('/return/<int:book_id>', methods=['GET','POST'])
@login_required
def return_book(book_id):
    book = BookModel.query.get_or_404(book_id)  # Find the book by ID
    
    # Ensure the current user borrowed the book
    if book.user_id != current_user.id:
        flash("You cannot return a book you didn't borrow.", "danger")
        return redirect(url_for('users_bp.user_dashboard'))  # Redirect to the user's dashboard
    
    # Mark the book as available and record the return date
    book.is_available = True
    book.user_id = None  # Clear the user who borrowed the book
    book.return_date = datetime.utcnow()  # Set the return date to now
    
    db.session.commit()  # Save changes to the database
    
    flash(f"You have successfully returned '{book.title}'.", "success")
    return redirect(url_for('users_bp.user_dashboard'))  # Redirect to the user's dashboard




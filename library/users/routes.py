from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from library import db
from library.models import AuthorModel, BookModel, UserModel
from library.users.forms import  UserForm, RegistrationForm, LoginForm, UpdateAccountForm
from library.books.forms import BookForm
from library.authors.forms import AuthorForm
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from library.users.utils import admin_required

users_bp = Blueprint('users_bp', __name__)


@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = UserModel.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email is already registered.', 'danger')
            return redirect(url_for('users_bp.register'))
        new_user = UserModel(
            name=form.name.data,
            email=form.email.data,
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('users_bp.login'))
    return render_template('register.html',title='Register' ,form=form)


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)  # Log the user in
            flash('Login successful!', 'success')
            return redirect(url_for('main_bp.index'))  # Redirect to the homepage or dashboard
        else:
            flash('Invalid email or password. Please try again.', 'danger')  # Error message if login fails
            return redirect(url_for('users_bp.login'))  # Stay on the login page

    return render_template('login.html', title='Login', form=form)


@users_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main_bp.index'))


@users_bp.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users_bp.account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

   

@users_bp.route('/admin_dashboard', methods=["GET", "POST"])
@login_required
@admin_required
def admin_dashboard():
    authors = AuthorModel.query.all()
    books = BookModel.query.all()

    author_form = AuthorForm()
    book_form = BookForm()

    if request.method == "POST":
        # Edit Author
        if 'edit_author' in request.form:
            author_id = request.form.get('author_id')
            author = AuthorModel.query.get(author_id)
            if author:
                author.name = request.form.get('name')
                db.session.commit()
                flash("Author updated successfully", "success")
                return redirect(url_for('users_bp.admin_dashboard'))

        # Add Author
        elif 'add_author' in request.form:
            new_author = AuthorModel(name=request.form.get('name'))
            db.session.add(new_author)
            db.session.commit()
            flash("Author added successfully", "success")
            return redirect(url_for('users_bp.admin_dashboard'))

        # Edit Book
        elif 'edit_book' in request.form:
            book_id = request.form.get('book_id')
            book = BookModel.query.get(book_id)
            author_id = request.form.get('author_id')  # Get the selected author_id
            
            if book and author_id:  # Make sure author_id is not None or empty
                book.title = request.form.get('title')
                book.author_id = author_id  # Update the author_id properly
                db.session.commit()
                flash("Book updated successfully", "success")
                return redirect(url_for('users_bp.admin_dashboard'))

        # Add Book
        elif 'add_book' in request.form:
            author_id = request.form.get('author_id')
            if author_id:  # Make sure author_id is provided
                new_book = BookModel(
                    title=request.form.get('title'),
                    author_id=author_id
                )
                db.session.add(new_book)
                db.session.commit()
                flash("Book added successfully", "success")
                return redirect(url_for('users_bp.admin_dashboard'))

        # Delete Author
        if 'delete_author' in request.form:
            author_id = request.form.get('author_id')
            author = AuthorModel.query.get(author_id)
            if author:
                # Check if the author has any books
                if BookModel.query.filter_by(author_id=author.id).count() > 0:
                    flash("This author has books associated with them. Please remove the books first.", "warning")
                else:
                    db.session.delete(author)
                    db.session.commit()
                    flash("Author deleted successfully", "success")
                    return redirect(url_for('users_bp.admin_dashboard'))

        # Delete Book
        elif 'delete_book' in request.form:
            book_id = request.form.get('book_id')
            book = BookModel.query.get(book_id)
            if book:
                db.session.delete(book)
                db.session.commit()
                flash("Book deleted successfully", "success")
                return redirect(url_for('users_bp.admin_dashboard'))

    return render_template('admin_dashboard.html', author_form=author_form, book_form=book_form, authors=authors, books=books)



@users_bp.route('/user_dashboard')
@login_required
def user_dashboard():
    borrowed_books = BookModel.query.filter_by(user_id=current_user.id).all()  # Get all books borrowed by the current user
    return render_template('user_dashboard.html', borrowed_books=borrowed_books, name= current_user.name)  # Pass the books to the template


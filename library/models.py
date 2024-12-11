from library import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id)) 

class AuthorModel(db.Model):
    __tablename__ = 'author_model'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    books = db.relationship('BookModel', backref='author', lazy=True)

    def __repr__(self):
        return f"author(name={self.name})"


class BookModel(db.Model):
    __tablename__ = 'book_model'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author_model.id'), nullable=False)
    borrowing_date = db.Column(db.DateTime, nullable=True)  # Allowing null if the user hasn't borrowed a book yet
    is_available = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=True)
    return_date = db.Column(db.DateTime)

    def __repr__(self):
         return f"Book(title={self.title}, author_id={self.author_id}, borrowing_date={self.borrowing_date}, user_id={self.user_id})"
         
class UserModel(db.Model, UserMixin):
    __tablename__ = 'user_model'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user')  # Can be 'user' or 'admin'

    borrowed_books = db.relationship('BookModel', backref='borrower', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return f"User(name={self.name},email={self.email} , role={self.role})"

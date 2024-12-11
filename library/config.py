import os

class Config:
    SECRET_KEY= os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///databse.db'
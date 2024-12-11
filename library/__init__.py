
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from library.config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'users_bp.login'
login_manager.login_message_category = 'info'



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    

    from library.users.routes import users_bp
    from library.books.routes import books_bp
    from library.main.routes import main_bp
    from library.authors.routes import authors_bp
    from library.errors.handlers import errors_bp
    from library.users.users_api import users_api
    from library.books.books_api import books_api
    from library.authors.authors_api import authors_api


    app.register_blueprint(users_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(authors_bp)
    app.register_blueprint(users_api, url_prefix='/api')
    app.register_blueprint(books_api, url_prefix='/api')
    app.register_blueprint(authors_api, url_prefix='/api')


    return app



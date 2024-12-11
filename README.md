# LibraryAPI

A Flask-based API for managing a library system. The project allows an admin to add and edit books and authors, while users can borrow books. It uses SQLAlchemy for the database and Flask-Login for user authentication.

## Features:
- Admins can manage books and authors.
- Users can borrow books.
- Secure user authentication with login and registration.
- Easily extensible with Flask Blueprints for modularity.

## Installation:
1. Clone the repository:
   ```bash
   git clone https://github.com/simayadolahi/LibraryAPI.git
   
2. Install the dependencies:
  pip install -r requirements.txt
3. Set up the database and run migrations:
  flask db upgrade
4. Run the application:
  python run.py

You can adjust any details or add more information based on your specific app features.


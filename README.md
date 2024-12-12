This project is a Library Management System built using Flask, a micro web framework in Python. It provides functionalities for managing books and authors, where administrators can add or edit books and authors, and users can borrow books. It implements both server-side logic and RESTful APIs for seamless interaction with the backend.

## Key Features

- Admin Functionalities:

  Add, edit, and delete books.

  Add, edit, and delete authors.

- User Functionalities:

  View available books.

  Borrow books.

- API Functionalities:

  Provides RESTful APIs for books and authors.

  Allows programmatic access to manage library resources.

### Flask Extensions:

- Flask-WTF: Simplified form creation and validation.

- Flask-Login: User authentication and session management.

- SQLAlchemy: Object-relational mapping (ORM) for database interactions.

- Flask-Blueprint: Modular application architecture.

- Flask-RESTful: Simplified API development.

## Project Setup

### Prerequisites

- Python 3.11 or later

- A virtual environment is recommended to manage dependencies.

#### Installation Steps

- Clone the repository:

  git clone https://github.com/simayadolahi/LibraryAPI.git
  cd LibraryAPI

- Create and activate a virtual environment:
  python -m venv venv
  
  source venv/bin/activate   # On Windows: venv\Scripts\activate
  
- Install the required dependencies: 
  pip install -r requirements.txt
- Run database migrations: 
  flask db upgrade
- Start the application: 
  flask run

The application will be available at http://127.0.0.1:5000/

## API Endpoints

The following RESTful API endpoints are available for managing the library system:

### Books Endpoints
- `GET /api/books`: Retrieves a list of all books.
- `GET /api/books/<id>`: Retrieves details of a specific book by ID.
- `POST /api/books`: Adds a new book.
- `PUT /api/books/<id>`: Updates a book's details by ID.
- `DELETE /api/books/<id>`: Deletes a book by ID.

### Authors Endpoints
- `GET /api/authors`: Retrieves a list of all authors.
- `GET /api/authors/<id>`: Retrieves details of a specific author by ID.
- `POST /api/authors`: Adds a new author.
- `PUT /api/authors/<id>`: Updates an author's details by ID.
- `DELETE /api/authors/<id>`: Deletes an author by ID.

### User Endpoints
- `POST /api/users`: Adds a new user (registers).
- `GET /api/users`: Retrieves a list of all users.
- `GET /api/users/<id>`: Retrieves details of a specific user by ID.
- `PUT /api/users/<id>`: Updates a specific user's details by ID
- `DELETE /api/users/<id>`: Deletes a user by ID.

## Application Structure

/templates/: HTML templates for front-end views.

/static/: Static files like CSS, JavaScript, and images.

/blueprints/: Modular blueprints for the application.

/migrations/: Database migration scripts.

run.py: Entry point for running the application.

Contributions are welcome! Feel free to fork this repository, make your changes, and submit a pull request.



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

The application will be available at http://127.0.0.1:5000/.

### API Endpoints

- Base URL
 http://127.0.0.1:5000/api/
### Books Endpoints
#### Get All Books
Method: GET
URL: /books
Description: Retrieve all books in the library.
Response Example:
[
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "available": true
    },
    {
        "id": 2,
        "title": "1984",
        "author": "George Orwell",
        "available": false
    }
]
#### Add a New Book
Method: POST
URL: /books
Description: Add a new book to the library.
- Request Body Example:
{
    "title": "New Book Title",
    "author": "Author Name",
    "available": true
}

- Response Example:
{
    "message": "Book added successfully.",
    "book_id": 3
}

#### Edit a Book
Method: PUT
URL: /books/{id}
Description: Update details of an existing book.

- Request Body Example:

{
    "title": "Updated Title",
    "author": "Updated Author",
    "available": false
}

- Response Example:

{
    "message": "Book updated successfully."
}

#### Delete a Book
Method: DELETE
URL: /books/{id}
Description: Delete a book by its ID.

- Response Example:

{
    "message": "Book deleted successfully."
}

### Authors Endpoints
#### Get All Authors
Method: GET
URL: /authors
Description: Retrieve all authors in the library.
Response Example:
[
    {
        "id": 1,
        "name": "F. Scott Fitzgerald"
    },
    {
        "id": 2,
        "name": "George Orwell"
    }
]

#### Add a New Author
Method: POST
URL: /authors
Description: Add a new author to the library.

- Request Body Example:

{
    "name": "J.K. Rowling"
}

- Response Example:

{
    "message": "Author added successfully.",
    "author_id": 3
}

## Application Structure

/templates/: HTML templates for front-end views.

/static/: Static files like CSS, JavaScript, and images.

/blueprints/: Modular blueprints for the application.

/migrations/: Database migration scripts.

run.py: Entry point for running the application.

Contributions are welcome! Feel free to fork this repository, make your changes, and submit a pull request.



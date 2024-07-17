# Library Management System

A Django-Ninja based library management system API.

## Technologies Used

- Python 3.8+
- Django 4.2
- Django-Ninja 0.22

## Setup Instructions

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Apply migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Run the development server: `python manage.py runserver`

## API Endpoints

- GET /api/books: List all books
- POST /api/books: Create a new book
- GET /api/books/{book_id}: Retrieve a specific book
- PUT /api/books/{book_id}: Update a book
- DELETE /api/books/{book_id}: Delete a book
- GET /api/available-books: List available books
- POST /api/borrow: Borrow a book
- POST /api/return: Return a book

## Testing

Run the test suite with: manage.py test library
## Deployment

Follow these steps to deploy the application:

1. Set DEBUG = False in settings.py
2. Update ALLOWED_HOSTS in settings.py
3. Set up a production database
4. Collect static files: `python manage.py collectstatic`
5. Use a production-ready web server like Gunicorn
6. Set up HTTPS using a reverse proxy like Nginx

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes and write tests
4. Submit a pull request

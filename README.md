# ShelfWise-Server - Django Book Management API

A RESTful API for managing books, users, and reading lists built with Django REST Framework.

## Features

- User registration and authentication
- Book creation, management, and sharing
- Personal reading lists with custom ordering
- Comprehensive error handling
- RESTful API design

## Requirements

- Python 3.8+
- Django 4.2+
- Django REST Framework
- PostgreSQL (recommended) or MySQL/SQLite (default)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/nasif-muhamed/ShelfWise-Server.git
cd django-book-management-api
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Setup

Create a `.env` file in the project root:

```env
ACCESS_TOKEN_LIFETIME="NUMBER OF MINUTES"
REFRESH_TOKEN_LIFETIME="NUMBER OF DAYS"
DJANGO_SECRET_KEY="your-django-secret-key"
DEBUG="True"
ALLOWED_HOSTS="*"
JWT_SECRET_KEY="your-jwt-secret-key"
JWT_ALGORITHM="your-jwt-algorithm"
CORS_ALLOWED_ORIGINS="http://localhost:8000"
DJANGO_LOG_LEVEL="DEBUG"
EMAIL_HOST_USER="your-email-host-user"
EMAIL_HOST_PASSWORD_USER="your-host-user-password"
DB_ENGINE="your-db-engine-postgres-recommended"
DB_NAME="your-db-name"
DB_USER="your-db-user"
DB_PASSWORD="your-db-password"
DB_HOST="your-db-host-or-default-localhost"
DB_PORT="your-db-port-or-default-5432"
```

### 5. Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run the Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Documentation

### Base URL
```
http://localhost:8000/
```

### Authentication
The API uses Token-based authentication. Include the token in the Authorization header:

**Exception:** register, verify-otp and login
```
Authorization: Token <your-token-here>
```

---

## User Management Endpoints

### Register User
**POST** `/users/register/`

Sending a verification email to register a user.

**Request Body:**
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
}
```

**Response (200 OK):**
```json
{
    "message": "OTP sent successfully",
    "expires_at": "2025-07-18T04:40:40.725017"
}
```

### Verify User OTP
**POST** `/users/verify-otp/`

Register a new user account by verifying the OTP send to email.

**Request Body:**
```json
{
    "username": "johndoe",
    "otp": "000000",
}
```

**Response (201 Created):**
```json
{
    "message": "User registered successfully",
    "id": 2
}
```

### Login
**POST** `/users/login/`

Authenticate user and receive access token.

**Request Body:**
```json
{
    "username": "johndoe",
    "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
    "refresh": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "access": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Get User Profile
**GET** `/users/profile/`

Get current user's profile information.

**Response (200 OK):**
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "",
    "last_name": "",
    "created_at": "2024-01-15T10:30:00Z",
    etc...
}
```

### Update User Profile
**PATCH** `/api/auth/profile/`

Update current user's profile information.

**Request Body:**
```json
{
    "first_name": "Jhon",
    "last_name": "Doe",
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "first_name": "Jhon",
    "last_name": "Doe",
     etc...
}
```

---

## Book Management Endpoints

### List All Books
**GET** `/books/`

Retrieve all books available in the system.

**Response (200 OK):**
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/books/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "The Great Gatsby",
            "authors": ["F. Scott Fitzgerald"],
            "genre": "Classic Fiction",
            "publication_date": "2025-07-18T10:18:44.339935Z",
            "description": "A classic American novel set in the Jazz Age.",
            "uploaded_by": {
                "id": 1,
                "username": "johndoe",
                "first_name": "John",
                "last_name": "Doe",
            }
        }
    ]
}
```

### Create Book
**POST** `/books/`

Create a new book entry.

**Request Body:**
```json
{
    "title": "To Kill a Mockingbird",
    "authors": ["Harper Lee"],
    "genre": "Fiction",
    "description": "A gripping tale of racial injustice and childhood innocence."
}
```

**Response (201 Created):**
```json
{
    "id": 2,
    "title": "To Kill a Mockingbird",
    "authors": ["Harper Lee"],
    "genre": "Fiction",
    "publication_date": "2025-07-18T10:18:44.339935Z",
    "description": "A gripping tale of racial injustice and childhood innocence.",
    "uploaded_by": "johndoe"
}
```

### Get Book Details
**GET** `/books/{id}/`

Retrieve detailed information about a specific book.

**Response (200 OK):**
```json
{
    "id": 1,
    "title": "The Great Gatsby",
    "authors": ["F. Scott Fitzgerald"],
    "genre": "Classic Fiction",
    "publication_date": "2025-07-18T10:18:44.339935Z",
    "description": "A classic American novel set in the Jazz Age.",
    "uploaded_by": "johndoe"
}
```

### Update Book
**PATCH** `/books/{id}/`

Update book information (only by the creator).

**Request Body:**
```json
{
    "title": "The Great Gatsby (Updated)",
    "genre": "Classic Literature",
    "publication_date": "1925-04-10",
    "description": "An updated description of this classic American novel."
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "title": "The Great Gatsby (Updated)",
    "authors": ["F. Scott Fitzgerald"],
    "genre": "Classic Literature",
    "publication_date": "2025-07-18T10:18:44.339935Z",
    "description": "An updated description of this classic American novel.",
    "uploaded_by": "johndoe",
}
```

### Delete Book
**DELETE** `/books/{id}/`

Delete a book (only by the creator).

**Response (204 No Content):**
```
No content
```

---

## Reading List Endpoints

### List User's Reading Lists
**GET** `/lists/reading-lists/`

Get all reading lists for the authenticated user.

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "name": "Summer Reading 2024",
        "description": "Books to read this summer",
        "created_at": "2024-01-15T10:30:00Z",
    },
    {
        "id": 2,
        "name": "Classic Literature",
        "description": "Timeless literary works",
        "created_at": "2024-01-16T09:15:00Z",
    }
]
```

### Create Reading List
**POST** `/lists/reading-lists/`

Create a new reading list.

**Request Body:**
```json
{
    "name": "Mystery Novels",
    "description": "Collection of thrilling mystery books"
}
```

**Response (201 Created):**
```json
{
    "id": 3,
    "name": "Mystery Novels",
    "description": "Collection of thrilling mystery books",
    "created_at": "2024-01-17T14:20:00Z",
}
```

### Get Reading List Details
**GET** `/lists/reading-lists/{id}/`

Get detailed information about a specific reading list including books.

**Response (200 OK):**
```json
{
    "id": 1,
    "name": "Summer Reading 2024",
    "description": "Books to read this summer",
    "created_at": "2024-01-15T10:30:00Z",
    "books": [
        {
            "id": 1,
            "book": 2,
            "order": 1,
        },
        {
            "id": 2,
            "book": 1,
            "order": 2,
        }
    ]
}
```

### Update Reading List
**PATCH** `/lists/reading-lists/{id}/`

Update reading list information.

**Request Body:**
```json
{
    "name": "Summer Reading 2024 (Updated)",
    "description": "Updated collection of summer books"
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "name": "Summer Reading 2024 (Updated)",
    "description": "Updated collection of summer books",
    "created_at": "2024-01-15T10:30:00Z",
}
```

### Delete Reading List
**DELETE** `/lists/reading-lists/{id}/`

Delete a reading list and all its associated books.

**Response (204 No Content):**
```
No content
```

---

## Reading List Book Management

### Add Book to Reading List
**POST** `/lists/reading-list-book/`

Add a book to a specific reading list.

**Request Body:**
```json
{
    "reading_list": 1,
    "book": 2
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "order": 1,
    "reading_list": 1,
    "book": 2
}
```

### Remove Book from Reading List
**DELETE** `/lists/reading-list-book/{book_id}/`

Remove a book from a reading list.

**Response (204 No Content):**
```
No content
```

### Update Book Order in Reading List
**PATCH** `/lists/reading-list-book/{book_id}/`

Update the order of a book within a reading list.

**Request Body:**
```json
{
    "new_order": 3
}
```

**Response (200 OK):**
```json
{
    "id": 2,
    "order": 3,
    "reading_list": 1,
    "book": 2
}
```

**NB**: Not included some url endpoints for admin user and publisher only views.
---
## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For support or questions, please open an issue in the GitHub repository.
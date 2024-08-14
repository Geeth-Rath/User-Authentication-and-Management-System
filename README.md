# User Authentication and Management System
## Overview
This project is a user authentication and management system built with FastAPI. It features user registration, login, profile management, and JWT-based authentication. The system uses SQLAlchemy for database interactions and SQLite for storage.

## Features
* User Registration: Allows users to register with a username, email, and password.
* User Login: Authenticates users and issues JWT tokens.
*   User Profile Management: Retrieve, update, and delete user profiles.
*   JWT Authentication: Secure token-based authentication.

## Requirements
*   Python 3.8+
*   FastAPI
*   Uvicorn
*   SQLAlchemy 2.0
*   SQLite
*   Passlib
*   Python-Jose
*   Pydantic
*   pytest
*   python-dotenv



## Source code
git clone https://github.com/yourusername/user_auth_system.git
Navigate to the Project Directory


## Create a .env File

Create a .env file in the root directory with the following content:

* `SECRET_KEY=your_secret_key
* ALGORITHM=HS256
* DATABASE_URL=sqlite:///./test.db`

Replace them with your choice.

## Running the Application
To run the FastAPI application, use the following command:

`uvicorn app.main:app --reload`
This will start the application on http://127.0.0.1:8000.

## API Endpoints
POST /users/register

* Description: Register a new user.
* Request Body: { "username": "string", "email": "string", "password": "string" }
* Response: { "id": "integer", "username": "string", "email": "string", "created_at": "string" }

POST /users/login

* Description: Authenticate a user and return a JWT token.
* Request Body: { "username": "string", "password": "string" }
* Response: { "access_token": "string", "token_type": "bearer" }

GET /users/me

* Description: Retrieve details of the authenticated user.
* Authorization: Bearer token required.
* Response: { "id": "integer", "username": "string", "email": "string", "created_at": "string" }

PUT /users/me

* Description: Update the authenticated user's details.
* Request Body: { "username": "string", "email": "string", "password": "string" }
* Authorization: Bearer token required.
* Response: { "id": "integer", "username": "string", "email": "string", "created_at": "string" }

DELETE /users/me

* Description: Delete the authenticated user's account.
* Authorization: Bearer token required.
* Response: { "id": "integer", "username": "string", "email": "string", "created_at": "string" }



## Testing
To ensure the application works correctly, run the tests using pytest:
`pytest`

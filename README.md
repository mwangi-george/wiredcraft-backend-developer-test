# Wiredcraft Users API

Welcome to the Wiredcraft Users API project! This API provides robust user management functionality built on **FastAPI, SQLAlchemy, Alembic, asyncpg, and PostgreSQL.**

## Features

-   **User Registration**: Register new users securely.

-   **User Authentication**: Log in users with password authentication.

-   **User Management**: Update user details, remove users, and fetch user information.

-   **Secure Endpoints**: Access endpoints securely using OAuth2.

## Technologies Used

-   **FastAPI**: Fast, modern web framework for building APIs with Python.

-   **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library.

-   **Alembic**: Database migration tool for SQLAlchemy.

-   **asyncpg**: Async PostgreSQL driver for Python.

-   **PostgreSQL**: Powerful, open-source relational database.

## Getting Started

**Prerequisites**

Ensure you have the following installed:

-   Python 3.10+
-   PostgreSQL
-   uv installed

## Installation

Clone the repository:

```         
git clone https://github.com/mwangi-george/wiredcraft-backend-developer-test.git
cd wiredcraft-backend-developer-test
```

## Install dependencies using uv:

```         
uv install
```

## Running the Application
1. Set up your environment variables. Example .env file:

```
DEV_DB_URL=postgresql://username:password@localhost/dev_db
PROD_DB_URL=postgresql://username:password@remote_host/prod_db

DEV_ACCESS_TOKEN_EXPIRY_TIME_IN_MINUTES=60
PROD_ACCESS_TOKEN_EXPIRY_TIME_IN_MINUTES=60

DEV_PASSWORD_RESET_TOKEN_EXPIRY_IN_MINUTES=20
PROD_PASSWORD_RESET_TOKEN_EXPIRY_IN_MINUTES=20

ALGORITHM=HS256
JWT_SECRET_KEY=mysecretkey

```

2. Run database migrations with Alembic:

``` 
alembic upgrade head
```

3. Start the FastAPI server:

```
uvicorn main:app --reload --port 8000
```

4. Visit http://localhost:8000/docs for Swagger UI or http://localhost:8000/redoc for ReDoc to explore the API.

## Configuration

**Environment Variables**

* **DEV_DB_URL, PROD_DB_URL**: Database connection URLs for development and production environments.

* **DEV_ACCESS_TOKEN_EXPIRY_TIME_IN_MINUTES**, **PROD_ACCESS_TOKEN_EXPIRY_TIME_IN_MINUTES**: Expiry time for access tokens in minutes.

* **DEV_PASSWORD_RESET_TOKEN_EXPIRY_IN_MINUTES**, **PROD_PASSWORD_RESET_TOKEN_EXPIRY_IN_MINUTES**: Expiry time for password reset tokens in minutes.

* **ALGORITHM**: JWT signing algorithm.

* **JWT_SECRET_KEY**: Secret key for JWT token signing and verification.

## API Documentation

**Endpoints**

* **POST** /api/v1/users/register: Register a new user.
* **POST** /api/v1/users/login: Log in a user.
* **PATCH** /api/v1/users/update: Update a user's information.
* **DELETE** /api/v1/users/{user_id}: Remove a user by ID.
* **GET** /api/v1/users/all: Get all users (paginated).
* **GET** /api/v1/users/user: Get a user by ID.
* **GET** /api/v1/me/: Secure endpoint to get the currently logged-in user.


## Security

The application uses JWT for secure authentication and authorization. Tokens are generated using a specified algorithm and secret key stored in environment variables.

## Contributing

I welcome contributions to enhance the functionality and maintainability of this project. To contribute:

1. Fork the repository.
2. Create your feature branch (git checkout -b feature/YourFeature).
3. Commit your changes (git commit -am 'Add some feature').
4. Push to the branch (git push origin feature/YourFeature).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

**Author**: George Mwangi
**Email**: mwangigeorge648@gmail.com


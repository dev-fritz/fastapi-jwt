# FastAPI-JWT
## Overview

FastAPI-JWT is a project that demonstrates how to implement JWT (JSON Web Tokens) authentication in a FastAPI application. This project is designed to provide a secure and scalable solution for managing user authentication and authorization.

## Features

- JWT Authentication: Securely authenticate users using JSON Web Tokens.
- Endpoint Protection: Easily protect API endpoints to ensure they are only accessible by authenticated users.
- Token Refresh: Implement token refresh logic to maintain user sessions.
- Role-Based Access Control: Control access to resources based on user roles.

## Endpoints
### Authentication Endpoints

    POST /login: Generates a new JWT token for a user. Requires a valid email and password.

### Protected Endpoints

    GET /user: A sample protected endpoint that requires a valid JWT token to access.

### User Management Endpoints

    POST /register: Registers a new user. Requires a email, name and password.

## How It Works

- User Registration: Users register by sending a POST request to /users with their username and password.
- User Authentication: Users authenticate by sending a POST request to /token with their username and password. The server validates the credentials and returns a JWT token.
- Accessing Protected Resources: Users access protected resources by including the JWT token in the Authorization header of their requests.

## Security

- JWT Tokens: All tokens are signed and optionally encrypted to ensure their integrity and confidentiality.
- Password Hashing: Passwords are hashed using bcrypt for secure storage.
- Token Expiry: Access tokens have a short expiry time, and refresh tokens can be used to obtain new access tokens without requiring the user to re-authenticate.

## Getting Started

- Install the required dependencies using pip install -r requirements.txt.
- Run the FastAPI application using uvicorn main:app --reload.

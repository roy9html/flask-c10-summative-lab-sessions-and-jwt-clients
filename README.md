# Flask Notes API with JWT Authentication

## Project Description

A secure RESTful Flask API for managing personal notes with JWT-based authentication and full CRUD operations. Users can create, read, update, and delete their own notes with pagination support. The API ensures that users can only access and modify their own data, providing robust security and data isolation. This project was built as a summative lab for a backend engineering course, demonstrating best practices in API development, authentication, and database management.

## Features

- **JWT-based Authentication**: Secure user authentication with access and refresh tokens
- **Full CRUD Operations**: Create, Read, Update, and Delete notes
- **User-specific Data Isolation**: Users can only access their own notes
- **Pagination**: Efficient data retrieval with page and per_page parameters
- **Note Categories**: Organize notes with custom categories
- **Archive Functionality**: Archive and unarchive notes
- **Input Validation**: Data validation using Marshmallow schemas
- **Database Migrations**: Version-controlled database schema with Flask-Migrate
- **Database Seeding**: Automatic generation of sample data for testing
- **Comprehensive Test Suite**: 22 passing tests with 81% code coverage
- **Error Handling**: Appropriate HTTP status codes and error messages

## Tech Stack

- **Flask 2.2.2**: Web framework
- **Flask-SQLAlchemy 3.0.3**: ORM for database operations
- **Flask-Migrate 4.0.0**: Database migration management
- **Flask-JWT-Extended 4.5.2**: JWT token authentication
- **Flask-Bcrypt 1.0.1**: Password hashing
- **Marshmallow 3.20.1**: Data validation and serialization
- **SQLite**: Development database
- **Pytest 7.2.0**: Testing framework
- **Faker 15.3.2**: Sample data generation

## Project Structure


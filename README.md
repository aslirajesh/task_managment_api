# Task Management API

## Overview
This is a Task Management API built using FastAPI. The API allows users to manage their tasks with functionalities for user registration, authentication, and task management (CRUD operations). 

## Features
- **User Registration**: Register with a username and password.
- **User Authentication**: Log in using username and password, with JWT token issuance.
- **Task Management**: Create, read, update, and delete tasks.
- **Token Management**: Authentication tokens with expiration.

## Requirements
- Python 3.8+
- SQLite (default) or another SQL database

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/aslirajesh/task_managment_api.git
    cd task_management_api
    ```

2. **Create and activate a virtual environment** (optional but recommended):
    ```bash
    python -m venv env
    source env/bin/activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. **Run the application**:
    ```bash
    uvicorn app.main:app --reload
    ```

2. **Access the API documentation**:
    Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the interactive API documentation provided by FastAPI.

## API Endpoints

### Authentication

- **POST /register/**: Register a new user.
  - Request Body:
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```

- **POST /token**: Obtain a token for authentication.
  - Request Body (Form Data):
    - `username`: `string`
    - `password`: `string`

### Tasks

- **POST /tasks/**: Create a new task.
  - Request Body:
    ```json
    {
      "title": "string",
      "description": "string",
      "is_completed": false
    }
    ```

- **GET /tasks/**: Retrieve all tasks for the authenticated user.

- **GET /tasks/{task_id}**: Retrieve a specific task by ID.

- **PUT /tasks/{task_id}**: Update a specific task by ID.
  - Request Body:
    ```json
    {
      "title": "string",
      "description": "string",
      "is_completed": false
    }
    ```

- **DELETE /tasks/{task_id}**: Delete a specific task by ID.



# Budget Planning API

## Introduction

Welcome to the Budget Planning API! This server application is designed to assist users in planning their monthly budget by managing expenses and revenues. It provides a set of endpoints for user management, transaction operations, and data visualization. The data is stored in MongoDB for efficient data management.

## Technologies Used

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python.
- **MongoDB**: A flexible, scalable, and high-performance document-oriented NoSQL database.
- **Matplotlib**: A comprehensive library for creating static, animated, and interactive visualizations in Python.

## Endpoints

### Users

- **Signup**: Allows users to create a new account.
- **Signin**: Allows users to authenticate and sign in.
- **Update Profile**: Enables users to update their profile information.

### Operations

- **Add Operation**: Adds a new transaction operation for the user.
- **Delete Operation**: Deletes a transaction operation by its ID.
- **Update Operation**: Updates an existing transaction operation.
- **Get Operations by Date Range**: Retrieves all user operations within a specified date range.
- **Get User Operations**: Retrieves all operations for a specific user.
- **Get Operation by ID**: Retrieves a specific operation by its unique identifier.

### Visualization

- **Get yearly expenses vs revenues bar**: Generates visual bar for user's expenses against user's revenues of all year divide to months.
- **Get yearly expenses vs revenues graph**: Generates visual graph for user's expenses against user's revenues of all year divide to months. 
- **Get monthly expenses vs revenues bar**: Generates visual bar for user's expenses against user's revenues of specific month . 
- **Get yearly balance bar**: Generates visual bar for user's balance  of all year divide to months. 
- **Get yearly expenses vs revenues graph**: Generates visual graph for user's balance  of all year divide to months 


## files tree:

    .
    ├─ app\
    │ ├─ models\
    │ │ ├─ operation.py                # Model for transaction operation
    │ │ ├─ operation_type.py           # Enum for operation types - expense and revenue
    │ │ └─ user_model.py               # Model for user
    │ ├─ routers\
    │ │ ├─ operation_router.py         # Routes for transaction operations
    │ │ ├─ visualization_router.py     # Routes for data visualization
    │ │ └─ user_router.py              # Routes for user operations
    │ ├─ services\
    │ │ ├─ db_service.py               # Connections to db
    │ │ ├─ operations_service.py       # Logic for transaction operations
    │ │ ├─ visualization_service.py   # Logic for data visualization
    │ │ └─ users_service.py            # Logic for user operations
    ├─ tests\
    │ ├─ test_operation.py             # Tests for operation_service page
    │ └─ test_user.py                  # Tests for user_service page
    ├─ utils\
    │ └─ log.py                     # Decorator for logs
    ├─ .gitignore                       # Project gitignore file
    ├─ README.md                        # Project README file
    ├─ main.py                          # Main application logic
    └─ requirements.txt                 # Dependencies for the project

## Installation

1. Clone the repository: `git clone https://github.com/miryamW/budgetPlanningAi`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up MongoDB and ensure it's running locally or on a remote server.
4. Configure the MongoDB connection in the application settings.

## Running the Server

To start the FastAPI server, run the following command:
```bash
 uvicorn main:app --reload
```
The server will start running at `http://localhost:8080` by default.

## Documentation

After running the server, you can access the API documentation and interactive UI (provided by Swagger UI) by navigating to `http://localhost:8080/docs` in your web browser.

## Contributing

Contributions are welcome! Feel free to open issues or pull requests for any improvements or features you'd like to add to the project.


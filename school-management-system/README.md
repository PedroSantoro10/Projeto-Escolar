# School Management System

This is a Flask-based school management system designed to manage professors and students efficiently. The application allows for user registration, login, and management of various functionalities related to school administration.

## Project Structure

```
school-management-system
├── app
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   └── templates
│       └── base.html
├── requirements.txt
├── config.py
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd school-management-system
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Edit the `config.py` file to set up your database URI and secret key.

## Running the Application

To run the application, use the following command:
```
flask run
```

## Usage

- Navigate to `http://127.0.0.1:5000` in your web browser to access the application.
- You can register as a professor or student and manage your profiles.

## Contributing

Feel free to submit issues or pull requests for improvements and bug fixes.
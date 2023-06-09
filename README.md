# **Scholar Stream - Online Learning Platform**

Scholar Stream is an innovative online learning platform built with Django. It provides interactive and streamlined learning experience, bringing high-quality educational content right to your fingertips.

**Table of Contents**

- [Getting Started]
- [Prerequisites]
- [Installation]
- [Usage]

**Getting Started**

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

**Prerequisites**

Ensure you have the following software installed on your system:

- Python 3.8 or later
- Django 3.2 or later
- pip (Python package manager)

**Installation**

1. Clone the repository

git clone https://github.com/yourgithubusername/scholar-stream.git

2. Navigate to the project directory

cd scholar-stream

3. Create a virtual environment

python3 -m venv env

4. Activate the virtual environment

sourceenv/bin/activate # On Windows, use `.\env\Scripts\activate`

5. Install the required packages

pip install -r requirements.txt

6. Make migrations to the database

python manage.py makemigrations

7. Apply the migrations

python manage.py migrate

8. Run the Django development server

python manage.py runserver

You should now be able to access the application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

**Usage**

For details on how to use Scholar Stream, please refer to our user manual located in the docs directory.

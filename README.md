# CerdasFinancial-api

This is a Restful API for Cerdas Financial App. It allows user to create account, get courses, and subscribe to this apps.

## Feature
- Create account
- Get courses
- Subscribe


## Technology Stack
- Language: Python
- Framework: Flask
- Database: MySQL
- Authentication: JWT (JSON Web Token)


## Installation
Clone the repository:
```bash
git clone https://github.com/gitchan07/CerdasFinancial-api
cd CerdasFinancial-api
```

Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

or 

```bash
pipenv install
```

Set up the database:

Create a MySQL database. 
Update the database configuration in the utils/connection.py file with your MySQL credentials.

Run the application:

```bash
flask run
```

License
This project is licensed under the MIT License. See the LICENSE file for details.
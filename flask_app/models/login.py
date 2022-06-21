from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
from flask_bcrypt import Bcrypt
from flask_app import app

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Login:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data['password']
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM logins;"
        results = connectToMySQL(DATABASE).query_db(query)

        all_logins = []
        for login in results:
            all_logins.append(login)

        return all_logins

    @classmethod
    def get_one_email(cls, data):
        query = "SELECT * FROM logins "
        query += "WHERE email = %(email)s"

        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def create_login(cls, data):
        query = "INSERT INTO logins (first_name, last_name, email, password) "
        query += "VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_one_id(cls, data):
        query = "SELECT * FROM logins "
        query += "WHERE id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_email(email):
        is_valid = True

        if Login.get_one_email(email):
            flash("Email address is already in use!", 'email_error')
            is_valid = False
        elif not EMAIL_REGEX.match(email['email']):
            flash("Invalid email address!", 'email_error')
            is_valid = False
        return is_valid

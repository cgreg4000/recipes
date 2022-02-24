from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"

        results = connectToMySQL('recipes_schema').query_db(query, data)

        if len(results) == 0:
            return False

        else:
            return User(results[0])

    @staticmethod
    def validate_new_user(data):
        is_valid = True

        if len(data['first_name']) < 2 or len(data['first_name']) > 50:
            flash("First name must be from 2 to 50 characters long.")
            is_valid = False
        if len(data['last_name']) < 2 or len(data['last_name']) > 50:
            flash("Last name must be from 2 to 50 characters long.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email format.")
            is_valid = False
        if User.get_user_by_email(data):
            flash("Email is already registered.")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters long.")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Password and Confirm Password must be the same.")
            is_valid = False

        return is_valid

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"

        results = connectToMySQL('recipes_schema').query_db(query, data)

        return results
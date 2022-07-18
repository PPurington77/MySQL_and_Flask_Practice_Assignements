from flask_app.config.mysqlconnection import connectToMySQL 
import re
from flask import flash
from flask_app import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$')
CONFIRM_PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.full_name = data['first_name'] + ' ' + data['last_name']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL('login_and_registration_db').query_db(query)
        all_users = []
        for user in results:
            all_users.append(cls(user))
        return all_users

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() );"
        
        return connectToMySQL('login_and_registration_db').query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('login_and_registration_db').query_db(query, data)

        if result:
            user = cls(result[0])
            return user
        return False

    @classmethod
    def update(cls, data):
        query = "UPDATE users SET user_name = %(user_name)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('login_and_registration_db').query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('login_and_registration_db').query_db(query, data)

    @classmethod
    def get_one_login(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('login_and_registration_db').query_db(query, data)

        if result:
            user = cls(result[0])
            return user
        return False

    @staticmethod
    def validate(data):
        is_valid = True

        if len(data['first_name']) < 2:
            flash('First Name does not have the required length', 'err_user_first_name')
            print('first')
            is_valid = False

        elif not data['first_name'].isalpha():
            flash('First Name can only include letters', 'err_user_first_name')
            print('first lett')
            is_valid = False

        if len(data['last_name']) < 2:
            flash('Last Name does not have the required length', 'err_user_last_name')
            print('last')
            is_valid = False

        elif not data['last_name'].isalpha():
            flash('Last Name can only include letters', 'err_user_last_name')
            print('last lett')
            is_valid = False

        if not EMAIL_REGEX.match(data['email']):
            flash('Email address is not valid', 'err_user_email')
            print('email')
            is_valid = False


        if not PASSWORD_REGEX.match(data['password']):
            flash('Password must include: 8 characters, one uppercase letter, one lower case letter, one number, and one special character', 'err_user_password')
            print('password ')
            is_valid = False

        if data['password'] != data['confirm_password']:
            flash('Passwords must match', 'err_user_password')
            print(' Passwords do not match ')
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True
        potential_user = User.get_one_login({'email': data['email']})
        print(potential_user)
        if not bcrypt.check_password_hash(potential_user.password, data['password']):
            # flash("Incorrect Password", 'err_user_password_login')
            print(is_valid)
            is_valid = False

        print(is_valid)
        return is_valid
        

        
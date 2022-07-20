from flask_app.config.mysqlconnection import connectToMySQL 
import re
from flask import flash
from flask_app import bcrypt
from flask_app.models import model_user

DATABASE = 'recipes_db'

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.under_30 = data['under_30']
        self.made = data['made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.owner = {}



    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id"
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        if results:
            all_recipes = []
            for dict in results:
                recipe = cls(dict)
                user_data = {
                    'id':dict['users.id'],
                    'first_name':dict['first_name'],
                    'last_name':dict['last_name'],
                    'email':dict['email'],
                    'password':dict['password'],
                    'created_at':dict['users.created_at'],
                    'updated_at':dict['users.updated_at']
                }
                user = model_user.User(user_data)
                recipe.owner = user
                all_recipes.append(recipe)
            return all_recipes
        return []

    @classmethod
    def get_one_user_from_recipes(cls, data):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s"

        results = connectToMySQL(DATABASE).query_db(query, data)
        recipe = cls(results[0])

        user_data = {
            'id':results[0]['users.id'],
            'first_name':results[0]['first_name'],
            'last_name':results[0]['last_name'],
            'email':results[0]['email'],
            'password':results[0]['password'],
            'created_at':results[0]['users.created_at'],
            'updated_at':results[0]['users.updated_at']
        }
        owner = model_user.User(user_data)
        recipe.owner = owner
        return recipe

    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes (name, description, instruction, under_30, made, user_id, created_at, updated_at) VALUES (%(name)s, %(description)s, %(instruction)s, %(under_30)s, %(made)s, %(user_id)s, NOW(), NOW() );"
        
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)

        if result:
            recipe = cls(result[0])
            return recipe
        return False

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instruction = %(instruction)s, under_30 = %(under_30)s, made = %(made)s, updated_at = Now() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate(data):
        is_valid = True

        if len(data['name']) < 3:
            flash('Field required', 'err_name')
            print('name')
            is_valid = False

        if len(data['description']) < 3:
            flash('Field Required', 'err_description')
            print('last')
            is_valid = False

        if len(data['instruction']) < 3:
            flash('Field Required', 'err_instruction')
            print('instruction')
            is_valid = False

        if not data['made']:
            flash('Choose date', 'err_made')
            print('made')
            is_valid = False

        if 'under_30' not in data:
            flash('Does it take under 30 minutes to make?', 'err_under_30')
            print('under 30')
            is_valid = False 

        print(is_valid)
        return is_valid




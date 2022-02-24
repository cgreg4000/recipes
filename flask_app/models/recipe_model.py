from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user_model import User

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None

    @staticmethod
    def validate_recipe(data):

        is_valid = True

        if len(data['recipe_name']) < 3:
            is_valid = False
            flash("Recipe name must be at least 3 characters long.")
        if len(data['recipe_description']) < 3:
            is_valid = False
            flash("Recipe description must be at least 3 characters long.")
        if len(data['recipe_instructions']) < 3:
            is_valid = False
            flash("Recipe instructions must be at least 3 characters long.")
        if (data['recipe_date']) == '':
            is_valid = False
            flash("Please enter a date.")
        if 'under_30' not in data:
            is_valid = False
            flash('Please select "Yes" or "No" for under 30 minutes.')

        return is_valid

    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_made, under_30, user_id)VALUES (%(recipe_name)s, %(recipe_description)s, %(recipe_instructions)s, %(recipe_date)s, %(under_30)s, %(user_id)s)"

        result = connectToMySQL('recipes_schema').query_db(query, data)
        
        return result
    
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"

        result = connectToMySQL('recipes_schema').query_db(query, data)
        
        return result

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(recipe_name)s, description = %(recipe_description)s, instructions = %(recipe_instructions)s, date_made = %(recipe_date)s, under_30 = %(under_30)s WHERE id = %(recipe_id)s;"

        result = connectToMySQL('recipes_schema').query_db(query, data)
        
        return result

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"

        results = result = connectToMySQL('recipes_schema').query_db(query)

        recipes =[]

        for item in results:
            new_recipe = Recipe(item)

            user_data = {
                'id' : item['users.id'],
                'first_name' : item['first_name'],
                'last_name' : item['last_name'],
                'email' : item['email'],
                'password' : item['password'],
                'created_at' : item['users.created_at'],
                'updated_at' : item['users.updated_at']
            }

            new_recipe.user = User(user_data)

            recipes.append(new_recipe)

        return recipes

    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"

        result = connectToMySQL('recipes_schema').query_db(query, data)

        print(result)

        recipe = Recipe(result[0])

        user_data = {
                'id' : result[0]['users.id'],
                'first_name' : result[0]['first_name'],
                'last_name' : result[0]['last_name'],
                'email' : result[0]['email'],
                'password' : result[0]['password'],
                'created_at' : result[0]['users.created_at'],
                'updated_at' : result[0]['users.updated_at']
            }

        recipe.user = User(user_data)

        return recipe
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Recipe:
    db_name = 'user_recipes_schema'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30_min = data['under_30_min']
        self.date_made = data['date_made']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_recipe(cls, data):
        query = '''
        INSERT INTO recipes ( name, description, instructions, under_30_min, 
        date_made, user_id, created_at, updated_at )
        VALUES ( %(name)s, %(description)s, %(instructions)s, %(under_30_min)s, 
        %(date_made)s, %(user_id)s, NOW(), NOW() );
        '''
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_recipes = list()
        for row_from_db in results: all_recipes.append(cls(row_from_db))
        return all_recipes

    @classmethod
    def get_users_recipes(cls, data):
        query = "SELECT * FROM recipes WHERE user_id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        recipes = list()
        for row_from_db in results:
            recipe = {
                "id": row_from_db['id'],
                "name": row_from_db['name'],
                "description": row_from_db['description'],
                "instructions": row_from_db['instructions'],
                "under_30_min": row_from_db['under_30_min'],
                "date_made": row_from_db['date_made']
            }
            recipes.append(recipe)
        return recipes

    # Need to fix
    @classmethod
    def edit_recipe(cls, data):
        print(f"Editing: {data}")
        query = '''
        UPDATE recipes 
        SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, 
        under_30_min = %(under_30_min)s, date_mode = %(date_mode)s, updated_at = NOW() 
        WHERE id = %(id)s;
        '''
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def destroy_recipe(cls, data): 
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters.", "recipe")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("description must be at least 3 characters.", "recipe")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("description must be at least 3 characters.", "recipe")
            is_valid = False
        if recipe['date_made'] is None:
            flash("need to chose a date.", "recipe")
            is_valid = False
        return is_valid

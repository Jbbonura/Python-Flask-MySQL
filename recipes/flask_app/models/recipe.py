from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re

DATABASE = 'recipes'

class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made_on = data['date_made_on']
        self.under_thirty = data['under_thirty']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#! CREATE
#! class method to add a recipe to the DB 
    @classmethod
    def save(cls, data:dict ) -> int:
        query = "INSERT INTO recipes (name, description, user_id, instructions, date_made_on, under_thirty) VALUES ( %(name)s, %(description)s, %(user_id)s, %(instructions)s, %(date_made_on)s, %(under_thirty)s);"
        return connectToMySQL(DATABASE).query_db( query, data )
        #! the return stmt returns the id as an int of the recipe created

#! READ
    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        recipes = []
        for recipe in results: #! taking dicts from DB and making recipe objects
            recipes.append( cls(recipe) )
        return recipes

#! READ
    @classmethod
    def get_one(cls, data:dict) -> object:
        query = 'SELECT * FROM recipes WHERE id = %(id)s;'
        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0])

#! UPDATE
    @classmethod
    def update(cls, data:dict) -> object:
        query = 'UPDATE recipes SET name=%(name)s, description=%(description)s, user_id=%(user_id)s, instructions=%(instructions)s, date_made_on=%(date_made_on)s, under_thirty=%(under_thirty)s WHERE id = %(id)s;'
        return connectToMySQL(DATABASE).query_db(query, data)

#! DELETE
    @classmethod
    def destroy(cls, data:dict) -> object:
        query = 'DELETE FROM recipes WHERE id = %(id)s;'
        return connectToMySQL(DATABASE).query_db(query, data)

#! VALIDATION
    @staticmethod
    def validate_recipe(recipe:dict) -> bool:
        is_valid = True # ! we assume this is true
        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False
        return is_valid

from flask_app.config.mysqlconnection import connectToMySQL
from datetime import date
from flask import flash
# from flask_bcrypt import Bcrypt
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# bcrypt = Bcrypt(app) 
# bcrypt.generate_password_hash(password_string)
# bcrypt.check_password_hash(hashed_password, password_string)

# place class here, change file name to match

DATABASE = "login_reg" #<-- does this go here?
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
    def save(cls, data):
        query="INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(DATABASE).query_db(query, data)

    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        user = cls(result[0])
        print(user.password)
        return user

    @classmethod
    def get_one_by_id(cls, data):
        query="SELECT * FROM users WHERE id = %(id)s;"
        user = connectToMySQL(DATABASE).query_db(query, data)
        return cls(user[0])

    # @classmethod
    # def get_all(cls):
    #     query="SELECT * FROM users;"
    #     results=connectToMySQL('DATABASE').query_db(query)

    #     users = []

    #     for user in results:
    #         users.append(cls(user))
    #     return users



    # @classmethod
    # def get_one_by_name(cls, data):
    #     query="SELECT * FROM users WHERE title = %(title)s;"
    #     user = connectToMySQL('DATABASE').query_db(query, data)
    #     print(user[0])
    #     return cls(user[0])




    # @classmethod
    # def get_user_with_favorites(cls, data):
    #     query="SELECT * FROM users LEFT JOIN favorites ON favorites.user_id = users.id LEFT JOIN authors ON favorites.author_id = authors.id WHERE users.id = %(id)s;"
    #     results = connectToMySQL('users_schema').query_db(query, data)

    #     user = cls(results[0])

    #     for row_from_db in results:
    #         author_data = {
    #             'id' : row_from_db['authors.id'],
    #             'name' : row_from_db['name'],
    #             'created_at' : row_from_db['authors.created_at'],
    #             'updated_at' : row_from_db['authors.updated_at']
    #         }
    #         user.authors.append(author.Author(author_data))
    #     return user

    @staticmethod
    def validate_form(user):
        is_valid = True # we assume this is true
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(user['first_name']) < 1:
            flash("Must input first name")
            is_valid = False
        if len(user['last_name']) < 1:
            flash("Must input last name")
            is_valid = False
        if user['password'] != user['password_conf']:
            flash("Passwords must match!")
            is_valid = False
        return is_valid

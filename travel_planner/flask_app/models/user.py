from flask_app.config.mysqlconnection import connectToMySQL 
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('trip_schema').query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL('trip_schema').query_db(query, data)
        
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('trip_schema').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('trip_schema').query_db(query, data)
        return cls(results[0])

    @staticmethod
    def validate_user(user):
        is_valid = True 
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('trip_schema').query_db(query, user)
        if len(results) >= 1:
            flash("Email already in use." , "register")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.","register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.","register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address.","register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid = False
        if user['password']!= user['confirm']:
            flash("Passwords do not match","register")
        return is_valid
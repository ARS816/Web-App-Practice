from flask_app.config.mysqlconnection import connectToMySQL 
from flask import flash
from flask_app.models.user import User

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name= data['name']
        self.instructions= data['instructions']
        self.description= data['description']
        self.date_made= data['date_made']
        self.under= data['under']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_made, under, user_id) VALUES( %(name)s,%(description)s, %(instructions)s, %(date_made)s, %(under)s, %(user_id)s);"
        return connectToMySQL('recipes_schema').query_db(query,data)

    @classmethod
    def update(cls,data):
        query= "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under = %(under)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('recipes_schema').query_db(query,data)

    @classmethod
    def get_all(cls):
        query = """SELECT * from recipes
                    JOIN users on recipes.user_id = users.id;"""
        results = connectToMySQL('recipes_schema').query_db(query)
        all_recipes = []
        for row in results:
            posting_user = User({
                "id": row["user_id"],
                "email": row["email"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"],
                "password": row["password"]
            })
            new_recipe = Recipe({
                "id": row["id"],
                "name": row["name"],
                "description": row["description"],
                "instructions": row["instructions"],
                "date_made": row["date_made"],
                "under": row["under"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "user_id": posting_user
            })
            all_recipes.append(new_recipe)
        return all_recipes

    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * from recipes JOIN users on recipes.user_id = users.id WHERE recipes.id = %(id)s"
        results = connectToMySQL('recipes_schema').query_db(query, {"id": id})
        print(results[0])
        show_recipe = results[0]
        recipe = Recipe(show_recipe)
        user =  User({
                "id": show_recipe["user_id"],
                "email": show_recipe["email"],
                "first_name": show_recipe["first_name"],
                "last_name":show_recipe["last_name"],
                "created_at": show_recipe["users.created_at"],
                "updated_at": show_recipe["users.updated_at"],
                "password": show_recipe["password"]
            })
        recipe.user = user
        return recipe

    @classmethod
    def delete(cls, id):
            query = "DELETE from recipes WHERE recipes.id = %(id)s;"
            connectToMySQL('recipes_schema').query_db(query, {"id": id})
            return id

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data["name"]) < 3:
            flash("Recipe name required.", "recipes")
            is_valid = False
        if len(data["description"]) <3:
            flash("Description required", "recipes")
            is_valid = False
        if len(data["instructions"]) <3:
            flash("Instructions required", "recipes")
            is_valid = False
        if not (data["date_made"]):
            flash("Date created required.", "recipes")
            is_valid = False
        if "under" not in data:
            flash("Recipe length required.", "recipes")
            is_valid = False
        return is_valid
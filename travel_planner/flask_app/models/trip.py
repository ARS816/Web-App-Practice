from flask_app.config.mysqlconnection import connectToMySQL 
from flask import flash
from flask_app.models.user import User

class Trip:
    def __init__(self,data):
        self.id = data['id']
        self.destination= data['destination']
        self.start_date= data['start_date']
        self.end_date= data['end_date']
        self.plan= data['plan']
        self.created_at= data['created_at']
        self.updated_at= data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO trips (destination, start_date, end_date, plan, user_id) VALUES (%(destination)s, %(start_date)s, %(end_date)s, %(plan)s, %(user_id)s);"
        return connectToMySQL('trip_schema').query_db(query,data)

    @classmethod
    def delete(cls, id):
            query = "DELETE from trips WHERE trips.id = %(id)s;"
            connectToMySQL('trip_schema').query_db(query, {"id": id})
            return id

    @classmethod
    def update(cls,data):
        query= "UPDATE trips SET destination = %(destination)s, start_date = %(start_date)s, end_date = %(end_date)s, plan = %(plan)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('trip_schema').query_db(query,data)


    @classmethod
    def get_all(cls):
        query = """SELECT * from trips
                    JOIN users on trips.user_id = users.id;"""
        results = connectToMySQL('trip_schema').query_db(query)
        all_trips = []
        for row in results:
            posting_user = User({
                "id": row["user_id"],
                "email": row["email"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "password": row["password"]
            })
            new_trip = Trip({
                "id": row["id"],
                "destination": row["destination"],
                "start_date": row["start_date"],
                "end_date": row["end_date"],
                "plan": row["plan"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "user_id": posting_user
            })
            all_trips.append(new_trip)
        return all_trips

    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * from trips JOIN users on trips.user_id = users.id WHERE trips.id = %(id)s"
        results = connectToMySQL('trip_schema').query_db(query, {"id": id})
        print(results[0])
        show_trip = results[0]
        trip = Trip(show_trip)
        user =  User({
                "id": show_trip["user_id"],
                "email": show_trip["email"],
                "first_name": show_trip["first_name"],
                "last_name":show_trip["last_name"],
                "password": show_trip["password"]
            })
        trip.user = user
        return trip

    @staticmethod
    def validate_trip(data):
        is_valid = True
        if len(data["destination"]) < 3:
            flash("A trip destination must consist of at least 3 charaters.", "trips")
            is_valid = False
        if len(data["plan"]) <3:
            flash("A trip plan must consist of at least 3 charaters.", "trips")
            is_valid = False
        if not (data["start_date"]):
            flash("A start date is required.", "trips")
            is_valid = False
        if not (data["end_date"]):
            flash("An end date is required.", "trips")
            is_valid = False 
        return is_valid
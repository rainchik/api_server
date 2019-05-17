from flask import Flask
from flask_restful import Api, Resource, reqparse
import datetime
import psycopg2

app = Flask(__name__)
api = Api(app)

users = [
    {
        "name": "Nic",
        "dateOfBirth": "1989-03-03"
    }
]

def str_to_date(string_date):
    output = datetime.datetime.strptime(string_date, '%Y-%m-%d')
    return(output)

class User(Resource):
    def get(self, name):
        if not name.isalpha():
            return "Name contains not only letters", 404

        for user in users:
            if(name == user["name"]):
                return user, 200
        return "User not found", 404

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("dateOfBirth")
        args = parser.parse_args()

        date_of_birth = str_to_date(args["dateOfBirth"])
        now = str_to_date(datetime.datetime.now().strftime("%Y-%m-%d"))

        if date_of_birth >= now:
            return "Date not valid. Should be less than today", 404
        user = {
            "name": name,
            "dateOfBirth": args["dateOfBirth"]
        }

        users.append(user)
        return user, 201


try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "api_db")
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")

    api.add_resource(User, "/hello/<string:name>")
    app.run(debug=True)

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
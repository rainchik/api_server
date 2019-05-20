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


def date_converter(o):
    if isinstance(o, datetime.date):
        return o.strftime('%Y-%m-%d')

def output_message(output_message):
    output_json = {
        "message": output_message
    }
    return output_json


class User(Resource):
    def get(self, name):
        if not name.isalpha():
            return output_message("Name contains not only letters"), 404
        try:
            cursor.execute("select * from users where name = (%s)", [name])
            record = cursor.fetchone()
        except:
            return output_message("Something goes wrong with database"), 500
        if record is None:
            return output_message("User not found"), 404

        # print(record)
        # record_list = list(record)
        # colnames = [desc[0] for desc in cursor.description]
        #
        # user_json = {}
        # for i in range(len(colnames)):
        #     if isinstance(record_list[i], datetime.date):
        #         record_list[i] = record_list[i].strftime('%Y-%m-%d')
        #
        #     user_json[colnames[i]] = record_list[i]
        #
        # print((record[1]))
        # now = str_to_date(datetime.datetime.now().strftime("%Y-%m-%d"))
        # print((now))

        today_date = datetime.date.today()
        users_date = record[1]

        next_birthday = datetime.date(today_date.year, users_date.month, users_date.day)
        if (next_birthday - today_date).days < 0:
            next_birthday = datetime.date(today_date.year + 1, users_date.month, users_date.day)

        if (next_birthday - today_date).days > 0:
            message = ('Hello, ' + record[0] + '! Your birthday is in ' + str((next_birthday - today_date).days) + ' day(s)')
        else:
            message = ('Hello, ' + record[0] + '! Happy birthday!')

        return output_message(message), 200


    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("dateOfBirth")
        args = parser.parse_args()

        date_of_birth = str_to_date(args["dateOfBirth"])
        now = str_to_date(datetime.datetime.now().strftime("%Y-%m-%d"))

        if date_of_birth >= now:
            return output_message("Date not valid. Should be less than today"), 404


        try:
            cursor.execute("insert into users (name, dob) values ((%s), (%s))", [name, args["dateOfBirth"]])
            connection.commit()
        except:
            return output_message("Something goes wrong with database"), 500

        return '', 201


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
    app.run(debug=False)

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
    exit()

finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
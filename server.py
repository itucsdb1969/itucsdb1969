from flask import Flask, request
from flask import render_template
import psycopg2 as dbapi2
import requests

app = Flask(__name__)

result = []
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")
@app.route("/login", methods=['POST'])
def login_page():
    auth = []
    auth = request.get_data()
    print(auth)
    url = "dbname='postgres' user='postgres' host='localhost' password='123456'"
    with dbapi2.connect(url) as connection: 
        cursor = connection.cursor()
        statement = """select pass from "User" 
	            where name = (%(name)s)"""
        cursor.execute(statement, {'name': auth})
        result = cursor.fetchall()
        print(result[0])
        cursor.close()
    return render_template("login.html", messages = result)
@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/players")
def all_players_page():
    return render_template("players.html")    
@app.route("/teams")
def all_teams_page():
    url = "dbname='postgres' user='postgres' host='localhost' password='123456'"
    with dbapi2.connect(url) as connection: 
        cursor = connection.cursor()
        statement = """insert into public."User"(user_id, name, password, is_active, is_admin) values(5,'mehmet3' , 'mehmet' , true , false);"""
        cursor.execute(statement)
        cursor.close()
    return render_template("teams.html")
if __name__ == "__main__":
    app.run(debug=True)

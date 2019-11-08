from flask import Flask, request,flash
from flask import render_template
import psycopg2 as dbapi2
from forms import LoginForm, RegisterForm
app = Flask(__name__)

result = []
@app.route("/")
def index():
    return render_template("home.html",methods=["POST","GET"])
@app.route("/home")
def home():
    return render_template("home.html")
@app.route("/login", methods=['POST','GET'])
def login():
    result = []
    if request.method == "POST":
        username = request.form['username']
        password_form = request.form['password']
        url = "dbname='postgres' user='postgres' host='localhost' password='123456'"
        with dbapi2.connect(url) as connection: 
            cursor = connection.cursor()
            statement = """select password from users 
                    where name = %s"""
            cursor.execute(statement, [username])
            result = cursor.fetchall()
            print(result)
            for res in result:
                print(res[0])
            cursor.close()
            if(password_form == res[0]):
                return render_template("home.html")
            else:
                return render_template("login.html")            
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
        statement = """insert into users(name, password, is_active, is_admin) values('mehmet4' , 'mehmet' , true , false);"""
        cursor.execute(statement)
        cursor.close()
    return render_template("teams.html")
if __name__ == "__main__":
    app.run(debug=True) 

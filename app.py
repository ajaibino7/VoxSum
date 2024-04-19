from flaskext.mysql import MySQL
from flask import (Flask, request, session, g, redirect, url_for, abort, render_template, flash, Response)
import os
import re
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def check(email):
 
    if(re.fullmatch(regex, email)):
        return True
 
    else:
        return False
        
mysql = MySQL()
app = Flask(__name__,static_folder='static')
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password123'
app.config['MYSQL_DATABASE_DB'] = 'chat'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'd3Y5d5nJkU6CdwY'



@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        cursor = mysql.connect().cursor()
        cursor.execute("SELECT * from user_details where email='" + email + "' and password='" + password + "'")
        print("SELECT * from user_details where email='" + email + "' and password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            return "Username or Password is wrong"
        else:
            session['email'] = data[2]
            session['user_id'] = data[0]
            return redirect(url_for('home'))

        return render_template('index.html')

    else:
        return render_template('index.html')

@app.route('/addUser',methods = ["GET","POST"])
def addUser():
    if request.method == 'POST':
        User_name = request.form['user_name']
        email = request.form['email']
        Phone_number = request.form['phone_number']
        age = request.form['age']
        Password = request.form['password']
        address = request.form['address']
        res=check(email)
        if User_name=="" or email=="" or Phone_number=="" or age=="" or Password=="" or address=="":
            return "Please Fill all fileds"
        if not res:
            return "Please Enter a valid Email"

        qry = " INSERT INTO `user_details` ( user_name,email, Password, age, phone_number,address ) values "
        qry += "('"+User_name +"','"+email +"','"+Password +"','"+age +"','"+Phone_number +"','"+address +"')"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(qry)
        conn.commit()
        return redirect(url_for('index'))
    return render_template('addUser.html')

@app.route("/home",methods = ["GET","POST"])
def home():
    return render_template('home.html')

if __name__ == "__main__": 
    app.run(debug=True) 

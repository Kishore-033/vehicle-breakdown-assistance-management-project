from flask import Flask, flash, render_template, request, redirect, session
import mysql.connector
import pymysql


app = Flask(__name__,template_folder='templates')
app.secret_key = 'jw123'

def connect_to_database():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'kishore',
        'database': 'vehicle',
        'auth_plugin': 'mysql_native_password' 
    }
    return mysql.connector.connect(**db_config)


def register_user(username, password, phoneno, email):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        #hashed_password = hash_password(password)

        insert_query = "INSERT INTO register (username, password, phoneno, email) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (username, password, phoneno, email))

        connection.commit()
        cursor.close()
        connection.close()

        print(f"User '{username}' registered successfully!")
        return True
    except Exception as e:
        print(f"Error during registration: {e}")
        return False

def login_user(username, password):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        select_query = "SELECT password FROM register WHERE username = %s"
        cursor.execute(select_query, (username,))
        result = cursor.fetchone()

        if result :
            stored_password = result[0]
            if password == stored_password:
                print("Login successful!")
                session['username'] = username
                return True
            else:
                print("Incorrect password.")
        else:
            print("User not found.")

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error during login: {e}")
        return False
    
def reg_details(name, date, vehicleno,problem, amount, location):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        insert_query = "INSERT INTO vehicle_details (name, date, vehicleno, problem, amount, location) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (name, date, vehicleno, problem, amount, location))

        connection.commit()
        cursor.close()
        connection.close()

        print(f"Details stored successfully!")
        return True
    except Exception as e:
        print(f"Error during storing details: {e}")
        return False
        

    
def review_details(name, email, phoneno, subject, message):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        insert_query = "INSERT INTO review_details (name, email, phoneno, subject, message) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (name, email, phoneno, subject, message))

        connection.commit()
        cursor.close()
        connection.close()

        print(f"Thanks for the review ")
        return True
    except Exception as e:
        print(f"Error during storing details: {e}")
        return False
        
default_username = "admin"
default_password = "password"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phoneno = request.form['phoneno']
        email = request.form['email']
        
        # Register the user
        if register_user(username, password, phoneno, email):
            return redirect('/register')
        
    return render_template('register.html')


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Login the user
        if login_user(username, password):
            return redirect('/home')

    return render_template('register.html')
       
@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        provided_username = request.form.get('username')
        provided_password = request.form.get('password')
    
        if provided_username == default_username and provided_password == default_password:
           
            return redirect('/view')
        else:
           
            return render_template('admin_login.html', error="Invalid username or password")

    return render_template('admin_login.html', username=default_username, password=default_password)
    
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name=request.form['name']
        date=request.form['date']
        vehicleno = request.form['vehicleno']
        problem = request.form['cars']
        amount = request.form['amount']
        location = request.form['location']
        # latitude = request.form['latitude']
        # longitude = request.form['longitude']
        
        success = reg_details(name, date, vehicleno, problem, amount, location)

        if success:
            flash('Registered successfully!', 'success')
            return redirect('/home')
        else:
            flash('Error during registration. Please try again.', 'error')

    return render_template('home.html')

@app.route('/display_details',methods=["GET"])
def display_details():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        search_query = request.args.get('search_query', default='', type=str)
                
        select_query = (
            "SELECT * FROM vehicle_details "
            "WHERE name LIKE %s"
            "OR date LIKE %s"
            "OR vehicleno like %s"
            "OR location LIKE %s" 
            "OR problem LIKE %s"     
        )
      
        cursor.execute(select_query, (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
        
        
        vehicle_detail = cursor.fetchall()

        cursor.close()
        connection.close()
        
        print("vehicle Details:", vehicle_detail)
        
        return render_template('display_details.html', vehicle_detail=vehicle_detail)
    
    except pymysql.Error as e:
        
        print(f"Error in fetching details: {e}")

        return render_template('error.html',error_message="Error fetching billing details")
    
@app.route('/view')
def view():
  
    return render_template('view.html')

@app.route('/causes')
def causes():
    return render_template('causes.html')

@app.route('/contact',methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name=request.form['username']
        email=request.form['email']
        phoneno = request.form['phoneno']
        subject = request.form['subject']
        message = request.form['message']
        
        
        success = review_details(name, email, phoneno, subject, message)

        if success:
            flash('Thanks for the review', 'success')
            return redirect('/contact')
        else:
            flash('Error during registration. Please try again.', 'error')

    return render_template('contact.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/card_details')
def card_details():
    return render_template('card_details.html')

@app.route('/i_description')
def i_description():
    return render_template('i_description.html')

@app.route('/ii_description')
def ii_description():
    return render_template('ii_description.html')

@app.route('/iii_description')
def iii_description():
    return render_template('iii_description.html')


@app.route('/book_taxi')
def book_taxi():
    return render_template('no_1.html')

@app.route('/tow_manage')
def tow_manage():
    return render_template('tow_manage.html')

@app.route('/vehicle_breakdown')
def vehicle_breakdown():
    return render_template('vehicle_breakdown.html')

@app.route('/call_center')
def call_center():
    return render_template('call_center.html')

@app.route('/battery')
def battery():
    return render_template('battery.html')

@app.route('/low_fuel')
def blow_fuel():
    return render_template('low_fuel.html')

@app.route('/engine')
def engine():
    return render_template('engine.html')

@app.route('/ac_cool')
def ac_cool():
    return render_template('ac_cool.html')


if __name__ == '__main__':
    app.run(debug=True)

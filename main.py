from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import re


app = Flask(__name__)
 
 
app.secret_key = 'your secret key'
 
 


@app.route('/', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        query = "SELECT * FROM users WHERE user_id=? AND password=?"
        result = c.execute(query, (username, password)).fetchone()

        conn.close()

        if result:
            # The username and password are correct
            session['username'] = username
            return redirect('/Home')
        else:
            # The username and password are incorrect
            return "Incorrect username or password. Try again."

    return render_template("login.html")

@app.route('/Home')
def home():
    if 'username' in session:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute(f"SELECT ROLL_NO,NAME,GENDER,BUS_NO,BUS_ROUTE,SEMESTER,VALID_UPTO,PHONE_NO,SEAT_NO FROM busdetails WHERE ROLL_NO='{session['username']}'")
        student_info = c.fetchone()
        conn.close()
        return render_template('index.html', ROLL_NO=student_info[0], NAME=student_info[1],GENDER=student_info[2],BUS_NO=student_info[3],BUS_ROUTE=student_info[4],SEMESTER=student_info[5],VALID_UPTO=student_info[6],PHONE_NO=student_info[7],SEAT_NO=student_info[8])
    return redirect('/login')
@app.route('/Front_page')
def front():
    return redirect('/Home')

@app.route('/Seat Booking')
def booking():
    return render_template('buss.html')
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


def fetch_data_from_database(id):
    # Connect to the database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Execute a SELECT statement to fetch the data based on the id
    c.execute("SELECT * FROM busdetails WHERE id=?", (id,))
    data = c.fetchone()

    # Close the connection
    conn.close()

    return data

@app.route('/data/<int:id>')
def show_data(id):
    # Get the data from the database using the id
    data = fetch_data_from_database(id)
    return render_template('index.html', data=data)


@app.route('/Select_seat', methods=['POST'])
def update_seat():
    button_id = request.form['Seat_no']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE busdetails SET seat_no = ? WHERE Roll_No = ?", (button_id,{session['username']}))
    conn.commit()
    return "seat updated"
@app.route('/route_Booking', methods=['POST'])
def update_route():
    # Connect to the database
    Bus_Route=request.form['Bus_Route']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Update the bus_route column in the busdetails table
    c.execute("UPDATE busdetails SET bus_route = ? WHERE Roll_No = ?", (Bus_Route,{session['username']} ))
    conn.commit()

    # Close the database connection
    conn.close()

    return "Updated sucessfully"


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
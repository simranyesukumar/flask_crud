from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import pymysql

import mysql.connector
db=mysql.connector.connect(host="localhost",user="root",passwd="mysql",database="students")
if db.is_connected():
    print("connect")
c=db.cursor()
c.execute("show databases")
for i in c:
    print(i)
c.execute("show tables")
# for i in c:
#     print(i)
# c.execute("create table student_information(id int,name varchar(20),DOB DATE,amount_due int)")
#
# for i in c:
#     print(i)
# c.execute("desc student_information")

app = Flask(__name__)
app.secret_key = "Cairocoders-Ednalan"

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mysql'
app.config['MYSQL_DATABASE_DB'] = 'students'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def Index():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute('SELECT * FROM student_informations')
    data = cur.fetchall()

    cur.close()
    return render_template('index.html', student=data)


@app.route('/add_contact', methods=['POST'])
def add_student():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        id=request.form['id']
        name = request.form['name']
        DOB = request.form['DOB']
        amount_due = request.form['amount_due']
        cur.execute("INSERT INTO student_informations (id,name, DOB, amount_due) VALUES (%s,%s,%s,%s)", (id,name, DOB, amount_due))
        conn.commit()
        flash('Student Added successfully')
        return redirect(url_for('Index'))


@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_student(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute('SELECT * FROM student_informations WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', student=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_employee(id):
    if request.method == 'POST':
        name = request.form['name']
        DOB = request.form['DOB']
        amount_due = request.form['amount_due']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            UPDATE student_informations
            SET name = %s,
                DOB = %s,
                amount_due = %s
            WHERE id = %s
        """, (name, DOB, amount_due, id))
        flash('Student Updated Successfully')
        conn.commit()
        return redirect(url_for('Index'))


@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_student(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute('DELETE FROM student_inform WHERE id = {0}'.format(id))
    conn.commit()
    flash('Student Removed Successfully')
    return redirect(url_for('Index'))


# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)

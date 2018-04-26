from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = '2847328r9waur934rawzfw9045'
mysql = MySQLConnector(app,'emailsdb')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/success', methods=['POST'])
def insert():
    if len(request.form['email']) < 1:
        flash("Email cannot be empty!") 
        return redirect('/')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
        return redirect('/')
    else:
        flash("The email address you entered {} is a VALID email address! Thank you!" .format(request.form['email'])) # just pass a string to the flash function
        query_insert = "INSERT INTO emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
        data_insert = {
                 'email': request.form['email'],
               }
        mysql.query_db(query_insert, data_insert)
        query_select = 'SELECT id, email, DATE_FORMAT(created_at, "%c %d %y %r") AS created_at FROM emails'
        emails = mysql.query_db(query_select)
        print emails
        return render_template ('success.html', list_emails=emails)

@app.route('/delete', methods=['POST'])
def delete():
    if len(request.form['id']) < 1:
        flash("You should inform an ID from the list") 
    else:
        flash("The email address of ID {} was deleted!" .format(request.form['id']))
        query_delete = "DELETE FROM emails WHERE id = :id"                          
        data_delete = {
            'id': request.form['id'],
        }
        mysql.query_db(query_delete, data_delete)     
    return redirect('/') 

app.run(debug=True)

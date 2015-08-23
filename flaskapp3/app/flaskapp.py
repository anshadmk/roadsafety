import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from flask import render_template
import MySQLdb

db = MySQLdb.connect(host="localhost",user="root",passwd="root",db="speedb" )
cursor = db.cursor()

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def login():
	return render_template('login2.html')
@app.route('/speed_violation',methods=['GET', 'POST'])
def speed_violation():
	cursor.execute("SELECT * FROM notification")
	data=cursor.fetchall()
	return render_template('login3.html',items=data)
	#return render_template('login3.html',name=row[0],msg_count=row[1],max_speed=row[2])
	#return redirect(url_for('speed_violation',name=row[0],msg_count=row[1],max_speed=row[2]))

if __name__ == '__main__':
    app.run()
    db.close()	
    

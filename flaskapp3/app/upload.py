import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from flask import render_template
import MySQLdb

# Open database connection

db = MySQLdb.connect(host="localhost",user="speed",passwd="speed",db="speedb" )

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','py','zip'])
app = Flask(__name__)
UPLOAD_FOLDER = ""

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def login(name=None):
    return render_template('index.html',name=name)
@app.route('/verification', methods=['GET', 'POST'])
def verification():
	
	number = request.form['usermail']
	msg_count = request.form['password']
	msg_count=str(msg_count)
	number=str(number)
	# prepare a cursor object using cursor() method
	cursor = db.cursor()
	#sql="select * from user where number=%"
	
	try:
		 cursor.execute("SELECT * FROM user WHERE number = %s ", (number))
		 data=cursor.fetchall()
		 # Execute the SQL command
		 cursor.close()
	except:
		# Rollback in case there is any error
		db.rollback()
	# disconnect from server
	if data==():
		 	return render_template('index.html',name="Please SignUp")

	for row in data:
		passw=row[1]
	if passw==msg_count:
		UPLOAD_FOLDER = "/home/apple/"+number
		app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
		return redirect(url_for('uploading'))
	else:
		return render_template('index.html',name="Invalid msg_count")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	number = request.form['usermail']
	msg_count = request.form['msg_count']
	msg_count1 = request.form['msg_count1']
	msg_count=str(msg_count)
	number=str(number)
	if msg_count!=msg_count1:
		return render_template('index.html',name1="msg_counts do not match")
	# prepare a cursor object using cursor() method
	cursor = db.cursor()
	os.makedirs("/home/apple/"+number)
	#sql="select * from user where number=%"
	sql="INSERT INTO user(name,msg_count) VALUES ('%s','%s' )" % (number,msg_count)
	try:
		 
		 cursor.execute(sql)
		 # Execute the SQL command
		 cursor.close()
		 db.commit()
	except:
		# Rollback in case there is any error
		db.rollback()	
	# disconnect from server
	return redirect(url_for('login'))
			
@app.route('/uploaded', methods=['GET', 'POST'])
def uploading():
	if request.method == 'POST':
        	file = request.files['file']
        	if file and allowed_file(file.filename):
            		filename = secure_filename(file.filename)
            		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            		return redirect(url_for('uploading'))

    	return render_template('upload.html')
	

if __name__ == '__main__':
    app.run()
    db.close()	
    

from Reminderapp import app,db,mail
from flask import render_template,flash,redirect,url_for,session
from Reminderapp.forms import AdminForm,EmployeeForm,EmployeeDocumentForm
from Reminderapp.models import User,Employee,EmployeeDocument,Role
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

from werkzeug.utils import secure_filename
import os
import schedule
from datetime import datetime,timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from zoneinfo import ZoneInfo


@app.route('/')
@app.route('/home')
def index():
	test=User.query.all()	
	return render_template('landing.html',user=test)
	
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	form=AdminForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user and user.hash_password==form.password.data:
			login_user(user, remember=False)
			#flash('loggedIn successful!','success')
			return redirect(url_for('dashboard'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html' ,form=form)
	
@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You logged out!', 'info')
	return redirect(url_for('login'))	
				
								
@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')	

@app.route('/employee-list')
def employee_list():
	employees=User.query.filter_by(role_id=3).all()
	return render_template('employee-list.html',employees=employees)
	
@app.route('/add-employee', methods=['GET', 'POST'])
def add_employee():
	form=EmployeeForm()
	if form.validate_on_submit():
		user=User(
		full_name=form.full_name.data,
		email=form.email.data,phone_no=form.phone_number.data,
		hash_password='password',
	role_id=3)
		db.session.add(user)
		db.session.flush()
		employee=Employee(
	dob=form.dob.data,
	department=form.department.data,
	position=form.position.data, user_id=user.id)

		db.session.add(employee)	
		db.session.commit()
		flash('new employee added','success')
		return redirect(url_for('employee_list'))
	return render_template('add-employee.html', form=form)
@app.route('/employee-profile/<id>')
def employee_profile(id):
	employee=User.query.get(id)
	return render_template('employee-profile.html',employee=employee)

	
@app.route('/upload-document', methods=['POST', 'GET'])
def upload_document():
    form = EmployeeDocumentForm()
    if form.validate_on_submit():
        document = form.document.data
        if document and allowed_file(document.filename):
            filename = secure_filename(document.filename)
            try:
                document.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('Document uploaded successfully', 'info')
            except Exception as e:
                flash('Error uploading document: ' + str(e), 'error')
            return redirect(url_for('upload_document')) 
    return render_template('upload-document.html', form=form)

	

@app.route('/report')
def report():
	documents=EmployeeDocument.query.all()
	return render_template('report.html')
	
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404
	
	

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500
	


scheduler = BackgroundScheduler(timezone=ZoneInfo("Africa/Johannesburg"))

def update_status(expiration_date):
    if expiration_date < datetime.now():
        status = "Expired"
    else:
        status = "Valid"
    return status


def doc_status():
        with app.app_context():
        	docs=EmployeeDocument.query.all()
        	for doc in docs:
        		doc.status=update_status(doc.expiring_date)
        	db.session.commit()
        	
def send_reset_email(total,expired,valid,in30days):
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=['phungula82@outlook.com']) 
    msg.subject="This report highlights the current status of documents"
    msg.body = f'''Dear Administrator,


This report highlights the current status of documents:


- Total Documents: {len(total)}
- Expired: {expired.count()}
- Valid:{valid.count()}
- Expiring in 30 days:  {in30days.count()} documents are  expiring in the next 30 days


We recommend reviewing and updating expired documents and taking action on documents expiring soon.


Best regards,
employee management
'''
    mail.send(msg)

def send_report():
	with app.app_context():
		total=EmployeeDocument.query.all()
		expired=EmployeeDocument.query.filter_by(status='Expired')
		valid=EmployeeDocument.query.filter_by(status='Valid')
		
		today=datetime.today()
		thirthydays=today+timedelta(weeks=4, days=2)
		in30days=EmployeeDocument.query.filter_by(expiring_date=thirthydays.date())
		send_reset_email(total,expired,valid,in30days)
		
def report():
	print('this is a reminder app')
	
		

sched =BackgroundScheduler(daemon=True)
sched.add_job(doc_status,'interval',seconds=5)
sched.add_job(send_report,'interval',hours=2)
#sched.add_job(report,'interval',seconds=2)
sched.start()

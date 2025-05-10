from Reminderapp import db,app,login_manager
from wtforms import ValidationError
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(id):
	return Admin.query.get(int(id))
	

class Admin(db.Model,UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	full_name=db.Column(db.String(100) ,nullable=False)
	email=db.Column(db.String(60),nullable=False,unique=True)
	phone_no=db.Column(db.String(15),nullable=False,unique=True)
	hash_password=db .Column(db.String(100),nullable=False)

class Employee(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	employee_fname=db.Column(db.String(100),nullable=False)
	dob=db.Column(db.DateTime , default=datetime.utcnow)
	employee_email=db.Column(db.String(50),nullable=False ,unique=True)
	employee_no=db.Column(db.String(13),nullable=False,unique=True)
	department=db.Column(db.String(25), nullable=True)
	position=db.Column(db.String(25))
	documents = db.relationship('EmployeeDocument', backref='employee')
	

class EmployeeDocument(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	document=db.Column(db.String(15),nullable=True)
	document_type=db.Column(db.String(15),nullable=True)
	issue_date=db.Column(db.DateTime())
	expiring_date=db.Column(db.DateTime())
	upload_date=db.Column(db.DateTime() ,nullable=True,default=datetime.utcnow)
	employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)



	
	
with app.app_context():
	db.create_all()
	admin=Admin(full_name="nkosingiphile",email="phungula@gmail.com",phone_no='0000078000',hash_password='password')
	admin2=Admin(full_name="nkosingiphile",email="phungula2@gmail.com",phone_no='0000070000',hash_password='password')
	
	
	employees = [
    Employee(
        employee_fname="Nkosingiphile",
        employee_email="nkosingiphile@example.com",
        employee_no="1234567890123",
        department="IT",
        position="Software Developer"
    ),
    Employee(
        employee_fname="John",
        employee_email="john.doe@example.com",
        employee_no="9876543210987",
        department="Sales",
        position="Sales Manager"
    ),
    Employee(
        employee_fname="Jane",
        employee_email="jane.smith@example.com",
        employee_no="1111111111111",
        department="Marketing",
        position="Marketing Specialist"
    )
]
	
	

	try:
		db.session.add(admin)
		db.session.add(admin)
		db.session.add_all(employees)
		db.session.commit()
	except:
		db.session.rollback()
	
	
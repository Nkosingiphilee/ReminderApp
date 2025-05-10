from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,TelField,DateField
from wtforms.validators import DataRequired,Email,Length



class AdminForm(FlaskForm):
	email=StringField('your email address',validators=[DataRequired(),Email()])
	password=PasswordField('your password',validators=[DataRequired()])
	button=SubmitField('Login')
	
	
class EmployeeForm(FlaskForm):
	full_name=StringField('employee full name',validators=[DataRequired(),Length(min=2, max=50)])
	dob=DateField('date of birth',validators=[DataRequired()])
	email=StringField('employee email',validators=[DataRequired(),Email()])
	phone_number=TelField('cellphone number',validators=[DataRequired(),Length(min=10, max=20)])
	department=StringField("Department",validators=[DataRequired(),Length(min=2, max=20)])
	position=StringField("position",validators=[DataRequired(),Length(min=2, max=20)])
	submit=SubmitField('add employee')
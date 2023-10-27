from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField('Log In')

class SignUpForm(FlaskForm):
    first_name = StringField(label='First Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired()])
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    confirm_password = PasswordField("Confirm your Password", [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
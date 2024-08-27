
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from flask_wtf.file import FileField,FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from ..models import User

# Sign Up Form
class SignupForm(FlaskForm):

    fname    = StringField("First Name", validators=[DataRequired(), Length(min=3, max=25)])
    lname    = StringField("Last Name", validators=[DataRequired(), Length(min=3, max=25)])
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=25)])
    email    = StringField("Email", validators=[DataRequired(), Length(max=50), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=50)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=6, max=50), EqualTo("password")])
    signup   = SubmitField("Sign Up")


    # Check username is not exist
    def validate_username(self, username):
        username = User.query.filter_by(username=username.data).first()
        if username:
            raise ValidationError("Username already exisit please chooce a diffrent one")
        
    # Check email is not exist
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Email already exisit please chooce a diffrent one")
        
# Login Form
class LoginForm(FlaskForm):

    email    = StringField("Email", validators=[DataRequired(), Length(max=50), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=50)])    
    remember = BooleanField("Remember me")
    login   = SubmitField("Log In")        


# Profile Form
class ProfileForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=25)])
    email    = StringField("Email", validators=[DataRequired(), Length(max=50), Email()])
    bio      = TextAreaField("Bio")
    image    = FileField("Update Profile Image", validators=[FileAllowed(["png", "jpg"])])
    update   = SubmitField("Update")

    
    # Check username is not exist
    def validate_username(self, username):
        if username.data != current_user.username:
            username = User.query.filter_by(username=username.data).first()
            if username:
                raise ValidationError("Username already exisit please chooce a diffrent one")
            
    # Check email is not exist
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("Email already exisit please chooce a diffrent one")

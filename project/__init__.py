from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_admin import Admin


app = Flask(__name__)

app.config['SECRET_KEY'] = 'd37999ff153417b38e63257cc8ac2bee'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
ckeditor = CKEditor(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
admin = Admin(app)


# Import Blueprint
from project.admins.routes import adminbp
from project.main.routes import main
from project.users.routes import users
from project.lessons.routes import lessonsbp
from project.errors.routes import errors

app.register_blueprint(adminbp)
app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(lessonsbp)
app.register_blueprint(errors)
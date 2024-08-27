
from flask import Blueprint
from project import admin, db
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView 
from project.models import User, Lessons, Courses
from flask_login import current_user

# from project import admin

adminbp = Blueprint("adminbp", __name__)


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    


admin.add_views(MyModelView(User, db.session))
admin.add_views(MyModelView(Lessons, db.session))
admin.add_views(MyModelView(Courses, db.session))









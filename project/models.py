from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(int(user_id))


# Create Database 

# User Tabel
class User(db.Model, UserMixin):
    __tabelname__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(125), nullable=False, unique=True)
    bio   = db.Column(db.Text())
    user_img = db.Column(db.String(125), nullable=False, default='default.png')
    create_at = db.Column(db.DateTime(), default=datetime.utcnow)
    password = db.Column(db.String())
    lessons = db.relationship("Lessons", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.fname}' '{self.lname}' '{self.username}' '{self.email}' '{self.user_img}')"
    

class Lessons(db.Model):
    __tabelname__ = 'lesssons'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), nullable=False)
    slug = db.Column(db.String(25), nullable=False)
    content = db.Column(db.Text(), nullable=False, unique=True)
    lessons_img = db.Column(db.String(125), nullable=False, default='lesson.png')
    create_at = db.Column(db.DateTime(), default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))

    def __repr__(self):
        return f"Lessons('{self.title}' '{self.content}' '{self.lessons_img}')"
    

class Courses(db.Model):
    __tabelname__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    course_img = db.Column(db.String(125), nullable=False, default='coures.png')
    create_at = db.Column(db.DateTime(), default=datetime.utcnow)
    lessons = db.relationship("Lessons", backref="course", lazy=True)

    def __repr__(self):
        return f"Lessons('{self.title}' '{self.content}' '{self.course_img}')"




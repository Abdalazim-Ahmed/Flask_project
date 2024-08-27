
from ..models import  Lessons, Courses
from flask import render_template, request
from . import main


# home page function
@main.route("/")
@main.route("/home")
def home():

    page_number = request.args.get('page', default=1, type=int)
    lessons = Lessons.query.paginate(page=page_number, per_page=3)
    courses = Courses.query.paginate(page=page_number, per_page=3)
    return render_template("pages/home.html",lessone=lessons, courses=courses, title='Home')

# about page function
@main.route("/about")
def about():
    return render_template("pages/about.html", title='About')

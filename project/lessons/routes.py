
from project import db
from flask_modals import render_template_modal
from ..models import Lessons, Courses
from flask import render_template, redirect, url_for, flash, request, session, abort
from flask_login import current_user, login_required
from .forms import NewLessonForm, UpdateLessonForm
from project.courses.forms import CourseForm
from ..helper_func import save_image
from flask import Blueprint

lessonsbp = Blueprint("lessonsbp", __name__)



# create new lesson page function
@lessonsbp.route("/dashboard/new_lesson", methods=["GET", "POST"])
@login_required
def new_lesson():

    lesson_form  = NewLessonForm()
    course_form  = CourseForm()

    form = ""

    if "slug" in request.form:
        form = "lesson_form"
    elif "description" in request.form:
        form = "course_form"

    if form == "lesson_form" and lesson_form.validate_on_submit():
        if lesson_form.image.data:
            image_file = save_image(lesson_form.image.data, "static/lesson_pics/")
        course = lesson_form.course.data
        lesson = Lessons(
            title = lesson_form.title.data,
            slug  = lesson_form.slug.data,
            content = lesson_form.content.data,
            author = current_user,
            course = course,
            lessons_img = image_file
        )
        db.session.add(lesson)
        db.session.commit()
        flash("Your Lession Has been Created", "success")
        return redirect(url_for("home"))
        
    elif form == "course_from" and course_form.validate_on_submit():
        course = Courses(
            title = course_form.title.data,
            content = course_form.description.data 
        ) 
        db.session.add(course)
        db.session.commit()
        session["flag"] = True
        flash("Your course has been Created", "success")
        return redirect(url_for("users.dashboard"))

    
    return render_template_modal("dashboard/new_lesson.html",
                            course_form=course_form,
                            lesson_form=lesson_form,
                            title="New_Lesson")



# view a lesson page function
@lessonsbp.route("/<string:course_title>/<string:lesson_slug>")
def lesson(course_title, lesson_slug):
    lesson = Lessons.query.filter_by(slug=lesson_slug).first()
    lesson_id = lesson.id if lesson else None
    lesson = Lessons.query.get_or_404(lesson_id)
 
    return render_template("pages/lesson.html", lesson=lesson, title=lesson.title)

# views all user lessons
@lessonsbp.route("/dashboard/lessons", methods=['GET', 'POST'])
@login_required
def user_lessons():
    return render_template("dashboard/user_lessons.html", title="Your Lessons")


# This Function view update lesson 
@lessonsbp.route("/<string:course_title>/<string:lesson_slug>/update", methods=['GET', 'POST'])
@login_required
def update_lesson(course_title, lesson_slug):

    lesson = Lessons.query.filter_by(slug=lesson_slug).first()
    lesson_id = lesson.id 
    lesson = Lessons.query.get_or_404(lesson_id)

    # check user if current user is authentication
    ''' write check code here '''
    if lesson.author != current_user:
        abort(403)

    form = UpdateLessonForm()

    if form.validate_on_submit():    
        lesson.course = form.course.data
        lesson.title = form.title.data
        lesson.slug = form.slug.data
        lesson.content = form.content.data
        if form.image.data:
            file_pectuer = save_image(form.image.data, "static/lesson_pics")
            lesson.image = file_pectuer

        db.session.commit()
        flash("Your lesson was Updated", "success")
        return redirect(url_for("lessonspb.user_lessons"))

    elif request.method == "GET":
        form.course.data = lesson.course.title
        form.title.data = lesson.title
        form.slug.data = lesson.slug
        form.content.data = lesson.content

    return render_template("dashboard/update_lesson.html", form=form, title="Update Lesson")


# Delete lesson Function
@lessonsbp.route("/lesson/<int:lesson_id>/delete", methods=['POST'])
def delete_lesson(lesson_id):
    lesson_id = Lessons.query.get_or_404(lesson_id)
    if lesson_id.author != current_user:
        abort(403)
    db.session.delete(lesson_id)
    db.session.commit()
    flash("Your lesson has been deleted", "success")
    return redirect(url_for('lessonsbp.user_lessons'))
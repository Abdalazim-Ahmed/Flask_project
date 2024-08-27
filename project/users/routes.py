
from . import users
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from .forms import SignupForm, LoginForm, ProfileForm
from project import bcrypt, db
from ..models import User
from ..helper_func import save_image


# signup page function
@users.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        password_hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(
            fname=form.fname.data,
            lname=form.lname.data,
            username=form.username.data,
            email=form.email.data,
            password=password_hashed,
            )         
        db.session.add(user)
        db.session.commit()

        flash(f"Welcom to our website {form.username.data}", "success")
        return redirect(url_for("login"))

    return render_template("register/signup.html", form=form, title='Signup')

# login page function
@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        redirect(url_for("main.home"))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Welcome You have been logged In ", "success")
            next_page = request.args.get("next")
            return redirect(next_page if next_page else url_for('main.home'))

        else:
            flash("wrong email or password", "danger")

    return render_template("register/login.html", form=form, title='Login')

# logout page function
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


# dashboard page function
@users.route("/dashboard/", methods=["GET"])
@login_required
def dashboard():

    """  profile_form = ProfileForm()

    if profile_form.validate_on_submit():
        if profile_form.image.data:
            pictuer_path = save_image(profile_form.image.data)
            current_user.user_img = pictuer_path
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        current_user.bio = profile_form.bio.data
        db.session.commit()

    elif request.method == "GET":
        profile_form.username.data = current_user.username
        profile_form.email.data = current_user.email
        profile_form.bio.data = current_user.bio
    img_file = url_for("static", filename=f"pics/{current_user.user_img}") 
    
    """

    return render_template("dashboard.html", title="Dashboard")


# profile page function
@users.route("/dashboard/profile", methods=["GET", "POST"])
@login_required
def profile():
    profile_form = ProfileForm()

    if profile_form.validate_on_submit():
        if profile_form.image.data:
            pictuer_path = save_image(profile_form.image.data, "static/user_pics", out_size=(150, 150))
            current_user.user_img = pictuer_path
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        current_user.bio = profile_form.bio.data
        db.session.commit()

    elif request.method == "GET":
        profile_form.username.data = current_user.username
        profile_form.email.data = current_user.email
        profile_form.bio.data = current_user.bio
    img_file = url_for("static", filename=f"user_pics/{current_user.user_img}")  

    return render_template("dashboard/profile.html", profile_form=profile_form, img_file=img_file, title="Profile")

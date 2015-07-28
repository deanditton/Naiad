from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required
from Naiad.extensions import cache
from Naiad.forms import LoginForm, SignupForm
from Naiad.models import User
from Naiad.models import db
import json

main = Blueprint('main', __name__)


@main.route('/')
@cache.cached(timeout=1000)
def home():
    return render_template('index.html')


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    check = False
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user)

        flash("Logged in successfully.", "success")
        return redirect(request.args.get("next") or url_for(".home"))

    return render_template("login.html", form=form)


@main.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        form = SignupForm(request.form)
        user = User(form.username, form.email, form.password)
        user_exist = User.query.filter_by(username=form.username.data).first()
        email_exist = User.query.filter_by(email=form.email.data).first()
        if user_exist:
            form.username.errors.append('Username already taken')
        if email_exist:
            form.email.errors.append('Email already use')
        if user_exist or email_exist:
            return render_template('signup.html', form=form, page_title='Signup to Bio Application')
        else:
            db.session.add(user)
            db.session.commit()
            return render_template('signup-success.html', user=user, page_title='Sign Up Success!')

    return render_template('signup.html', form=SignupForm(), page_title='Signup to Bio Application')


@main.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")

    return redirect(url_for(".home"))


@main.route("/restricted")
@login_required
def restricted():
    return "You can only see this if you are logged in!", 200


@main.route("/weather_data", methods="POST")
def weather_data():
    city = request.data
    with open('./weatherData/collection.json', 'r') as data_file:
        data = json.loads(data_file)
    useful_data = {"max_0": data[city]['max_0'], "max_1": data[city]['max_1'], "max_2": data[city]['max_2'],"max_3": data[city]['max_3'],
                   "max_4": data[city]['max_4'], "max_5": data[city]['max_5'], "max_6": data[city]['max_6'], "max_7": data[city]['max_7'],

                   "min_0": data[city]['min_0'], "min_0": data[city]['min_0'],"min_0": data[city]['min_0'],"min_0": data[city]['min_0'],
                   "min_0": data[city]['min_0'],"min_0": data[city]['min_0'],"min_0": data[city]['min_0']}



    send_value = data[city]


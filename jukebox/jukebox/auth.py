from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = bool(request.form.get("remember"))

    user = User.query.filter_by(email=email).first()

    if not user:
        flash(f"No user account was found for email '{email}'")
        return redirect(url_for("auth.login"))
    elif not check_password_hash(user.password, password):
        flash("Please check your password and try again")
        return redirect(url_for("auth.login"))
    else:
        login_user(user, remember=remember)
        return redirect(url_for("main.profile"))


@auth.route("/create_account")
@login_required
def create_account():
    return render_template("create_account.html")


@auth.route("/create_account", methods=["POST"])
@login_required
def create_account_post():
    if current_user.can_create_users:
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            flash(f"A user with email address '{email}' already exists.")
            return redirect(url_for("auth.signup"))

        new_user = User(email=email, name=name, password=generate_password_hash(password, method="sha256"))
        db.session.add(new_user)
        db.session.commit()

    flash(f"Success: User '{email}' created successfully.")
    return redirect(url_for("auth.create_account"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


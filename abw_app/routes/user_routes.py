# abw_app/routes/user_routes.py

from flask import Blueprint, jsonify, request, render_template, flash, redirect

from abw_app.models import User, db
user_routes = Blueprint("user_routes", __name__)


@user_routes.route("/users.json")
def list_users():
    """
    Return results in machine-readable form
    """
    users = [
        {"id": 1, "username": "@aaron", "email": "aaron@gmail.com"},
        {"id": 2, "username": "@mercedes", "email": "mercedes@yahoo.com"},
        {"id": 3, "username": "@omar", "email": "omar@att.net"},
    ]
    return jsonify(users)


@user_routes.route("/users")
def list_users_for_humans():
    """
    Return results in HTML (web page) style
    """
    t_users = [
        {"id": 1, "screen_name": "@_ekselan", "name": "Aaron", "location": "GA", "followers_count": 190},
        {"id": 2, "screen_name": "@mjp30004", "name": "Mercedes", "location": "GA", "followers_count": 500},
        {"id": 3, "screen_name": "@maybacho", "name": "Omar", "location": "CT", "followers_count": 350},
    ]

    # SELECT * FROM users
    user_records = User.query.all()
    print(user_records)

    return render_template(
        "users.html", message="Here's some users", users=user_records)


@user_routes.route("/users/new")
def new_user():
    return render_template("new_users.html")


@user_routes.route("/users/create", methods=["POST"])
def create_user():
    print("FORM DATA:", dict(request.form))

    # return jsonify({
    #     "message": "USER CREATED OK",
    #     "user": dict(request.form)
    # })

    # INSERT INTO users ... (store data in the database)
    new_user = User(
        screen_name=request.form["screen_name"],
        name=request.form["name"],
        location=request.form["location"],
        followers_count=request.form["followers_count"])
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

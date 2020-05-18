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
        {"id": 1, "username": "@aaron", "email" : "aaron@gmail.com"},
        {"id": 2, "username": "@mercedes", "email" : "mercedes@yahoo.com"},
        {"id": 3, "username": "@omar", "email" : "omar@att.net"},
    ]
    return jsonify(users)

# @user_routes.route("/users")
# def list_users_for_humans():
#     """
#     Return results in HTML (web page) style
#     """
#     # users = [
#     #     {"id": 1, "username": "@rvr3_ekselan", "email" : "acewatguy@gmail.com"},
#     #     {"id": 2, "username": "@mjp30004", "email" : "macparis@yahoo.com"},
#     #     {"id": 3, "username": "@maybach_o", "email" : "spartan_dawgs@att.net"},
#     # ]

#     # SELECT * FROM books
#     book_records = Book.query.all()
#     print(book_records)

#     return render_template(
#         "books.html", message="Here's some books", books=book_records)

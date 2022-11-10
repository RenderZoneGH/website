from app import flask, request, render_template, redirect, flash, session
from app.util.animation import a
from app.util.db import read
import bcrypt

def init(route):
    @flask.route(route, methods=['GET', 'POST'])
    def admin_login():
        if request.method == "GET":
            return render_template("admin/login.html.j2", session=session)
        else:
            password = request.form.get("password")
            username = request.form.get("username")

            dbc = read()
            if username in dbc['admins']:
                # Check password using bcrypt
                if bcrypt.checkpw(password.encode('utf-8'), dbc['admins'][username]['password'].encode('utf-8')):
                    session["admin"] = True
                    session["username"] = username
                    flash("Logged in!", "success")
                    return redirect("/admin")
                else:
                    flash("Invalid password!", "error")
                    return redirect("/admin/login")
            else:
                flash("Invalid username!", "error")
                return redirect("/admin/login")
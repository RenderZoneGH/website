from app import flask, request, render_template, redirect, flash, session
from app.util.animation import a
from app.util.db import read
from app.util.decorators.admin import requiresAdmin

def init(route):
    @flask.route("/admin/jobs/all")
    @requiresAdmin
    def admin_jobs_all():
        dbc = read()

        alljobs = dbc["analytics"]["renders"]
        alljobs.reverse()

        return render_template("admin/jobs_all.html.j2", session=session, db=dbc, jobs=alljobs)
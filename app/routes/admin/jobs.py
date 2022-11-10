from app import flask, request, render_template, redirect, flash, session, jobs
from app.util.animation import a
from app.util.db import read
from app.util.decorators.admin import requiresAdmin

def init(route):
    @flask.route("/admin/jobs")
    @requiresAdmin
    def admin_jobs():
        dbc = read()
        recentjobs = jobs

        return render_template("admin/jobs.html.j2", session=session, db=dbc, jobs=recentjobs)
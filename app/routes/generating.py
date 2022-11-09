from app import flask, request, render_template, redirect, url_for, flash, session, jobs
from app.util.animation import a
from app.util.db import read
import uuid as u
import os

def init(route):
    @flask.route(route)
    def generating(uuid):
        return render_template('generating.html', session=session, animation=a(request))

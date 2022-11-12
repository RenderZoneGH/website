from app import flask, request, render_template, redirect, flash, session, jobs
from app.util.animation import a
from app.util.db import read
import uuid as u
import json as j
import os

def init(route):
    @flask.route('/api/v1/'+route, methods=['GET'])
    def job(uuid):
        if uuid in jobs:
            job = jobs[uuid]
            job.get("url") == None
            return j.dumps(job)
        else:
            return j.dumps({
                "status": "error",
                "error": "Unknown job!",
                "display": "Unknown job!"
            })
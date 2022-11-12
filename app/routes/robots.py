from app import flask, request, render_template, redirect, flash, session
from app.util.animation import a
from app.util.db import read
 
def init(route):
    @flask.route(route)
    def robots():
        robots = """
# This is the robots.txt file for RenderZone. We are working on an API so if you wan't to access our library of templates, you can do so by using our API.

user-agent: *
disallow: /api/
disallow: /admin/
disallow: /static/
disallow: /checkout/
disallow: /generating/
disallow: /coupon/
"""
        return robots

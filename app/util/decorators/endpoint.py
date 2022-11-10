from app import request, render_template, session
from app.util.animation import a
from functools import wraps

def endpoint(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        return func(*args, **kwargs)
    return wrapper
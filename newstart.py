from app import flask
from app.util.env import env

if __name__ == "__main__":
    flask.run(port=env("PORT", 5000), debug=True if env("ENVIRONMENT", "prod") == "dev" else False)
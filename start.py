from app import flask
from app.util.env import env

if __name__ == "__main__":
    print("(Pterotrigger) Started.")
    flask.run(port=env("PORT", 5000), debug=True if env("ENVIRONMENT", "prod") == "dev" else False, host="0.0.0.0")
    
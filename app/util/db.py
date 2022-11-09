from app.util.env import env
import json as j

def read():
    with open(env("DB_FILE", "datab.json"), 'r') as f:
        return j.load(f)


def write(data):
    with open(env("DB_FILE", "datab.json"), 'w') as f:
        j.dump(data, f)

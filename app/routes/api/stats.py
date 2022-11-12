from app import flask, request
from app.util.db import read
import json as j
import humanize

def init(route):
    @flask.route("/api/v1/" + route, methods=["GET"])
    def stats():
        dbc = read()
        if "Authorization" not in request.headers:
            return "Unauthorized", 401
        apikey = request.headers.get('Authorization').split(" ")[1]
        if apikey not in dbc['apikeys']:
            return j.dumps({"error": "Invalid API key."}), 401
        if "read" not in dbc['apikeys'][apikey]['access']:
            return j.dumps({"error": "Access denied."}), 403
        
        total = len(dbc['analytics']['renders'])
        # turn total into a string (like 1000 -> 1k) using the library "humanize"
        total = humanize.intword(total)
        words = total.split(" ")
        if len(words) == 1:
            total = words[0]
        else:
            word = words[1]
            shorts = {
                "thousand": "k",
                "million": "m",
                "billion": "b",
                "trillion": "t",
                "quadrillion": "q",
            }
            total = total.replace(" "+word, shorts[word])



        stats = {
            "renders": {
                "total": {
                    "exact": len(dbc['analytics']['renders']),
                    "humanized": total
                }
            }
        }

        return j.dumps(stats)
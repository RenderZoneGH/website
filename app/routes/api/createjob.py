from app import flask, request, render_template, redirect, flash, session, jobs, sio
from app.util.db import read
import json as j
 
def init(route):
    @flask.route('/api/v1/'+route, methods=['POST'])
    def createjob():
        json = request.json
        jobs[json["id"]] = {
            "done": False,
            "render": {
                "progress": 0,
            },
            "display": "Preparing...",
            "templateid": "Custom",
            "uuid": json["id"],
            "fields": json["fields"],
        }
        sio.emit(
            "job", 
            {
                "uuid": json["id"],
                "product": {
                    "name": "Custom",
                    "id": "Custom",
                    "price": 0,
                    "ae": json["ae"],
                },
                "key": json["key"],
                "hide": json["hide"],
            }
        )
        return j.dumps({"success": True, "uuid": json["id"]})
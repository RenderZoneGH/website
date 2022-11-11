import requests
from app import jobs, sio
import time
from app.util.db import read, write
from app.util.env import env
class colours:
    SUCCESS = '\033[92m'
    INFO = '\033[94m'
    FAIL = '\033[91m'
    DEFAULT = '\033[0m'

@sio.event
def json(data):
    print(colours.INFO, 'Render API sent JSON: '+str(data), colours.DEFAULT)
    # if data contains "done" or "error" then send it to the client
    if "done" in data:
        r = requests.get(data['url'], allow_redirects=True)
        open('app/static/img/exported/'+data['uuid']+'.gif', 'wb').write(r.content)

        jobs[data['uuid']]['done'] = True
        jobs[data['uuid']]['url'] = data['url']
        jobs[data['uuid']]['display'] = data['display']
        print(colours.SUCCESS, 'Job ' +
              data['uuid']+' is done!', colours.DEFAULT)

        if jobs[data['uuid']].get("hide", False):
            dbc = read()
            dbc['analytics']['renders'].append({
                "uuid": data['uuid'],
                "templateid": jobs[data['uuid']]['templateid'],
                "time": time.time()
            })

            if "payment" in jobs[data['uuid']]:
                dbc['analytics']['renders'][-1]["payment"] = jobs[data['uuid']]['payment']
                dbc['analytics']['renders'][-1]["payment"]["paypal"] = jobs[data['uuid']]['paypal']
            
            write(dbc)
    
    elif "error" in data:
        jobs[data['uuid']]['done'] = True
        jobs[data['uuid']]['error'] = data['error']
        jobs[data['uuid']]['display'] = data['display']
        print(colours.FAIL, 'Job '+data['uuid']+' failed!', colours.DEFAULT)
    elif "update" in data:
        jobs[data['uuid']]['display'] = data['display']
        print(colours.INFO, 'Job '+data['uuid']+' updated!', colours.DEFAULT)
 

@sio.event
def rnode(data):
    print(colours.INFO, 'Render Node update: '+str(data), colours.DEFAULT)
    if "uuid" in data:
        uuid = data['uuid']
        jobs[uuid]["display"] = "In queue" if data["details"]["state"] == "queued" else "Getting started..." if data["details"]["state"] == "started" else "Rendering..."
        jobs[uuid]["render"]["progress"] = data["details"]['renderProgress']

@sio.event
def disconnect():
    print(colours.FAIL, 'Disconnected from Render API', colours.DEFAULT)
    # try to reconnect every 5 seconds
    rfail = True
    while True:
        try:
            sio.connect(env('RENDER_API_URL', 'http://localhost:3000'))
            rfail = False
            break
        except:
            time.sleep(5)

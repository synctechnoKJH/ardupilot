import requests, json
HOST = "http://203.253.128.177:7579"
CBS = "/Mobius"
ORIGIN = "SITL_nCube"
http = requests

def createCNT(uri, name):
    con = {
        "m2m:cnt": {
            "rn": name
        }
    }
    headers = {
        "Accept": "application/json",
        "X-M2M-RI": "12345",
        "X-M2M-Origin": ORIGIN,
        "Content-Type": "application/vnd.onem2m-res+json; ty=3"
    }
    res = http.post(uri, data=json.dumps(con), headers=headers)
    return res.json()

def createCIN(uri, content):
    con = {
        "m2m:cin": {
            "con": content
        }
    }
    headers = {
        "Accept": "application/json",
        "X-M2M-RI": "12345",
        "X-M2M-Origin": ORIGIN,
        "Content-Type": "application/vnd.onem2m-res+json; ty=4"
    }
    res = http.post(uri, data=json.dumps(con), headers=headers)
    return res.json()

def getResource(uri):
    headers = {
        'X-M2M-RI': "12345",
        'Accept': 'application/json',
        'X-M2M-Origin': ORIGIN,
        'Locale': 'en'
    }
    print("get resource: " + uri)
    res = http.get(uri, headers=headers)
    return res.json()

def getConOnResponse(res):
    cin = res['m2m:cin']
    return cin['con']
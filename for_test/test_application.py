import requests
import json
def getdata(bno=None):
    d1={}
    if d1 is not None:
        d1['bno']=bno
    json_data=json.dumps(d1)
    res=requests.get("http://127.0.0.1:8000/result/",data=json_data)
    print(res.status_code)
    print(res.json())
getdata(bno='5d')
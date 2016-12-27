import sys
import os
import requests
from workflow import Workflow3

USERNAME = ''
PASSWORD = 'md5'
FILE_PATH = os.getcwd() + '/token'

def createFile():
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'w'):
            pass

def readLocalToken():
    token = None
    with open(FILE_PATH, 'r') as f:
        token = f.readline()
    return token

def checkToken(token):
    params = {'token': token}
    resp = requests.get('http://capi.douyucdn.cn/api/v1/my_info', params=params).json()
    return resp['error'] == 200

def saveToken(token):
    with open(FILE_PATH, 'w') as f:
        f.write(token)

def getToken():
    token = None
    params = dict(username=USERNAME, password=PASSWORD)
    resp = requests.get('http://capi.douyucdn.cn/api/v1/login', params=params).json()
    if resp['error'] != 0:
        print(resp['error'], resp['data'])
    else:
        token = resp['data']['token']
        saveToken(token)
    return token

def getFollows(token):
    params = {'token': token, 'live': 1}
    resp = requests.get('http://capi.douyucdn.cn/api/v1/followRoom', params=params).json()
    return resp['data']

def main(wf):
    createFile()
    token = readLocalToken()
    if not token or not checkToken:
        token = getToken()
    rooms = getFollows(token)
    for room in rooms:
        wf.add_item('[%s] %s' % (room['room_id'], room['room_name']), room['nickname'], arg=room['room_id'], valid=True, icon='icon.png')
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow3()
    sys.exit(wf.run(main))

from flask import Flask, render_template, session, redirect, request
from flask.sessions import SessionInterface
from beaker.middleware import SessionMiddleware
import json
import Dao
import uuid

class BeakerSessionInterface(SessionInterface):
    def open_session(self, app, request):
        session = request.environ['beaker.session']
        return session

    def save_session(self, app, session, response):
        session.save()



app = Flask(__name__)

data = {}

def modelAndView(templateName, data = {}):
    if not session.has_key('auth') and request.endpoint != 'login':
        return redirect('/sign/in')
    else:
        return render_template(templateName, data=data)

@app.route('/')
def main():
    return modelAndView('index.html', data)

@app.route('/sign/in/auth', methods=["GET", "POST"])
def auth():
    getUserId = request.form['userId']
    getUserPw = request.form['userPw']

    retValidUser = Dao.userLoginCheck({"userId": getUserId, "userPw": getUserPw})

    if ( retValidUser != None and len(retValidUser) > 0 ):
        session['auth'] = retValidUser[0]
        data["userId"] = retValidUser[0]
        data["userName"] = retValidUser[1]
        ret = {"result": 200, "err": ""}    # success
    else:
        ret = {"result": 100, "err": ""}    # failure

    return json.dumps(ret)

@app.route('/sign/on')
def signon():
    session.clear()
    return render_template('signon.html')

@app.route('/sign/on/valid_user', methods=["POST"])
def validUserCheck():
    getUserId = request.form['userId']

    duplChkRs = Dao.userDuplicateCheck({"userId": getUserId})

    retData = {}
    if ( duplChkRs[0] == 0 ):
        retData['result'] = 200
    else:
        retData['result'] = 100

    return json.dumps(retData)

@app.route('/sign/on/regist', methods=['POST'])
def signonRegist():
    session.clear()
    getUserId = request.form['userId']
    getUserPw = request.form['userPw']
    getUserName = request.form['userName']

    Dao.insUser({'userId': getUserId, 'userPw': getUserPw, 'userName': getUserName})

    session['auth'] = getUserId
    data["userId"] = getUserId
    data["userName"] = getUserName

    return json.dumps({'result':200, 'err':'', 'data':''})

@app.route('/sign/in')
def login():
    session.clear()
    return modelAndView('login.html')

@app.route('/device/control', methods=['GET'])
def loadDeviceControl():
    return modelAndView('deviceControl.html', data)

@app.route('/device/manage', methods=['GET'])
def loadDeviceManage():
    return modelAndView('deviceManage.html', data)

@app.route('/device/get_device_list', methods=['POST'])
def getDevice():
    retData = {}
    getUserId = request.form['userId']

    retData['data'] = Dao.getDevice({'userId': getUserId})
    if ( retData['data'] != None ):
        retData['result'] = 200
        retData['err'] = ''
    else:
        retData['result'] = 100
        retData['err'] = 'no result'

    return json.dumps(retData)

@app.route('/device/set_pin_status', methods=['POST'])
def udtPinStatus():
    getPinId = request.form['pId']
    getPinStatus = request.form['pinStatus']

    Dao.udtPinStatus({"pinId": getPinId, "pinStatus": getPinStatus})

    retData = {}
    retData['result'] = 200
    retData['err'] = ''
    retData['data'] = ''
    return json.dumps(retData)

@app.route('/device/manage/regist', methods=['GET'])
def loadDeviceManageRegist():
    return modelAndView('deviceManageRegist.html', data)

@app.route('/device/manage/regist_ok', methods=['POST'])
def restDeviceManageRegistOk():
    getDeviceName = request.form['deviceName']
    getDeviceIp = request.form['deviceIp']
    getDevicePort = request.form['devicePort']
    getPinNo = request.form['pinNo']

    Dao.insDevice({'uId': uuid.uuid4().get_hex(), 'userId':data['userId'], 'deviceName':getDeviceName, 'deviceIp':getDeviceIp, 'devicePort':getDevicePort, 'pinNo':getPinNo})

    retData = {}
    retData['result'] = 200
    retData['err'] = ''
    retData['data'] = ''
    return json.dumps(retData)

@app.route('/device/manage/delete', methods=['POST'])
def restDeviceManageDeleteOk():
    getDeviceUid = request.form.getlist('deviceUid')

    Dao.delDevice({'uId':getDeviceUid})

    return json.dumps({'result':200, 'err':'', 'data':''})

if __name__ == '__main__':
    app.wsgi_app = SessionMiddleware(app.wsgi_app)
    app.session_interface = BeakerSessionInterface()
    app.run(host='0.0.0.0', port=8080, debug=True)

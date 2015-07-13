from flask import Flask, request, render_template, jsonify
import ControlGPIO


app = Flask(__name__)

@app.route('/control')
def procControlGPIO():
    pinId = request.args['pId']          # parse pinID on request parameter
    proc = request.args['proc']          # parse pinOnOff on request parameter
    callback = request.args['callback']  # parse callback string ( jsonp )

    if proc and proc == "on":
        ret = ControlGPIO.pinHigh(pinId)
        return callback + "(" + str(ret) + ")"
    elif proc == "off":
        ret = ControlGPIO.pinLow(pinId)
        return callback + "(" + str(ret) + ")"

@app.route('/control/read')
def readControlGPIO():
    uId = request.args['deviceUid']
    pinId = request.args['pinId']          # parse pinID on request parameter
    callback = request.args['callback']  # parse callback string ( jsonp )

    ret = ControlGPIO.pinStatus(uId, pinId)

    return callback + "(" + str(ret) + ")"
    

"""
@app.route('/file/create/<filename>', methods=['POST', 'GET'])
def process_create_file(filename):
    filepath = os.path.dirname(os.path.abspath(__file__)) + "/" + filename

    contents = request.form['contents']
    print "contents : ", contents

    f = open(filepath, mode="w+")
    f.write("1234")
    f.close()

    isFile = os.path.isfile(filepath)

    if isFile:
        f = open(filepath)
        return render_template("viewFileContents.html", fileContents=f.read())
    else:
        return "False"
"""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)


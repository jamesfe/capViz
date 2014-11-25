#!/usr/bin/python
from os.path import isfile
import cgitb
import cgi
import pickle
import json

cgitb.enable()
import capFunc

badIDFile = './badfiles.pickle'

print "Content-Type: text/html\n\r\n"

print """
<html>
<head>
<style>
img {
    margin: 0px;
    padding: 0px;
}
</style>
<script src="./jsFunc.js"></script>
</head>
"""
capSize = 10
jpgDir = "./jpg/"
form = cgi.FieldStorage()
if 'blist' not in form:
    capFunc.dispList(jpgDir, capSize, badIDFile)
    capFunc.showRemoveForm()
else:
    badIDs = set()
    if isfile(badIDFile):
        badIDs = pickle.load(file(badIDFile, 'rb'))
    # print form.getvalue('blist')
    formBadList = json.loads(form.getvalue('blist'))
    for k in formBadList:
        badIDs.add(k)
    pickle.dump(badIDs, file(badIDFile, 'wb'))
    capFunc.dispList(jpgDir, capSize, badIDFile)
    capFunc.showRemoveForm()
print "</html>"

"""
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
"""
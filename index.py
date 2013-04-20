#!/usr/bin/python

from os import listdir
from os.path import isfile
import cgitb, sys, cgi, pickle, json
from math import sqrt
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
form = cgi.FieldStorage()
if('blist' not in form):
	capFunc.dispList("./jpg/", 30, badIDFile)
	capFunc.showRemoveForm()
else:
	badIDs = set()
	if(isfile(badIDFile)):
		badIDs = pickle.load(file(badIDFile, 'rb'))
	#print form.getvalue('blist')
	formBadList = json.loads(form.getvalue('blist'))
	for k in formBadList:
		badIDs.add(k)
	pickle.dump(badIDs, file(badIDFile, 'wb'))
	capFunc.dispList('.', 30, badIDFile)
	capFunc.showRemoveForm()
print "</html>"

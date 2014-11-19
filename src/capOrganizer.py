#!/usr/bin/python
import cgitb
import cgi
import types
import capFunc

cgitb.enable()

print "Content-Type: text/html\n\r\n"


def getHeader():
    retStr = "<html><head><title>cap organizer</title></head>"
    return (retStr)


def getFooter():
    ret_str = "</html>"
    return ret_str


form = cgi.FieldStorage()

print getHeader()

if 'action' in form:
    badPickle = 'badfiles.pickle'
    datPickle = 'statsdat.pickle'
    targetDir = '.'
    dispList = 0  # # this should be turned into a list later on
    d = 40
    newAction = form.getvalue('action')
    if newAction == 'indexsort':
        try:
            a = int(form.getvalue('a'))
            b = int(form.getvalue('b'))
        except:
            print "Issues with the indices.  Must be integers!"
            sys.exit(-1)
        dispList = capFunc.indexsort(badPickle, datPickle, [a, b])
    elif newAction == 'rowsort':
        try:
            a = int(form.getvalue('a'))
            b = int(form.getvalue('b'))
        except:
            print "Issues with the indices.  Must be integers!"
            sys.exit(-1)
        dispList = capFunc.rowsort(badPickle, datPickle, [a, b])
    elif newAction == 'repickle':
        capFunc.repickle(targetDir, datPickle)
    elif newAction == 'showall':
        print "<table>"
        for a in range(0, 6):
            print "<tr>"
            for b in range(0, 6):
                print "<td>"
                print "<h3>" + str(a) + ", " + str(b) + "</h3>"
                dispList = capFunc.rowsort(badPickle, datPickle, [a, b])
                # print dispList[0:3]
                capFunc.showCapSquare(dispList, 8)
                del dispList
                print "</td>"
            print "</tr>"
        print "</table>"
        dispList = -1

    if type(dispList) != types.IntType:
        capFunc.showCapSquare(dispList, d)

else:
    print "<a href=\"./capOrganizer.py?action=indexsort&a=1&b=2\">sort,1,2</a><br>"
    print "<a href=\"./capOrganizer.py?action=repickle\">repickle</a><br>"

print getFooter()

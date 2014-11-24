""" functions that facilitate the HTML output of caps """

from os import listdir
from math import sqrt
import sys
import colorsys
from os.path import isfile, join
import cPickle

# import Image
# import ImageStat


class capDat:
    def __init__(self, fn, r, g, b, h, s, l):
        self.fname = fn
        self.r = r
        self.g = g
        self.b = b
        self.h = h
        self.s = s
        self.l = l

    def __str__(self):
        """ if you want to print yourself."""
        arr = [self.fname, self.r, self.g, self.b, self.h, self.s, self.l]
        return str(arr)

    def getArr(self):
        return [self.r, self.g, self.b, self.h, self.s, self.l]


def dispList(tgtDir, d, badFile):
    """ prints to standard output a square of caps, unorganized,
        minus the bad caps that were previously marked.
        tgtDir - target directory for listing with jpgs inside
        d - dimension, number of caps per line
        badFile - pickled file listing filenames of bad caps (set)
        """
    badList = set()
    if isfile(badFile):
        badList = cPickle.load(file(badFile, 'rb'))
    cDirList = listdir(tgtDir)
    cutLine = round(sqrt(len(cDirList)), 0)
    count = -1
    dimension = str(d)
    for k in cDirList:
        if (k[-4:].lower() == ".jpg") & (k not in badList):
            count += 1
            if count % cutLine == 0:
                sys.stdout.write("<br />\n")
            sys.stdout.write(
                "<img id=\"" + k + "\" onClick=\"deltaBorder(this)\" src=\"" +
                tgtDir + k + "\" height=\"" + dimension + "\" width=\"" +
                dimension + "\">")


def showRemoveForm():
    """ form that updates a list of bad caps and sends it to be added to the
        badCaps pickle list.
    """
    print """
<form method="POST" action="./index.py" onClick="document.getElementById('blist').value=JSON.stringify(badIDList)">
<input type="hidden" name="blist" id="blist" value="test">
<input type="submit" value="remove">
</form>"""


def indexsort(badPFile, pickle_file, indices):
    if len(indices) != 2:
        print "Fail"
        return (-1)
    badFiles = cPickle.load(file(badPFile, 'rb'))
    fileDat = cPickle.load(file(pickle_file, 'rb'))
    if len(fileDat[0].getArr()) <= max(indices):
        print "Sort index too large.  Fail."
        return (-1)
    targetData = []
    for i in fileDat:
        if i.fname not in badFiles:
            targetData.append([i.fname, i.getArr()[indices[0]],
                               i.getArr()[indices[1]]])
    targetData.sort(key=lambda x: x[1])
    targetData.sort(key=lambda x: x[2])

    return targetData


def rowsort(badPFile, pickleFile, indices):
    if len(indices) != 2:
        print "Fail"
        return -1
    badFiles = cPickle.load(file(badPFile, 'rb'))
    fileDat = cPickle.load(file(pickleFile, 'rb'))
    if len(fileDat[0].getArr()) <= max(indices):
        print "Sort index too large.  Fail."
        return -1
    targetData = list()
    for i in fileDat:
        if (i.fname not in badFiles):
            targetData.append([i.fname, i.getArr()[indices[0]],
                               i.getArr()[indices[1]]])
    targetData.sort(key=lambda x: x[1])
    cutLine = int(round(sqrt(len(targetData)), 0))
    for i in range(0, cutLine):
        targetData[i:len(targetData):cutLine] = sorted(
            targetData[i:len(targetData):cutLine],
            key=lambda x: x[2])
    """
    ranges = [[cutLine*(i-1), cutLine*i] for i in range(1, cutLine+1)]
    #print "Pre: ", targetData[0]
    for k in ranges:
        print "R: ", k, "<br>"
        targetData[k[0]:k[1]] = sorted(targetData[k[0]:k[1]], key=lambda x: x[1])
    #print "Post: ", targetData[0]
    """
    """
    for i in range(0, len(targetData)/cutLine):
        cInd = range(i, len(targetData), cutLine)
        tmp = sorted([targetData[i] for i in cInd], key=lambda x: x[1])
        r = 0
        for i in cInd:
            targetData[i] = tmp[r]
            r+=1
    """
    return targetData


def showCapSquare(d_list, d):
    d = str(d)
    cutline = round(sqrt(len(d_list)))
    count = 0
    for k in d_list:
        count += 1
        sys.stdout.write("<img src=\"./" + k[
            0] + "\" height=\"" + d + "\" width=\"" + d + "\">")
        if count % cutline == 0:
            print "<br />\n"


def reScale01(num, mx_num):
    """
    rescale to a 0-1 scale
    :param num:     current value to scale
    :param mx_num:  max value
    :return:
    """
    return (1.0 * num) / mx_num


def repickle(tgt_dir, pickle_file):
    """ creates a new pickle file with the hsl and rgb specs for all the
        caps in the target directory (including bad ones, for glitches.)
    """
    print "repickling<br>"
    file_list = [i for i in listdir(tgt_dir) if
                 ((i[-3:].lower() == 'jpg') & (len(i) > 3))]
    is_list = [(i, ImageStat.Stat(Image.open(join(tgt_dir, i)))) for i in
               file_list]
    cap_list = list()
    for statset in is_list:
        rgb = [reScale01(i, 255) for i in statset[1].mean]
        hsl = list(colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2]))
        cap_list.append(capDat(statset[0], rgb[0], rgb[1], rgb[2],
                               hsl[0], hsl[1], hsl[2]))
        print cap_list[len(cap_list) - 1], "<br>"
    cPickle.dump(cap_list, file(pickle_file, 'wb'))
    return pickle_file

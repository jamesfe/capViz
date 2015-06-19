"""
cv2 test code: pulls out circles in images (bottle caps) and saves them off
into smaller image files for later analysis and rearrangement.

NOTE:
OpenCV and/or cv/cv2 is a real hassle to install.  This project is wonky
because it doesn't use a virtualenv as my system refuses to accept OpenCV for
a virtualenv.  Be careful!
"""

import cv2
from cv2 import cv
from os.path import join, isdir
from os import makedirs


def cv2hough(sobel_image, color_image, minrad, maxrad):
    """
    Identifies and cuts out to a directory potentially circular shapes
    that match a known radius range.
    :param sobel_image: sobel-filtered image
    :param color_image: non-sobel filtered version of colored_image
    :return:
    """

    in_cv_image = cv2.imread(sobel_image, 0)
    avg_rad = (minrad + maxrad) / 2
    circles = cv2.HoughCircles(in_cv_image, cv.CV_HOUGH_GRADIENT, 1, 65,
                               param1=90, param2=15,
                               minRadius=minrad, maxRadius=maxrad)
    export_circles(circles, color_image, 'caps', avg_rad)


def export_circles(circ_data, src_img, out_dir, avg_rad):
    """
    Export circles from an image (given hough xform) to a directory.
    :param circ_data: output from cv2.HoughCircles
    :param src_img: source, color image filename
    :param out_dir: output directory
    :param avg_rad: average radius of cap; user input
    :return: <none>
    """

    src_img_ld = cv2.imread(src_img)
    if not isdir(join('.', out_dir)):
        try:
            makedirs(join('.', out_dir))
        except OSError:
            print "Couldn't make directory"
            exit(-1)
    count = 0
    for k in circ_data[0]:
        rnd = avg_rad
        ## average radius of circle (via user input)
        yo = 20
        ## offset of y - for some reason the hough transform is offset by 20?
        xo = 0
        ## offset for x - in case we need it some day
        cv2.imwrite(join('.', out_dir, "circle_" + str(count) + "_img.jpg"),
                    src_img_ld[k[1] - (yo + rnd):k[1] + (rnd - yo),
                    k[0] - (rnd + xo):k[0] + (rnd - xo)])
        count += 1
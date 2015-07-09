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
from os import makedirs, path


class CapImage:

    @staticmethod
    def validate_paths(file_name, file_path):
        if not path.isfile(path.join(file_path, file_name)):
            raise ValueError
        return True

    def load_image(self):
        self.loaded_image = cv2.imread(self.get_whole_target_path())

    def __init__(self, file_name=None, file_path="./", autoload=False, **kwargs):
        if self.validate_paths(file_name, file_path):
            self.file_name = file_name
            self.file_path = file_path

        self.sobel_image = None
        self.hough_circles = None
        self.minrad = None
        self.maxrad = None
        self.average_rad = None

        if autoload:
            self.load_image()
        else:
            self.loaded_image = None

        if 'param1' in kwargs:
            self.param1 = kwargs['param1']
        else:
            self.param1 = 90

        if 'param2' in kwargs:
            self.param2 = kwargs['param2']
        else:
            self.param2 = 15

    def get_whole_target_path(self):
        return path.join(self.file_path, self.file_name)

    def store_sobel_image(self):
        sobel_x = cv2.Sobel(self.loaded_image, cv.CV_8U, 1, 0)
        sobel_y = cv2.Sobel(self.loaded_image, cv.CV_8U, 0, 1)
        self.sobel_image = cv2.bitwise_or(sobel_x, sobel_y)

    def calculate_hough_circles(self, minrad, maxrad):
        gray_image = cv2.cvtColor(self.sobel_image, cv2.COLOR_BGR2GRAY)
        self.hough_circles = cv2.HoughCircles(gray_image, cv.CV_HOUGH_GRADIENT, 1, 65,
                         param1=self.param1, param2=self.param2,
                         minRadius=minrad, maxRadius=maxrad)
        self.minrad = minrad
        self.maxrad = maxrad
        self.average_rad = sum([self.minrad, self.maxrad])/2

    @staticmethod
    def confirm_and_build_output_directory(output_directory):
        if not isdir(join('.', output_directory)):
            try:
                makedirs(join('.', output_directory))
                return True
            except OSError:
                return False
        else:
            return True

    def export_circles(self, output_directory):
        src_img_ld = self.loaded_image
        if self.confirm_and_build_output_directory(output_directory):
            for index, identified_circle in enumerate(self.hough_circles[0]):
                rounding_val = self.average_rad
                y_offset = 0
                x_offset = 0
                cv2.imwrite(join('.', output_directory, "circle_" + str(index) + "_img.jpg"),
                            src_img_ld[identified_circle[1] - (y_offset + rounding_val):identified_circle[1] + (rounding_val - y_offset),
                            identified_circle[0] - (rounding_val + x_offset):identified_circle[0] + (rounding_val - x_offset)])

if __name__ == '__main__':
    cap_filename = "P1000118.JPG"
    cap_filepath = "../data/"
    test_cap = CapImage(file_name=cap_filename, file_path=cap_filepath, autoload=True)
    test_cap.store_sobel_image()
    test_cap.calculate_hough_circles(40, 70)
    test_cap.export_circles("output_dir")

from PIL import Image, ImageDraw, ImageStat
import colorsys
import time
import re

TESTCONF = """
in_caps_rows=30
in_caps_cols=30
out_caps_rows=30
out_caps_cols=30
in_cap_file=./new_grid_110316_daylight.bmp
incap_pixwidth=80
first_sort=hue
second_sort=saturation
number_order=1
use_temp_name=1
draw_style=pix
"""


class ImageGenerator:
    """
    This is a class that will take an image, cut it up, calculate statistics
    on every cut in the file, and then rearrange it into something the user
    has specified.
    """
    def __init__(self, conf_file):
        self.conf = dict()
        ## cfile = file(conf_file, 'r')
        cfile = TESTCONF.split("\n")
        for keyword in cfile:
            ## A hackish configuration file
            dv = keyword.strip().split("=")
            if len(dv) == 2:
                if re.match("^[0-9]*$", dv[1].strip()) is not None:
                    indat = int(dv[1].strip())
                else:
                    indat = dv[1].strip()
                self.conf[dv[0].strip()] = indat
        self.inImage = Image.open(self.conf['in_cap_file'])
        self.sorts = dict(
            {"red": 0, "green": 1, "blue": 2, "hue": 3, "saturation": 4,
             "lum": 5})
        self.imageDatList = None
        self.sortedDatList = None
        self.outname = None

    def gather_data(self):
        """
        Based on the config file, we cut up the image into x*x segments
        and calculate statistics on each of these segments.
        Note: In later versions, this is replaced with hough transform and cv2
        code.
        :return:
        """
        mult = self.conf['incap_pixwidth']
        self.imageDatList = list()
        for col in range(0, self.inImage.size[0] / mult):
            for row in range(0, self.inImage.size[1] / mult):
                xleft = mult * col
                xright = mult * (col + 1)
                ytop = mult * row
                ybottom = mult * (row + 1)
                box = (xleft, ytop, xright, ybottom)
                subregion = self.inImage.crop(box)
                rgb_means = ImageStat.Stat(subregion).mean
                hsl_means = colorsys.rgb_to_hls(rgb_means[0] / 255,
                                                rgb_means[1] / 255,
                                                rgb_means[2] / 255)
                tinsert = rgb_means + list(hsl_means) + [subregion]
                self.imageDatList.append(tinsert)

    def first_sort(self):
        """
        Reach into the internal config and find out what we want to have as
        our first order sort on the caps.
        :return:
        """
        self.sortedDatList = sorted(self.imageDatList,
                                    key=lambda thislist: thislist[
                                        self.sorts[self.conf['first_sort']]])
        del self.imageDatList
        self.imageDatList = self.sortedDatList

    def second_sort(self):
        """
        Second sort on the caps: sort rows individually.
        Example: We want a 30x30 grid of caps, sorted first by hue, then by
        saturation.
        We sort by hue in first_sort, then in second_sort, we sort 30 lists
        of 30 caps each individually and replace them into the list.
        :return:
        """
        ranges = [[self.conf['out_caps_cols'] * (p - 1),
                   self.conf['out_caps_cols'] * p] for p in
                  range(1, self.conf['out_caps_rows'] + 1)]
        for r in ranges:
            self.imageDatList[r[0]:r[1]] = sorted(self.imageDatList[r[0]:r[1]],
                                                  key=lambda thislist: thislist[
                                                      self.sorts[self.conf[
                                                          'second_sort']]])

    def save_image(self):
        """
        Given the rearrangement that we have done on imageDatList,
        now is the time to slice and dice every image into its place on
        the master image.
        :return:
        """
        count = 0
        if self.conf['number_order'] == 1:
            for i in xrange(0, len(self.imageDatList)):
                dr = ImageDraw.Draw(self.imageDatList[i][6])
                dr.text((0, 0), str(count), fill="white")
                count += 1
                del dr
        del count

        out_img = Image.new("RGB", (
            self.conf['out_caps_cols'] * self.conf['incap_pixwidth'],
            self.conf['out_caps_rows'] * self.conf['incap_pixwidth']))
        draw = ImageDraw.Draw(out_img)
        mult = self.conf['incap_pixwidth']
        count = 0
        for row in range(0, self.conf['out_caps_rows']):
            for col in range(0, self.conf['out_caps_cols']):
                xleft = mult * col
                xright = mult * (col + 1)
                ytop = mult * row
                ybottom = mult * (row + 1)
                box = (xleft, ytop, xright, ybottom)
                if self.conf['draw_style'] == 'pix':
                    draw.rectangle(box, fill=(int(self.imageDatList[count][0]),
                                              int(self.imageDatList[count][1]),
                                              int(self.imageDatList[count][2])))
                elif self.conf['draw_style'] == 'caps':
                    out_img.paste(self.imageDatList[count][6], box)
                count += 1
        ctime = str(time.time())[:-3]
        self.outname = ctime + "_hsvrgb_sort_" + self.conf['first_sort'] + "_" + \
                       self.conf['second_sort'] + ".jpg"
        if self.conf['use_temp_name'] == 1:
            self.outname = "temp.jpg"
        out_img.save(self.outname)


if __name__ == "__main__":
    img_gen = ImageGenerator("img_read.conf")
    img_gen.gather_data()
    img_gen.first_sort()
    img_gen.second_sort()
    img_gen.save_image()

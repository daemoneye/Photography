#!/usr/bin/env python3
import argparse
import os
import sys
from PIL import Image


class PHOTO:
    def __init__(self):
        self.image_name = ""
        self.image_filepath = ""
        self.thumbnail_filepath = ""
        self.html_filepath = ""
        self.exif_data = {}

    def set_data(self, image_name, image_fp, thumbnail_fp, html_fp):
        self.image_name = image_name
        self.image_filepath = image_fp
        self.thumbnail_filepath = thumbnail_fp.split('/')[5] + "/" + thumbnail_fp.split('/')[6] + "/"
        self.html_filepath = html_fp

    def set_exif_data(self):
        command = "exiftool " + str(self.image_filepath + self.image_name)
        for each in os.popen(command):
            each_data = each.split(':')
            key = each_data[0].strip().replace(" ", "_")
            value = each_data[1].strip()
            self.exif_data[key] = value

    def create_thumbnail(self):
        thumbnail_division = 25
        if not os.path.exists(self.image_filepath + "thumbnails/"):
            os.mkdir(self.image_filepath + "thumbnails/")
        im = Image.open(self.image_filepath + self.image_name)
        width, height = im.size
        MAX_SIZE = (int(width/thumbnail_division), int(height/thumbnail_division))
        im.thumbnail(MAX_SIZE)
        im.save(self.image_filepath + "thumbnails/" + self.image_name, "JPEG")

    def generate_html(self):
        if not os.path.exists(self.html_filepath):
            os.mkdir(self.html_filepath)

        exif_info_list = ['File_Name', 'Camera_Model_Name', 'Aperture', 'ISO', 'Shutter_Speed', 'Lens_ID', 'Focal_Length', 'Shooting_Mode']

        HEADER = "<!DOCTYPE HTML>\n\n<html>\n<head>\n<title>" + self.image_name + "</title>\n<link rel=\"stylesheet\" href=\"../../styles.css\">\n</head>\n<body>\n"
        FOOTER = "</body>\n<p>Copyright 2021 Keane Wolter</p>\n</footer>\n"
        IMG = "<div class=\"images\">\n<img src=\"../" + self.image_name + "\" id=\"image_canv\" class=\"rotateimg0\" width=\"100%\">\n</div>\n"
        DATA = "<div class=\"exif\">\n<table border=\"1\">\n<tr>\n"
        for each in exif_info_list:
            DATA += "<td>" + each + "</td>\n"
        DATA += "</tr>\n<tr>\n"
        for each in exif_info_list:
            DATA += "<td>"
            if each == 'Aperture':
                DATA += "f/"
            DATA += self.exif_data[each]
            DATA += "</td>\n"
        DATA += "</table>\n</div>"

        f = open(self.html_filepath + self.image_name.split('.')[0] + ".html", 'w')
        f.write(HEADER + IMG + DATA + FOOTER)
        f.close()

    def add_to_index(self):
        return "<div class=\"image\"><a href=\"" + self.html_filepath.split('/')[5] + "/" + self.html_filepath.split('/')[6] + "/" + self.image_name.split('.')[0] + ".html" + "\" /><img src=\"" + self.thumbnail_filepath + self.image_name + "\" /></a><p>" + self.image_name + "</p></div>\n"


def get_args():
    parser = argparse.ArgumentParser(description="Code generator for https://pics.daemo.nz")
    parser.add_argument('-v', '--verbose',
                        dest='verbose',
                        action='store_true',
                        help='Be verbose')
    parser.add_argument('--version',
                        dest='version',
                        action='store_true',
                        help="Display version and exit")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    version = 3.10

    if args.version:
        print("site.py " + str(version))
        sys.exit()

    photos = []

    HEADER = "<!DOCTYPE HTML>\n\n<html>\n<head>\n<title>Daemoneye's Photos</title>\n<link rel=\"stylesheet\" href=\"styles.css\">\n</head>\n"
    FOOTER = "<footer>\n<p>Script generation version: " + str(version) + "</p>\n<p>Image Copyright 2021 Keane Wolter</p>\n</footer>\n</html>"
    BODY = "<body>\n"

    image_filepath = "/var/www/html/photos"
    for subdir, dirs, files in os.walk(image_filepath):
        if "thumbnail" not in subdir and not subdir.endswith("html"):
            for images in os.listdir(subdir):
                if "jpg" in images or "JPG" in images:
                    tmp = PHOTO()
                    tmp.set_data(images, subdir + "/", subdir + "/thumbnails/", subdir + "/html/")
                    photos.append(tmp)

    if args.verbose:
        print("[+] Sorting photos by name")
    photos.sort(key=lambda PHOTO: PHOTO.image_name)

    for photo in photos:
        if args.verbose:
            print("[+] Working on image " + images)
        if args.verbose:
            print("\t[-] Getting EXIF data")
        photo.set_exif_data()
        if args.verbose:
            print("\t[-] Generating thumbnail")
        photo.create_thumbnail()
        if args.verbose:
            print("\t[-] Adding image to index page")
        photo.generate_html()
        BODY = BODY + photo.add_to_index()

    BODY += "</body>"

    with open(image_filepath + "/index.html", "w") as f:
        f.write(HEADER + BODY + FOOTER)

    for subdir, dirs, files in os.walk(image_filepath):
        if "thumbnail" not in subdir and not subdir.endswith("html") and not subdir.endswith('photos'):
            HEADER_2 = "<!DOCTYPE HTML>\n\n<html>\n<head>\n<title>" + subdir + "</title>\n<link rel=\"stylesheet\" href=\"../styles.css\">\n</head>\n"
            FOOTER_2 = "<footer>\n<p>Image Copyright 2021 Keane Wolter</p>\n</footer>\n</html>"
            BODY_2 = "<body>\n"
            if args.verbose:
                print("[+] Generating index for " + subdir)
            for images in os.listdir(subdir):
                if "jpg" in images or "JPG" in images:
                    tmp = PHOTO()
                    tmp.set_data(images, subdir + "/", subdir + "/thumbnails/", subdir + "/html/")
                    BODY_2 += tmp.add_to_index().replace('"2', '"../2')
            BODY_2 += "</body>"
            with open(subdir + '/index.html', 'w') as f:
                f.write(HEADER_2 + BODY_2 + FOOTER_2)

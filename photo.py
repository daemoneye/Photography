#!/usr/bin/env python 3
import os
from PIL import Image


class PHOTO:
    def __init__(self):
        self.image_name = ""
        self.image_filepath = ""
        self.thumbnail_filepath = ""
        self.html_filepath = ""
        self.time_filepath = ""
        self.exif_data = {}

    def set_data(self, image_name, image_fp, thumbnail_fp, html_fp, time_fp):
        '''Set Variables needed for a photo'''
        self.image_name = image_name
        self.image_filepath = image_fp
        self.thumbnail_filepath = thumbnail_fp.split('/')[5] + "/" + thumbnail_fp.split('/')[6] + "/"
        self.html_filepath = html_fp
        self.time_filepath = time_fp

    def set_time_file(self):
        '''Obtain the create time of the image and store it for future reference'''
        if not os.path.exists(self.time_filepath):
            os.mkdir(self.time_filepath)
        f = open(self.time_filepath + self.image_name.split('.')[0] + ".txt", 'w')
        f.write(str(os.path.getctime(self.image_filepath + self.image_name)))
        f.close()

    def set_exif_data(self):
        '''Collect exif data from an image'''
        command = "exiftool " + str(self.image_filepath + self.image_name)
        for each in os.popen(command):
            each_data = each.split(':')
            key = each_data[0].strip().replace(" ", "_")
            value = each_data[1].strip()
            self.exif_data[key] = value

    def same_timestamps(self):
        '''Check if the timestamp saved matches the creation timestamp on the file'''
        file_time = 0
        photo_time = 0
        if os.path.exists(self.time_filepath + self.image_name.split('.')[0] + '.txt'):
            with open(self.time_filepath + self.image_name.split('.')[0] + ".txt") as f:
                file_time = float(f.read())
            photo_time = os.path.getctime(self.image_filepath + self.image_name)
            return file_time == photo_time
        else:
            return False

    def create_thumbnail(self):
        '''Generate the thumbnail of an image'''
        thumbnail_division = 25
        if not os.path.exists(self.image_filepath + "thumbnails/"):
            os.mkdir(self.image_filepath + "thumbnails/")
        im = Image.open(self.image_filepath + self.image_name)
        width, height = im.size
        MAX_SIZE = (int(width/thumbnail_division), int(height/thumbnail_division))
        im.thumbnail(MAX_SIZE)
        im.save(self.image_filepath + "thumbnails/" + self.image_name, "JPEG")

    def generate_html(self):
        '''Generate webpage for the image'''
        if not os.path.exists(self.html_filepath):
            os.mkdir(self.html_filepath)

        exif_info_list = ['File_Name', 'Camera_Model_Name', 'Aperture', 'ISO', 'Shutter_Speed', 'Lens_ID', 'Focal_Length', 'Shooting_Mode']
        HEADER = "<!DOCTYPE HTML>\n\n<html>\n<head>\n<title>" + self.image_name + "</title>\n<link rel=\"stylesheet\" href=\"../../styles.css\">\n</head>\n<body>\n"
        FOOTER = "</body>\n<p>Copyright 2021 Keane Wolter</p>\n</footer>\n"
        IMG = "<div class=\"images\" width=\"100%\">\n<img src=\"../" + self.image_name + "\" id=\"image_canv\" class=\"rotateimg0\" width=\"100%\">\n</div>\n"
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
        '''Returns the html for the image index page'''
        return "<div class=\"image\"><a href=\"" + self.html_filepath.split('/')[5] + "/" + self.html_filepath.split('/')[6] + "/" + self.image_name.split('.')[0] + ".html" + "\"><img src=\"" + self.thumbnail_filepath + self.image_name + "\"></a><p>" + self.image_name + "</p></div>\n"

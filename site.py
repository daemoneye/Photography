#!/usr/bin/env python3
import argparse
import os
import sys
from PIL import Image
from photo import PHOTO


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


def generate_photo(photo, args):
    if args.verbose:
        print("[+] Working on image " + photo.image_name)
    if args.verbose:
        print("\t[-] Getting EXIF data")
    photo.set_exif_data()
    photo.resize()
    if args.verbose:
        print("\t[-] Setting time data")
    photo.set_time_file()
    if args.verbose:
        print("\t[-] Generating thumbnail")
    photo.create_thumbnail()
    if args.verbose:
        print("\t[-] Adding image to index page")
    photo.generate_html()


def main():
    args = get_args()
    version = 4.4
    image_filepath = "/var/www/html/photos"
    photos = []
    HEADER = "<!DOCTYPE HTML>\n\n<html>\n<head lang=\"en\">\n<title>Daemoneye's Photos</title>\n<link rel=\"stylesheet\" href=\"styles.css\">\n<meta charset=\"utf-8\">\n</head>\n"
    FOOTER = "\n<footer>\n<p>Script generation version: " + str(version) + "</p>\n<p>Image Copyright 2021 Keane Wolter</p>\n</footer>\n</html>"
    BODY = "<body>\n"

    if args.version:
        print("site.py " + str(version))
        sys.exit()

    if args.verbose:
        print("[+] Collecting Images")
    for subdir, dirs, files in os.walk(image_filepath):
        if "thumbnail" not in subdir and not subdir.endswith("html") and not subdir.endswith("time"):
            for images in os.listdir(subdir):
                if "resize" not in images:
                    if "jpg" in images or "JPG" in images:
                        tmp = PHOTO()
                        tmp.set_data(images, subdir + "/", subdir + "/thumbnails/", subdir + "/html/", subdir + "/time/", subdir + "/comments/")
                        photos.append(tmp)

    if args.verbose:
        print("[+] Sorting photos by name")
    photos.sort(key=lambda PHOTO: PHOTO.image_name)

    for photo in photos:
        if os.path.exists(photo.time_filepath):
            if photo.same_timestamps():
                if args.verbose:
                    print("[+] Skipping " + photo.image_name + ".")
            else:
                generate_photo(photo, args)
        else:
            generate_photo(photo, args)
        BODY = BODY + photo.add_to_index()

    BODY += "</body>"

    with open(image_filepath + "/index.html", "w") as f:
        f.write(HEADER + BODY + FOOTER)

    for subdir, dirs, files in os.walk(image_filepath):
        if "thumbnail" not in subdir and not subdir.endswith("html") and not subdir.endswith('photos') and not subdir.endswith('time'):
            HEADER_2 = "<!DOCTYPE HTML>\n\n<html lang=\"en\">\n<head>\n<title>" + subdir + "</title>\n<link rel=\"stylesheet\" href=\"../styles.css\">\n<meta charset=\"utf-8\"/>\n</head>\n"
            FOOTER_2 = "\n<footer>\n<p>Image Copyright 2021 Keane Wolter</p>\n</footer>\n</html>"
            BODY_2 = "<body>\n"
            if args.verbose:
                print("[+] Generating index for " + subdir)
            for images in os.listdir(subdir):
                if "jpg" in images or "JPG" in images:
                    tmp = PHOTO()
                    tmp.set_data(images, subdir + "/", subdir + "/thumbnails/", subdir + "/html/", subdir + "/time/", subdir + "/comments/")
                    BODY_2 += tmp.add_to_index().replace('"2', '"../2')
            BODY_2 += "</body>"
            with open(subdir + '/index.html', 'w') as f:
                f.write(HEADER_2 + BODY_2 + FOOTER_2)


if __name__ == "__main__":
    main()

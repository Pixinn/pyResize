
#
# pyConvert.py
# Copyright (C) 2016 Christophe Meneboeuf <christophe@xtof.info>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


#!/usr/bin/python3

import os
import argparse
import json


# PARSING COMMAND LINE ARGUMENTS
parser = argparse.ArgumentParser(description="This script recursively resize all images of a given directory.")
parser.add_argument("dir_input", help="Input directory containing your images")
parser.add_argument("dir_output", help="Output directory")
parser.add_argument("size", help="Targeted *long* edge size")
parser.add_argument("-j","--json", help="JSON file used to determine if an image needs to be processed. Based on its modification time.")
parser.add_argument("-q","--quality", type=int, default=75, help="Quality of the saved jpeg, from 0 to 100")
args = parser.parse_args()
# Sanity
if not os.path.isdir(args.dir_input):
    print(args.dir_input + " is not a directory.")
    exit(-1)
if args.quality < 0 or args.quality > 100:
    print("Quality out of range")
    exit(-1)
if not os.path.exists( args.dir_output ):
    os.makedirs( args.dir_output )


# LISTING THE JPEGS FILES
image_suffixes = (".jpg", ".jpeg", ".JPG", ".JPEG")
files_jpeg_in = [ [os.path.join(root, name), os.path.getmtime(os.path.join(root, name))]  # [ file's absolute path, file's modification time ]
                 for root, dirs, files in os.walk(args.dir_input)
                 for name in files
                 if name.endswith(image_suffixes)]

# LOADING PREVIOUS ITERATION RESULT
result_previous = dict();
if args.json != None and os.path.exists( args.json ):
    try:
        with open(args.json, "r") as result_in:
            decoded = json.load( result_in )
        for image in decoded:
            result_previous[ image[0] ] = image[1]
    except ValueError:
        print(ValueError)
        exit(-1)
else:
    print("No suitable JSON file provided")


# PROCESSING THE FILES
images_processed = []
nb_images_processed = 0
for image in files_jpeg_in:
    # output folder
    dir_out = ( args.dir_output + "/" + os.path.dirname(image[0].replace(args.dir_input,"")) ).replace("//","/") + "/"
    if not os.path.exists( dir_out ):
        os.makedirs( dir_out )
    filename = os.path.basename( image[0] )
    # Processing
    try:
        filepath_output = "\"" + (dir_out+filename).replace("//","/") + "\""
        # Only if the destination file is not up to date
        time_previous_modification = result_previous.get(  image[0] )
        if not os.path.exists( filepath_output ) or time_previous_modification == None or not time_previous_modification == image[1] :
            cmd = "convert " + "\"" + image[0] + "\"" + " -resize " + args.size + "x" + args.size + " -quality " + str(args.quality) + " -filter Lanczos " + filepath_output
            print( cmd )
            if os.system( cmd ) == 0:
                nb_images_processed += 1
        images_processed.append( image )
    except ValueError:
        print(ValueError)
print( "{} image was processed.".format(nb_images_processed) if nb_images_processed < 1 else "{} images were processed.".format(nb_images_processed) )


# SAVING RESULT
if args.json != None:
    try:
        print("JSON: " + args.json)
        with open( args.json, "w") as result_out:
            json.dump(images_processed, result_out, sort_keys=True, indent=1)
    except ValueError:
        print(ValueError)
        exit(-1)

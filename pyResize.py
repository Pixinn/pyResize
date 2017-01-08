#!/usr/bin/env python3
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


import os
import argparse
import json


# PARSING COMMAND LINE ARGUMENTS
parser = argparse.ArgumentParser(description="This script recursively resize all images of a given directory.")
parser.add_argument("dir_input", help="Input directory containing your images")
parser.add_argument("dir_output", help="Output directory")
parser.add_argument("size", help="Targeted *long* edge size")
parser.add_argument("-q","--quality", type=int, default=75, help="Quality of the saved jpeg, from 0 to 100")
parser.add_argument("-j","--json", help="JSON file used to determine if an image needs to be processed a second time.")
parser.add_argument("-i","--ignore", help="Text file containing pattern in file paths to ignore.")
parser.add_argument("-v","--verbose", action="store_true", help="Display more info while running.")
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


# REMOVING THE IGNORED PATHS
patterns_ignored = []
if args.ignore != None and os.path.exists( args.ignore ):
    with open(args.ignore, 'r') as text_ignored:
        for line in text_ignored:
            patterns_ignored.append(line.strip('\n'))

images_ignored = []
for image in files_jpeg_in:
    for pattern in patterns_ignored:
        path_image = image[0]
        if pattern in path_image:
            if args.verbose:
                print("Ignoring ", path_image, ": ", pattern, "pattern found")
            images_ignored.append(image)
            break
for image in images_ignored:
    files_jpeg_in.remove(image)


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
images_ignored = []
images_error = []
for image in files_jpeg_in:
    path_image = image[0]
    image_time_modified = image[1]
    # output folder
    dir_out = ( args.dir_output + "/" + os.path.dirname(image[0].replace(args.dir_input,"")) ).replace("//","/") + "/"
    if not os.path.exists( dir_out ):
        os.makedirs( dir_out )
    filename = os.path.basename( image[0] )
    # Processing
    try:
        filepath_output = "\"" + (dir_out+filename).replace("//","/") + "\""
        # Only if the destination file is not up to date
        time_previous_modification = result_previous.get( image[0] )
        if not os.path.exists( filepath_output.strip('\"') ) or time_previous_modification == None or not time_previous_modification == image[1] :

            if args.verbose:
                print("=========\nSource path: ", path_image, "\nSource modification time: ", image_time_modified  )
                print("Target path: ", filepath_output)
                print("Target exists? ", os.path.exists( filepath_output.strip('\"') ), "\Target modification time: ", time_previous_modification)

            cmd = "convert " + "\"" + image[0] + "\"" + " -resize " + args.size + "x" + args.size + " -quality " + str(args.quality) + " -filter Lanczos " + filepath_output
            print( cmd )
            if os.system( cmd ) == 0:
                images_processed.append( image )
            else:
                images_error.append( image )
        else:
            images_ignored.append( image )

    except ValueError:
        print(ValueError)

print( "{} image was processed.".format(len(images_processed)) if len(images_processed) <= 1 else "{} images were processed.".format(len(images_processed)))
print( "{} image was ignored.".format(len(images_ignored)) if len(images_ignored) <= 1 else "{} images were ignored.".format(len(images_ignored)))
print( "{} error.".format(len(images_error)) if len(images_error) <= 1 else "{} errors.".format(len(images_error)))


# SAVING RESULT
if args.json != None:
    try:
        print("JSON: " + args.json)
        with open( args.json, "w") as result_out:
            json.dump(images_processed + images_ignored, result_out, sort_keys=True, indent=1)
    except ValueError:
        print(ValueError)
        exit(-1)

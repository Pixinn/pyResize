This script recursively resizes all Jpeg files in a folder.
The folder structure of the folder will be mirrored in the destination.
Source file-paths matching provided patterns can be ignored. Result can be saved
 in a json file so the unmodified input files won't be processed next time.
It relies on "convert" from _ImageMagick_.

# Requirements

* Python 3
* ImageMagick

# usage

usage: pyResize.py [-h] [-q QUALITY] [-j JSON] [-i IGNORE] [-v] input output size

## Required arguments
* input  : Input folder containing the Jpeg to recursively process
* output : Output folder where the resized images will be saved
* size   : Long edge size desired

## Optional arguments
* -h, --help            : show this help message and exit
* -q QUALITY, --quality QUALITY
                        : Quality of the saved jpeg, from 0 to 100
* -i IGNORE, --ignore IGNORE
                        : Text file containing pattern in file paths to ignore.
* -v, --verbose         : Display more info while running.

## Ignore list
An "ignore list" can be provided. It is a text file containing patterns to ignore.  
One pattern per line.

If a source filepath contains one of those patterns, it won't be processed.

## JSON output
A JSON file will be created in the output directory, listing all source images
which where resized during the process.  
If pyResize is called later, targeting the very same directory, unmodified source
images won't be processed again.

This script recursively resizes all Jpeg files in a folder.
The folder structure of the folder will be mirrored in the destination.
It relies on "convert" from _ImageMagick_.

# Requirements

* Python 3
* ImageMagick

# usage

pyConvert.py [-h] [-j JSON] [-q QUALITY] input output size

## Required arguments
* input  : Input folder containing the Jpeg to recursively process
* output : Output folder where the resized images will be saved
* size   : Long edge size desired

## Optional arguments
* -j --json    : A report that can be used during a later call in order to process only the source images that have been modified
* -q --quality : Jpeg quality [0:100]
* -h --help    : Displays help

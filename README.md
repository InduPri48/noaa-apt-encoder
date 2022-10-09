# noaa-apt-encoder
This is a simple program to take two user-given images and stitch them together, in accordance with the Automatic Picture Transmission (APT) protocol used by the NOAA weather satellites (NOAA-15, -18, and -19),  and the resulting image is saved. This composite image is then modulated on to a 2.4kHz carrier tone and saved as a 44.6kHz WAV file.

## Important
This program is a simple Python script. To use this script, run the command "python encode.py [path_to_videoA_image] [path_to_videoB_image]"

## Notes

* The two images may have any height but they must be 909px wide.
* APT only encodes grayscale images, so only the red pixel channel from each image is used.
* The output location of the composite image and WAV file output is the current working directory of the project.
* This script needs Python packages Scipy, Numpy, and Python Image Library (PIL)

## To Do

* Add user-chosen names for the outputted files
* Add user-chosen sample rates for the WAV file

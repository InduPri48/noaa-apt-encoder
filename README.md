# noaa-apt-encoder
A simple app for converting two 909px wide images to a composite image according to the Automatic Picture Transmission Protocol and then modulated onto a carrier audio wave and exported as a WAV file.

## Important
This app is very basic and I am working to develop the program so that it has greater functionality.

## Notes

* The two images may have any height but must be 909px wide if they are to be decoded again by other software.
* The image should be grayscale (i.e. R, G, and B channels all have the same pixel values) but the program only uses the red channel anyway
* The output location of the composite image is the current working directory of the project currently
* There is no command line interface currently

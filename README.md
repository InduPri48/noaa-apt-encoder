# noaa-apt-encoder

[Automatic Picture Transmission](https://www.sigidwiki.com/wiki/Automatic_Picture_Transmission_(APT)) (APT) is used to send weather satellite photos from the NOAA satellites (NOAA-15, NOAA-18, and NOAA-19) to ground stations. Two channels of pictures are taken, usually one visible light and one infrared, that are each 909px wide. These are then combined into an APT image along with sync, spacing, and telemetry information. This image is then scanned line-by-line, with each line taking 0.5 seconds to be transmitted. Each pixel has a brightness value between 0 (black) and 255 (white) that amplitude modulates a 2400Hz carrier wave. This modulated carrier is then transmitted at around 137MHz (the exact value depends on which satellite).

## How to install and use this program

* Clone this repo via `git clone https://github.com/InduPri48/noaa-apt-encoder.git`.
* Navigate inside the folder `noaa-apt-encoder`.
* Run `python encode.py [videoA_filepath] [videoB_filepath] [audio_filepath]`.
* The program will also create the combined APT image at the same location as the WAV audio file, also with the same name.
* The program can also resample the audio to a value of your choosing. Add the rate as the final argument after `[audio_filepath]`. Without this, it will output it at sample rate of 11025Hz.

## Notes

* The two images may have any height but they must be 909px wide.
* The APT format only encodes grayscale images, so only the red pixel channel from each image is used.
* Please make sure you have the Python modules listed in `requirements.txt`, as these are all used by the program

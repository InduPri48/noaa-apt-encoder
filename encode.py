import sys
import scipy.io.wavfile as wav
from PIL import Image
import numpy as np

def generate_carrier(length, amplitude=1000, fs=41600, freq=2400): # Rather arbitrary amplitude chosen here

    N = int(fs * length)
    w = 2 * np.pi * freq
    
    t = np.linspace(0, length, N)

    y = amplitude * np.sin(w * t)
    
    return fs, y

# Some simple input validation for the two required image filepaths
if not len(sys.argv) > 2:
    
    print("Incorrect parameters supplied")
    exit()

videoA_filepath, videoB_filepath = sys.argv[1:] # Get filepaths for both video files

try:
    
    videoA = Image.open(videoA_filepath)
    
except:
    
    print("Could not load videoA image")
    exit()
    
try:
    
    videoB = Image.open(videoB_filepath)
    
except:
    
    print("Could not load videoB image")
    exit()

if videoA.width != 909:
    
    print("Video A does not have a width of 909px")
    exit()

if videoB.width != 909:
    
    print("Video B does not have a width of 909px")
    exit()

videoA_pixels = np.asarray(videoA)[:, :, 0] # Get the red pixel values for the video images as the images will be grayscale anyway
videoB_pixels = np.asarray(videoB)[:, :, 0]

syncA_pixels = np.array([0,0,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0], dtype=np.int8) * 255 # Generate a line of the sync line pixels
syncB_pixels = np.array([0,0,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0], dtype=np.int8) * 255

spaceA_pixels = np.zeros(47, dtype=np.int8) * 255 # Generate a line of the space pixels
spaceB_pixels = np.ones(47, dtype=np.int8) * 255

height = len(videoA_pixels) # Get the vertical height of the video images

telemA_pixels = np.ones(45, dtype=np.int8) * 32 # Generate a blank space to fill the space where the telemetry data would be
telemB_pixels = np.ones(45, dtype=np.int8) * 32

image = np.concatenate((syncA_pixels, spaceB_pixels, videoA_pixels[0], telemA_pixels, syncB_pixels, spaceA_pixels, videoB_pixels[0], telemB_pixels)) # Create the first complete line of the final image
    
for i in range(1, height):

    # This part essentially adds the minute markers in the spacing columns and a gradient pattern in the telemetry zones in accordance with the APT protocol
    mm = i % 120 == 0 or i % 120 == 1

    tm = (i >> 4) % 16

    tm_col = 255
    if tm < 8:

        tm_col = 32 * (tm + 1)
        tm_col = min(tm_col, 255)

        telemA_pixels = np.ones(45, dtype=np.int8) * tm_col
        telemB_pixels = np.ones(45, dtype=np.int8) * tm_col

    elif tm == 8:

        telemA_pixels = np.ones(45, dtype=np.int8) * 0
        telemB_pixels = np.ones(45, dtype=np.int8) * 0
            
    else:

        telemA_pixels = np.ones(45, dtype=np.int8) * 128
        telemB_pixels = np.ones(45, dtype=np.int8) * 128

    row = np.concatenate((syncA_pixels, spaceB_pixels if mm else spaceA_pixels, videoA_pixels[i], telemA_pixels, syncB_pixels, spaceA_pixels if mm else spaceB_pixels, videoB_pixels[i], telemB_pixels))
        
    image = np.vstack((image, row)) # Shuffle the rows around to make a proper array ready to be converted into an image again
    image = image.astype(np.uint8)

Image.fromarray(image).save("image.png") # Save the final image before we modulate it upon the 2400Hz carrier

width = 2080 # Final image total width
height = len(image) # Final image total height

image = np.asarray(image).flatten() / 255 # Normalise the pixels from 0-255 to 0-1

fs, carrier = generate_carrier(height * 0.5)
    
sl = int((fs * 0.5) / width) # How many samples of carrier will one pixel be encoded over
    
expanded = np.repeat(image, sl) # Blow up the image by the scale length factor so that the image pixel count and total carrier sample count match
    
modulated = carrier * expanded # Amplitude modulution here

modulated = modulated.astype(np.int16) # Simple type change ready to be saved as WAV
    
wav.write("audio_file.wav", fs, modulated) # Save the modulated carrier as a WAV file

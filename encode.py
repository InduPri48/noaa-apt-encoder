from PIL import Image
import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as sps
import sys

# Read the command line arguments: videoA location, videoB location, audio location. Optionally sample rate too
args = sys.argv[1:]
if len(args) < 3:

    print("Not enough arguments provided")
    exit()
    
else:

    videoA_filepath = args[0]
    videoB_filepath = args[1]
    audio_filepath = args[2]

    if len(args) > 3:

        try:
            output_sample_rate = int(args[3])
        except:
            print("Failed to parse the given sample rate into an integer") 
            exit()
            
    else:

        output_sample_rate = 11025

# Load the video A and video B images
try:
    videoA_image = Image.open(videoA_filepath)
except:

   print("Failed to open video A image file")
   exit()

try:
    videoB_image = Image.open(videoA_filepath)
except:

   print("Failed to open video B image file")
   exit()
   
# Check to see if both images are 909px wide
if videoA_image.width != 909:

    print("Video A image is not 909px wide")
    exit()

if videoB_image.width != 909:

    print("Video B image is not 909px wide")
    exit()

# Check to see if both images have the same height
if videoA_image.height != videoB_image.height:

    print("The two images do not have matching heights")
    exit()

# Convert the image to an 256 level array of each line of pixels i.e. a 2D array of array[row][col]. The red channel is chosen only.
videoA_pixels = np.asarray(videoA_image)[:, :, 0]
videoB_pixels = np.asarray(videoB_image)[:, :, 0]

# Generate one line of the sync pixels
syncA_pixels = np.array([0,0,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0], dtype=np.int8) * 255
syncB_pixels = np.array([0,0,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0], dtype=np.int8) * 255

# Generate one line of the space pixels
spaceA_pixels = np.zeros(47, dtype=np.int8)
spaceB_pixels = np.ones(47, dtype=np.int8) * 255

# Create an empty array for our final image
image_pixels = np.zeros(shape=(videoA_image.height, 2080))

# Go through each line of pixels to create the final image
for line in range(0, videoA_image.height):

    minute_marker = line % 120 == 0 # will this line contain a minute marker in the spacings

    # Telemetry
    telemetry_block = (line // 8) % 16

    if telemetry_block < 8:

        block_color = 32 * (telemetry_block)
        
        telemetryA_pixels = np.ones(45, dtype=np.int8) * block_color
        telemetryB_pixels = np.ones(45, dtype=np.int8) * block_color

    elif telemetry_block == 8:

        telemetryA_pixels = np.zeros(45, dtype=np.int8)
        telemetryB_pixels = np.zeros(45, dtype=np.int8)

    else:
        
        telemetryA_pixels = np.ones(45, dtype=np.int8) * 128
        telemetryB_pixels = np.ones(45, dtype=np.int8) * 128
        
    # stitch an entire row of the image together
    row = np.concatenate((syncA_pixels, spaceB_pixels if minute_marker else spaceA_pixels, videoA_pixels[line], telemetryA_pixels, syncB_pixels, spaceA_pixels if minute_marker else spaceB_pixels, videoB_pixels[line], telemetryB_pixels))

    image_pixels[line] = row

# Convert the pixel array back into a PIL image and save it
image_pixels = image_pixels.astype(np.uint8)
image = Image.fromarray(image_pixels)
image_filepath = audio_filepath[:audio_filepath.index('.')] + '.png'
image.save(image_filepath)

# Flatten the image pixels array to a 1D array and normalize it
image_pixels = np.asarray(image).flatten() / 255

# Generate a carrier wave at 2400Hz
sample_rate = 2080 * 20
duration = 0.5 * image.height
n_samples = int(duration * sample_rate)

time = np.linspace(0, duration, n_samples)
carrier = 1023 * np.sin(2 * np.pi * 2400 * time)

# Scale up the signal to match the carrier sample number
scale = n_samples // len(image_pixels)
signal = np.repeat(image_pixels, scale)

# Amplitude modulate the carrier with the 256-level signal
modulated = carrier * signal

# Resample the audio to the desired rate
sample_rate = output_sample_rate
n_samples = int(sample_rate * duration)
modulated = sps.resample(modulated, n_samples)

# Save the audio as a WAV file
modulated = modulated.astype(np.int16)
wav.write(audio_filepath, sample_rate, modulated)







    

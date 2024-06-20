from PIL import Image
import numpy as np
import math
from colorama import Fore      #For coloring the foreground
from colorama import Style    #For text style
from colorama import Back   #For coloring background


ASCII_CHARS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
# The characters in it are ordered from thinnest to boldest, which means darkest to 
# lightest for white text on a dark terminal background.
MAX_PIXEL_VALUE = 255


def get_pixel_matrix(img, height):
    img.thumbnail((height, 200))
    pixels = list(img.getdata())
    return [pixels[i:i+img.width] for i in range(0, len(pixels), img.width)]

def get_intensity_matrix(pixels_matrix, algo_name='average'):
    # Convert RGB matrix into brightnesss matrix
    # The brightness matrix will be the same shape and size as the RGB matrix, 
    # but each element will be a single value between 0 and 255 that represents 
    # the overall brightness of the pixel, instead of a tuple with 3 values for each 
    # of red, blue and green.
    # Basically conversion of rgb to black and white
    intensity_matrix = []
    for row in pixels_matrix:
        intensity_row = []
        for p in row:
            if algo_name == 'average':
                intensity = (p[0] + p[1] + p[2]) / 3.0
            elif algo_name == 'max_min':
                intensity = (max(p) + min(p)) / 2.0
            elif algo_name == 'luminosity':
                intensity = 0.21*p[0] + 0.72*p[1] + 0.07*p[2]
            elif algo_name == 'hsv':
                intensity = max(p)
            elif algo_name == 'hsp':
                intensity = math.sqrt(0.299*p[0]*p[0] + 0.587*p[1]*p[1] + 0.114*p[2]*p[2])
            else:
                raise Exception("Unrecognixed algo_name: %s" % algo_name)

            intensity_row.append(intensity)
        intensity_matrix.append(intensity_row)

    return intensity_matrix

def normalize_intensity_matrix(intensity_matrix):
    normalized_intensity_matrix = []
    max_pixel = max(map(max, intensity_matrix))
    min_pixel = min(map(min, intensity_matrix))
    for row in intensity_matrix:
        rescaled_row = []
        for p in row:
            r = MAX_PIXEL_VALUE * (p - min_pixel) / float(max_pixel - min_pixel)
            rescaled_row.append(r)
        normalized_intensity_matrix.append(rescaled_row)

    return normalized_intensity_matrix

# I fwe want to invert the image (Black to white)
def invert_intensity_matrix(intensity_matrix):
    inverted_intensity_matrix = []
    for row in intensity_matrix:
        inverted_row = []
        for p in row:
            inverted_row.append(MAX_PIXEL_VALUE - p)
        inverted_intensity_matrix.append(inverted_row)

    return inverted_intensity_matrix

# Convert brightness matrix to ascii matrix
def convert_to_ascii(intensity_matrix, ascii_chars):
    ascii_matrix = []
    for row in intensity_matrix:
        ascii_row = []
        for p in row:
            ascii_row.append(ascii_chars[int(p/MAX_PIXEL_VALUE * len(ascii_chars)) - 1])
        ascii_matrix.append(ascii_row)

    return ascii_matrix

def print_ascii_matrix(ascii_matrix, text_color):
#def print_ascii_matrix(ascii_matrix):
    for row in ascii_matrix:
        line = [p+p for p in row]     # Printing every character twice maintins shape
        print(Style.NORMAL +text_color + "".join(line)) # Foreground text
    print(Style.RESET_ALL)

filepath = "C:/Users/hp/Downloads/c1.jpeg"

img = Image.open(filepath)
pixels = get_pixel_matrix(img, 1000)

intensity_matrix = get_intensity_matrix(pixels, 'hsv')
#HSV is good for fluorescent or cell diagrams or faces
# Generally HSP gives the best results
intensity_matrix = normalize_intensity_matrix(intensity_matrix)
#intensity_matrix = invert_intensity_matrix(intensity_matrix)  #If you want to inverse the image


ascii_matrix = convert_to_ascii(intensity_matrix, ASCII_CHARS)
#print(Back.LIGHTCYAN_EX) #I added this line
print_ascii_matrix(ascii_matrix, Fore.BLUE)
#print_ascii_matrix(ascii_matrix)


#TRY K1 in yellow in hsv
#TRY S1 in green in max_min
#TRY c1 in blue in hsv
#TRY test8890 in cyan in hsp
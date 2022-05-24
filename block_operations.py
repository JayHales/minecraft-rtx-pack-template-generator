'''Functions for dealing with images of blocks'''
import string
import os
from PIL import Image


def convert_to_grey_scale(image: Image.Image) -> Image.Image:
    '''A function to convert an image into a non-weighted grey scale version on a single channel.'''
    grey_scale_image = Image.new('L', image.size)

    for y_pixel in range(image.size[1]):
        for x_pixel in range(image.size[0]):
            color_tuple = image.getpixel((x_pixel, y_pixel))

            grey_scale_image.putpixel((x_pixel, y_pixel), (color_tuple[0] + color_tuple[1] + color_tuple[2]) // 3)

    return grey_scale_image

def create_height_map(color_path: string, heightmap_path: string):
    '''A function to set the heightmap file for a given block on a path.'''
    color_image = Image.open(color_path)

    print(color_image.mode, color_path)

    if color_image.mode == 'P':
        color_image = color_image.convert('RGB')

    grey_scale_image = convert_to_grey_scale(color_image)

    total_color = 0
    
    for y_pixel in range(grey_scale_image.size[1]):
        for x_pixel in range(grey_scale_image.size[0]):

            if color_image.mode == 'RGBA':
                if not color_image.getpixel((x_pixel, y_pixel))[3] == 1:
                    continue

            total_color += grey_scale_image.getpixel((x_pixel, y_pixel))

    average_color_offset = 127 - total_color // (grey_scale_image.size[1] * grey_scale_image.size[0])

    for y_pixel in range(grey_scale_image.size[1]):
        for x_pixel in range(grey_scale_image.size[0]):
            new_color = grey_scale_image.getpixel((x_pixel, y_pixel)) + average_color_offset

            grey_scale_image.putpixel((x_pixel, y_pixel), new_color)

    if os.path.exists(heightmap_path):
        os.remove(heightmap_path)
    
    grey_scale_image.save(heightmap_path)








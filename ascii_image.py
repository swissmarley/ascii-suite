from PIL import Image, ImageDraw, ImageFont
from tkinter import Tk, Label, Button, Text, filedialog, StringVar, OptionMenu, Frame, Canvas, messagebox
import os
import math

chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]
charArray = list(chars)
charLength = len(charArray)
interval = charLength/256

scaleFactor = 0.09

oneCharWidth = 10
oneCharHeight = 18

def getChar(inputInt):
    return charArray[math.floor(inputInt*interval)]

file_path = filedialog.askopenfilename(title="Select an image file", filetypes=[
        ("PNG-Images", "*.png"),
        ("JPG/JPEG-Images", "*.jpg"),
        ("JPG/JPEG-Images", "*.jpeg"),
        ("GIF-Images", "*.gif"),
        ("Bitmap-Images", "*.bmp")
        ])

img = Image.open(file_path)
img = img.convert('RGB')

width, height = img.size
img = img.resize((int(scaleFactor*width), int(scaleFactor*height*(oneCharWidth/oneCharHeight))), Image.NEAREST)
width, height = img.size
pix = img.load()

# Extract the filename and extension from the input image path
filename, extension = os.path.splitext(os.path.basename(file_path))

# Create an output text file based on the image path
output_file_path = f"{filename}_output.txt"
text_file = open(output_file_path, "w")

outputImage = Image.new('RGB', (oneCharWidth * width, oneCharHeight * height), color = (0, 0, 0))
d = ImageDraw.Draw(outputImage)
fnt = ImageFont.load_default() 

for i in range(height):
    for j in range(width):
        r, g, b = pix[j, i]
        h = int(r/3 + g/3 + b/3)
        pix[j, i] = (h, h, h)
        text_file.write(getChar(h))
        d.text((j*oneCharWidth, i*oneCharHeight), getChar(h), font = fnt, fill = (r, g, b))

    text_file.write('\n')

output_image_path = f"{filename}_output.png"
outputImage.save(output_image_path)
text_file.close()

messagebox.showinfo("Success", f"ASCII art saved to {output_file_path}")
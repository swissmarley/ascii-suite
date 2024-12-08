import pyfiglet
from tkinter import Tk, Label, Button, Text, filedialog, StringVar, OptionMenu, Frame, Canvas, messagebox, Scale, colorchooser, HORIZONTAL
from PIL import Image, ImageTk
import tkinter as tk
from datetime import datetime
import os
import subprocess

loaded_image = None

current_font_size = 14

def text_to_ascii(input_text, ascii_style):
    ascii_art = pyfiglet.figlet_format(input_text, font=ascii_style)
    return ascii_art

def add_border(ascii_art, border_style):
    if border_style == "None":
        return ascii_art

    border_chars = {
        "Single Line": "+-|",
        "Double Line": "++||",
        "Dashed Line": "----",
        "Stars": "************",
        "Wavy Line": "~",
        "Hash Line": "###########",
        "Dotted Line": "···········",
        "Double Dot Line": "::::::::::",
    }

    lines = ascii_art.split('\n')
    if not lines or not lines[0]:
        return ascii_art

    border_top = border_chars[border_style][0] * (len(lines[0]) + 2) + '\n'
    
    if len(border_chars[border_style]) > 1:
        border_bottom = border_chars[border_style][1] * (len(lines[0]) + 2) + '\n'
    else:
        border_bottom = ""

    ascii_art_with_border = border_top + "\n".join("|" + line + "|" for line in lines) + border_bottom
    return ascii_art_with_border

def save_to_txt(ascii_art, style, border, font_size, font_color):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"output_{style.lower()}_{border.lower()}_{font_size}pt_{font_color}_{timestamp}.txt"
    
    with open(filename, 'w') as file:
        file.write(ascii_art)
    
    return filename

def set_font_size(value):
    global current_font_size
    current_font_size = int(value)
    update_preview()

def get_color_from_name(name):
    colors = {
        "black": "#000000",
        "red": "#FF0000",
        "green": "#00FF00",
        "blue": "#0000FF",
        "yellow": "#FFFF00",
        "purple": "#663399",
        "orange": "#DD6200",
        "cyan": "#71FFFF",
        "magenta": "#FF00FF",
        "white": "#FFFFFF",
    }
    return colors.get(name, "#000000")

def update_preview():
    input_text = input_entry.get("1.0", tk.END).strip()
    selected_ascii_style = ascii_style_var.get()
    selected_border_style = border_style_var.get()
    selected_font_color = font_color_var.get().lower()

    ascii_result = text_to_ascii(input_text, selected_ascii_style)

    ascii_result_with_border = add_border(ascii_result, selected_border_style)

    font_color = get_color_from_name(selected_font_color)

    preview_canvas.delete("all")
    preview_canvas.create_text(5, 5, anchor="nw", text=ascii_result_with_border, font=("Courier", current_font_size), fill=font_color)

    update_canvas()


def update_canvas():
    preview_canvas.update()

def execute_script():
    try:
        subprocess.run(["python3", "ascii_image.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")

def execute_cam_script():
    try:
        subprocess.run(["python3", "ascii_cam.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")

def convert_and_save():
    input_text = input_entry.get("1.0", tk.END).strip()
    selected_ascii_style = ascii_style_var.get()
    selected_border_style = border_style_var.get()

    ascii_result = text_to_ascii(input_text, selected_ascii_style)

    ascii_result_with_border = add_border(ascii_result, selected_border_style)

    font_color = get_color_from_name(font_color_var.get().lower())
    ascii_output.config(state=tk.NORMAL)
    ascii_output.delete("1.0", tk.END)
    ascii_output.insert(tk.END, ascii_result_with_border)
    ascii_output.tag_configure("colored", foreground=font_color)
    ascii_output.tag_add("colored", "1.0", "end")
    ascii_output.config(state=tk.DISABLED)

    filename = save_to_txt(ascii_result_with_border, selected_ascii_style, selected_border_style, current_font_size, font_color)
    messagebox.showinfo("Success", f"ASCII art saved to {filename}")

def create_font_slider():
    font_slider = Scale(root, from_=1, to=32, orient=HORIZONTAL, label="Font Size", length=200, command=set_font_size)
    font_slider.set(current_font_size)
    font_slider.pack()


def reset_fields():
    global loaded_image, image_label
    loaded_image = None
    image_label = None

    input_entry.delete("1.0", tk.END)
    preview_canvas.delete("all")
    ascii_output.config(state=tk.NORMAL)
    ascii_output.delete("1.0", tk.END)
    ascii_output.config(state=tk.DISABLED)


# GUI setup
root = Tk()
root.title("ASCII Art Suite")

ascii_styles = ["Standard", "Slant", "Script", "Doh", "Caligraphy", "Rectangles", "Big", "Small", "Shadow",
                "Shimrod", "SMSlant", "Speed", "ANSI_Shadow", "Sub-Zero", "Electronic", "Block", "Univers", "Ghost", "Epic",
                "Wavy", "Bulbhead", "Chiseled", "3D-ASCII", "Alpha", "Nipples", "Acrobatic", "Alligator2", "Impossible", 
                "Peaks", "Ticks", "Rev", "3-D", "Banner3-D", "Starwars", "Gothic", "Doom", "USAFlag"]
border_styles = ["None", "Single Line", "Double Line", "Dashed Line", "Stars", "Wavy Line", "Hash Line", "Dotted Line", "Double Dot Line"]

ascii_style_var = StringVar(root)
ascii_style_var.set(ascii_styles[0])  
ascii_style_menu = OptionMenu(root, ascii_style_var, *ascii_styles)
ascii_style_menu.pack()

border_style_var = StringVar(root)
border_style_var.set(border_styles[0])  
border_style_menu = OptionMenu(root, border_style_var, *border_styles)
border_style_menu.pack()

font_color_var = StringVar(root)
font_color_var.set("Black")  
font_color_label = Label(root, text="Font Color:")
font_color_label.pack()

font_color_menu = OptionMenu(root, font_color_var, "Black", "Red", "Green", "Blue", "Yellow", "Purple", "Orange", "Cyan", "Magenta", "White")
font_color_menu.pack()

preview_frame = Frame(root)
preview_frame.pack()

preview_canvas = Canvas(preview_frame, width=600, height=200)
preview_canvas.pack()

create_font_slider()

load_button = Button(root, text="Load Image and Convert", command=execute_script)
load_button.pack()

cam_button = Button(root, text="Start ASCII Webcam", command=execute_cam_script)
cam_button.pack()

image_label = None  

input_label = Label(root, text="Enter text:")
input_label.pack()

input_entry = Text(root, height=5, width=30)
input_entry.pack()

convert_button = Button(root, text="Convert and Save", command=convert_and_save)
convert_button.pack()

update_button = Button(root, text="Update Preview", command=update_preview)
update_button.pack()

reset_button = Button(root, text="Reset", command=reset_fields)
reset_button.pack()

ascii_output = Text(root, height=20, width=80, state=tk.DISABLED)
ascii_output.pack()

root.mainloop()

import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image, ImageTk

def select_file():
    file_path = tk.filedialog.askopenfilename(title="Select File")
    if file_path:
        file_name.set(os.path.basename(file_path))
    global fw
    fw = open(file_path, 'rb+')

def select_image():
    image_path = tk.filedialog.askopenfilename(title="Select Image")
    if image_path:
        image_name.set(os.path.basename(image_path))
    global image
    image = Image.open(image_path)
    image = image.resize((200,200), Image.ANTIALIAS)
    global photo
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)

def change_logo():
    # Read the file in binary mode
    data = fw.read()

    # Get the offset of the logo section
    logo_start = data[0x20]
    logo_len = data[0x21]
    logo_offset = 0x20 + logo_start
    logo_end = logo_offset + logo_len

    # Read new logo image
    new_logo_data = image.tobytes()

    # Replace the logo if the new one is not too long
    if len(new_logo_data) <= logo_len:
        data = data[:logo_offset] + new_logo_data + data[logo_end:]

        # Write the new data back to the file
        fw.seek(0)
        fw.write(data)

        with open("newfile.bin", "wb") as f:
            f.write(data)

        print('Logo changed successfully')
    else:
        print('Error: new logo is too long')

window = tk.Tk()
window.title('Logo Changer')

file_name = tk.StringVar()
tk.Label(window, text='File:', bg='lightblue').grid(row=0, column=0, sticky='w')
tk.Entry(window, textvariable=file_name, bg='lightgray').grid(row=0, column=1)

image_name = tk.StringVar()
tk.Label(window, text='Image:', bg='lightblue').grid(row=1, column=0, sticky='w')
tk.Entry(window, textvariable=image_name, bg='lightgray').grid(row=1, column=1)

tk.Button(window, text='Select File', command=select_file, bg='green').grid(row=0, column=2)
tk.Button(window, text='Select Image', command=select_image, bg='green').grid(row=1, column=2)

tk.Button(window, text='Change Logo', command=change_logo, bg='red').grid(row=2, column=1)

label = tk.Label(window, image=None, bg='lightblue')
label.grid(row=3, column=1)

window.mainloop()
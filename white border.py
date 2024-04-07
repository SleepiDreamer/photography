import tkinter as tk
from tkinter import filedialog, ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import os

# cd in the directory of this file
os.chdir(os.path.dirname(os.path.abspath(__file__)))	

# Create the main window
root = ThemedTk(theme="aqua")
root.title("White Border")
root.geometry("600x500")
# root.configure(bg="#DDDDDD")

global imgName, imgPil, imgTk, scale, aspect_ratio

aspect_ratio = 4/5

def store_image(name, image):
    # do sanity/validation checks here, if need be
    new_file_name = name
    image.save(new_file_name, "PNG")

# Create a function to open the file dialog and load the selected image
def open_image():
    global imgName, imgPil, imgTk, scale

    # Open the file dialog and get the selected file path
    file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg")])
    
    # Load the image using PIL
    imgPil = Image.open(file_path).convert("RGB")
    
    # Create a white border around the image
    width, height = imgPil.size
    scale = 1.0
    if maintain_aspect_ratio.get():
        new_width = int(width * scale)
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = int(height * scale)
        new_width = int(width + (new_height - height))
    img = Image.new("RGB", (new_width, new_height), "white")
    img.paste(imgPil, (int((new_width - width) / 2), int((new_height - height) / 2)))
    
    # Resize the image to a maximum height of 800 pixels
    if height > 800:
        scale_factor = 800 / new_height
        new_width2 = int(new_width * scale_factor)
        new_height2 = 800
        img = img.resize((new_width2, new_height2))
    
    imgTk = ImageTk.PhotoImage(img)
    label.config(image=imgTk)
    label.image = imgTk
    label.config(borderwidth=2, relief="ridge")
    
    # Save the image name for later use
    imgName = file_path

    edit_slider_minimum()
    update_image(None)

def save_image():
    # Check if an image has been loaded
    if not hasattr(label, "image"):
        return
    
    # Get the image from the label
    global imgPil
    image = imgPil

    # Create a white border around the image
    width, height = image.size
    if maintain_aspect_ratio.get():
        new_width = int(width * scale)
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = int(height * scale)
        new_width = int(width + (new_height - height))
    img = Image.new("RGB", (new_width, new_height), "white")
    img.paste(image, (int((new_width - width) / 2), int((new_height - height) / 2)))
    
    # save to whiteborder/ folder
    file_path = "whiteborder/" + imgName.split("/")[-1]
    print(file_path)
    
    # Save the image to the selected location
    store_image(file_path, img)


# Create a button to open the file dialog
button = ttk.Button(root, text="Open Image", command=open_image)
button.place(x=0, y=0, width=100, height=25)

# Create a button to save the image
saveButton = ttk.Button(root, text="Save Image", command=save_image)
saveButton.place(x=0, y=25, width=100, height=25)

# Create a label to display the image
label = ttk.Label(root)
label.place(x=0, y=50)

# Create a function to update the scale slider and entry
def update_scale(value):
    # Update the scale slider
    scaleSlider.set(value)

    # Update the scale entry
    scaleEntry.delete(0, tk.END)
    scaleEntry.insert(0, value)


# Create a function to update the scale entry and slider
def update_scale_entry(value):
    # Update the scale entry
    scaleEntry.delete(0, tk.END)
    scaleEntry.insert(0, round(value, 2))
    
    # Update the scale slider

# Create a scale slider to adjust the scale factor
scaleSlider = ttk.Scale(root, from_=1.0, to=2.0, orient=tk.HORIZONTAL, command=lambda x: [update_image(float(x)), update_scale_entry(float(x))])
scaleSlider.set(1.2)
scaleSlider.place(x=100, y=0, width=250)

scaleEntry = ttk.Entry(root, textvariable=scaleSlider)
scaleEntry.place(x=350, y=0, width=75)
scaleEntry.insert(0, 1.2)
scaleEntry.bind("<Return>", lambda event: update_scale(float(scaleEntry.get())))

def edit_slider_minimum():
    img_aspect_ratio = imgPil.size[0] / imgPil.size[1]
    min_aspect_ratio = max(img_aspect_ratio / aspect_ratio, 1.0)
    if (maintain_aspect_ratio.get()):
        scaleSlider.config(from_= min_aspect_ratio)
        scaleSlider.config(to = min_aspect_ratio * 2)
        if (float(scaleEntry.get()) < min_aspect_ratio):
            scaleSlider.set(min_aspect_ratio)
            scaleEntry.delete(0, tk.END)
            scaleEntry.insert(0, round(min_aspect_ratio, 2))
    else:
        scaleSlider.config(from_= 1.0)
        scaleSlider.config(to = 2.0)

def on_aspect_ratio_change(value):
    global aspect_ratio
    aspect_ratio = aspect_ratio_dict[value]

    edit_slider_minimum()
    update_image(None)

def on_maintain_aspect_ratio_change():
    edit_slider_minimum()
    update_image(None)

# aspect ratio dropdown
aspect_ratio_dict = {"dummy": 1.0, "2:3": 0.66666666, "3:2": 1.5, "3:4": 0.75, "4:3": 1.33, "4:5 (ig portrait)": 0.8, "5:4": 1.25, "1:1 (ig square)": 1.0, "16:9 ": 1.78, "9:16 (ig reel/story)": 0.56}
aspect_ratio_str = tk.StringVar(value="4:5 (ig portrait)")
aspect_ratio_dropdown = ttk.OptionMenu(root, aspect_ratio_str, *aspect_ratio_dict.keys(), command=on_aspect_ratio_change)
aspect_ratio_str.set("4:5 (ig portrait)")
aspect_ratio_dropdown.config(width=18)	
aspect_ratio_dropdown.place(x=425, y=0)

maintain_aspect_ratio = tk.BooleanVar(value=True)
scaleCheckbutton = ttk.Checkbutton(root, text="use aspect ratio", var=maintain_aspect_ratio, command=on_maintain_aspect_ratio_change)
scaleCheckbutton.place(x=425, y=28)


def update_image(new_scale):
    global imgPil, imgTk, scale

    # check if there's an image
    if not hasattr(label, "image"):
        return

    width, height = imgPil.size
    # Update the scale factor
    scale = scaleSlider.get()
    if maintain_aspect_ratio.get():
        scale *= aspect_ratio * height / width

    # Create a white border around the image
    if maintain_aspect_ratio.get():
        new_width = int(width * scale)
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = int(height * scale)
        new_width = int(width + (new_height - height))
    img = Image.new("RGB", (new_width, new_height), "white")
    img.paste(imgPil, (int((new_width - width) / 2), int((new_height - height) / 2)))
    
    # Resize the image to a maximum height of 800 pixels
    if height > 800:
        scale_factor = 800 / new_height
        new_width2 = int(new_width * scale_factor)
        new_height2 = 800
        img = img.resize((new_width2, new_height2))

    # Convert the image to a Tkinter PhotoImage and display it in a label
    imgTk = ImageTk.PhotoImage(img)
    label.config(image=imgTk)
    label.image = imgTk

    # update root geometry to fit the image
    root.geometry(str(max(new_width2 + 5, 570)) + "x" + str(new_height2 + 55))

# Start the main loop
root.mainloop()
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import os

# Set the desired aspect ratio
aspect_ratio = 4/5

# Create the main window
root = tk.Tk()
root.title("White Border")
root.geometry("800x500")

global imgName, imgPil, imgTk, scale

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
    
    # Save the image name for later use
    imgName = file_path

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
button = tk.Button(root, text="Open Image", command=open_image)
button.place(x=0, y=0, width=100, height=25)

# Create a button to save the image
saveButton = tk.Button(root, text="Save Image", command=save_image)
saveButton.place(x=0, y=25, width=100, height=25)

# Create a label to display the image
label = tk.Label(root)
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

scaleEntry = tk.Entry(root, textvariable=scaleSlider)
scaleEntry.place(x=350, y=0, width=75)
scaleEntry.bind("<Return>", lambda event: update_scale(float(scaleEntry.get())))

maintain_aspect_ratio = tk.BooleanVar(value=True)
scaleCheckbutton = tk.Checkbutton(root, text="maintain ratio", var=maintain_aspect_ratio, command=lambda: update_image(None))
scaleCheckbutton.place(x=425, y=0)


def update_image(new_scale):
    global imgPil, imgTk, scale
    
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
    if height > 1000:
        scale_factor = 1000 / new_height
        new_width2 = int(new_width * scale_factor)
        new_height2 = 1000
        img = img.resize((new_width2, new_height2))

    # Convert the image to a Tkinter PhotoImage and display it in a label
    imgTk = ImageTk.PhotoImage(img)
    label.config(image=imgTk)
    label.image = imgTk

    # update root geometry to fit the image
    root.geometry(str(new_width2) + "x" + str(new_height2 + 50))

# Start the main loop
root.mainloop()
import poke_api
import image_lib
from tkinter import *
from tkinter import ttk
import os
import ctypes

# Get the path of the script and its parent directory
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
image_cache_dir = os.path.join(script_dir, 'images')

# Make the image cache folder if it does not already exist
if not os.path.isdir(image_cache_dir):
    os.makedirs(image_cache_dir)

#Create the main window
root = Tk()
root.title("Poke Image Viewer")
root.minsize(100, 100)

# Set the window icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('COMP593.PokeImageViewer')
icon_path = os.path.join(script_dir , 'Poke-Ball.ico')
root.iconbitmap(icon_path)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#Create the Frame
frame = ttk.Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

#Add the image to Frame
image_poke = PhotoImage(file=os.path.join(script_dir, 'logo1.png'))
lbl_poke_image = ttk.Label(frame, image=image_poke)
lbl_poke_image.grid(row=0, column=0)

pokemon_name_list = sorted(poke_api.get_pokemon_names())
cbox_poke_names = ttk.Combobox(frame, values=pokemon_name_list, state='readonly')
cbox_poke_names.set("Select a Pokemon")
cbox_poke_names.grid(row=1, column=0, padx=10, pady=10)

def handle_pokemon_sel(event):
    # Get the name of the Selected Pokemon
    pokemon_name = cbox_poke_names.get()
    global image_path

    # Download and save the artwork for selected Pokemon
    image_path = poke_api.download_pokemon_artwork(pokemon_name, image_cache_dir)

    #Display the Pokemon artwork
    if image_path is not None:
        image_poke['file'] = image_path
    
cbox_poke_names.bind('<<ComboboxSelected>>', handle_pokemon_sel)

def set_desktop_wallpaper():
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

btn_set_desktop = ttk.Button(frame, text='Set as Desktop Wallpaper', command=set_desktop_wallpaper)
btn_set_desktop.grid(row=2, column=0, padx=10, pady=10)

root.mainloop()
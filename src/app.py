import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw
import sys
import os
import platform

def generate_gradient(colors, file_name):
    # Create a new blank image
    img = Image.new('RGB', (1920, 1080))
    draw = ImageDraw.Draw(img)
    
    # Get the coordinates and colors for the gradient
    top_left_color, top_right_color, bottom_left_color, bottom_right_color = colors
    
    for y in range(img.height):
        for x in range(img.width):
            # Calculate the ratio of the current pixel's position to the image dimensions
            xratio = x / img.width
            yratio = y / img.height
            
            # Linearly interpolate the colors
            r = int((1-xratio)*(1-yratio)*top_left_color[0] + xratio*(1-yratio)*top_right_color[0] + (1-xratio)*yratio*bottom_left_color[0] + xratio*yratio*bottom_right_color[0])
            g = int((1-xratio)*(1-yratio)*top_left_color[1] + xratio*(1-yratio)*top_right_color[1] + (1-xratio)*yratio*bottom_left_color[1] + xratio*yratio*bottom_right_color[1])
            b = int((1-xratio)*(1-yratio)*top_left_color[2] + xratio*(1-yratio)*top_right_color[2] + (1-xratio)*yratio*bottom_left_color[2] + xratio*yratio*bottom_right_color[2])
            
            # Set the pixel color
            draw.point((x, y), (r, g, b))
    
    # Save the image
    img.save(file_name)

    # Open the image with the default image viewer
    if platform.system() == "Windows":
        os.system(f'start {file_name}')
    elif platform.system() == "Darwin":
        os.system(f'open {file_name}')
    else:
        os.system(f'xdg-open {file_name}')

def update_color_preview(color_entry, preview_label):
    color_hex = color_entry.get()
    if len(color_hex) == 7 and color_hex.startswith('#'):
        preview_label.config(bg=color_hex)

def get_colors_and_filename():
    root = tk.Tk()
    root.title("Gradi3nt")
    root.geometry("300x210")
    root.iconbitmap('assets/icon.ico')

    color_entries = []
    color_previews = []
    for i in range(4):
        tk.Label(root, text=f"Color {i + 1} (hex format):").grid(row=i, column=0, padx=10, pady=10)
        color_entry = tk.Entry(root)
        color_entry.grid(row=i, column=1)
        color_entries.append(color_entry)

        color_preview = tk.Label(root, width=2, height=1)
        color_preview.grid(row=i, column=2)
        color_previews.append(color_preview)

        color_entry.bind('<KeyRelease>', lambda event, ce=color_entry, pl=color_preview: update_color_preview(ce, pl))

    def save():
        colors = []
        for color_entry in color_entries:
            color_hex = color_entry.get()
            colors.append(tuple(int(color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)))

        file_name = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("All files", "*.*")])
        if file_name:
            generate_gradient(colors, file_name)

    tk.Button(root, text="Generate Gradient", command=save).grid(row=4, columnspan=3, pady=(10,20))
    root.mainloop()

def main():
    if len(sys.argv) == 6:  # Check if there are four color arguments and one file name argument
        colors = [tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) for hex_color in sys.argv[1:5]]
        file_name = sys.argv[5]
        generate_gradient(colors, file_name)
    else:
        get_colors_and_filename()  # Launch the GUI if no command-line arguments are found

if __name__ == "__main__":
    main()
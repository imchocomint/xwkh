import json
import sys
import configparser
import tkinter as tk
from tkinter import ttk
import os 

def get_config_file():
    home_config_path = os.path.join(os.path.expanduser("~"), ".config", "xwkh", "config.ini")
    fallback_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "config.ini")
    
    if os.path.isfile(home_config_path):
        return home_config_path
    elif os.path.isfile(fallback_config_path):
        return fallback_config_path
    else:
        raise FileNotFoundError("Config file not found in both locations.")
#Load configuration from a file using configparser.
def load_config(config_file):

    config = configparser.ConfigParser()
    config.read(config_file)
    return config

#Load keybinds from a JSON file.
def load_keybinds(json_file):
    with open(json_file, "r") as file:
        return json.load(file)

#Display keybind data in a customizable window.
def display_keybinds(keybind_data, settings):

    # Tkinter root window setup
    root = tk.Tk()
    root.title("xwkh")

    width = settings["width"]  # Load width from settings
    height = settings["height"]  # Load height from settings
    root.geometry(f"{width}x{height}")  # Use the width and height from config
    root.resizable(False, False)

    # Set background color for the root window
    root.configure(bg=settings["background_color"])

    # Create styles for ttk widgets
    style = ttk.Style()
    style.configure("TFrame", background=settings["background_color"])  # Frame background style
    style.configure("TLabel", background=settings["background_color"], foreground=settings["font_color"])  # Label style
    style.configure("TScrollbar", background=settings["background_color"], troughcolor=settings["background_color"])  # Scrollbar style

    # Function to exit the application
    def exit_application(event):
        root.destroy()  # Close the Tkinter window

    # Bind the ESC key to the exit function
    root.bind('<Escape>', exit_application)


    # Create a scrollable frame
    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)  # Remove padding to avoid gaps

    # Create a Canvas and Scrollbar
    canvas = tk.Canvas(frame, bg=settings["background_color"], highlightthickness=0)
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    # Configure the scrollable frame
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Add the scrollable frame to the canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack canvas and scrollbar to frame
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Add keybinds to the scrollable frame
    for idx, (key, keybind) in enumerate(keybind_data["keybinds"].items(), start=1):
        keybind_label = ttk.Label(
            scrollable_frame,
            text=f"{keybind['keys']} | {keybind['description']}",
            font=(settings["font"], 10)
        )
        keybind_label.pack(anchor="w", pady=5)

    # Ensure the scrollable frame resizes correctly
    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Start the tkinter event loop
    root.mainloop()


def parse_args(json_files, default_json_index):
    """Parse command-line arguments to determine which JSON file to load."""
    json_file = None

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.startswith("-"):
            index = int(arg[1:]) - 1  # Convert CLI arg (-1, -2, etc.) to zero-based index
            if 0 <= index < len(json_files):
                json_file = json_files[index]
            else:
                print(f"Error: Invalid JSON file option '{arg}'. Defaulting...")

    if not json_file:
        json_file = json_files[default_json_index]

    return json_file  # Ensure it returns a filename, not a list



def main():
    """Main function to load configuration, keybinds, and display the GUI."""
    config_file = get_config_file()  # Retrieve config file path
    config = load_config(config_file)  # Load the configuration file

    default_file_index = int(config["OPTIONS"]["default_json_file"].strip())

    # Load keybinds JSON files
    json_files = [file.strip() for file in config["DEFAULT"]["json_files"].split(",")]
    
    json_files_combined = []
    for json_file in json_files:
        home_json_path = os.path.join(os.path.expanduser("~"), ".config", "xwkh", json_file)
        fallback_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "configs", json_file)

        if os.path.isfile(home_json_path):
            json_files_combined.append(home_json_path)
        elif os.path.isfile(fallback_json_path):
            json_files_combined.append(fallback_json_path)
    
    json_file = parse_args(json_files_combined, default_file_index)

    try:
        # Load the JSON file and extract settings
        keybind_data = load_keybinds(json_file)
        settings = {
            "background_color": config["DEFAULT"]["background_color"],
            "font": config["DEFAULT"]["font"],
            "font_color": config["DEFAULT"]["font_color"],
            "opacity": float(config["DEFAULT"]["opacity"].strip()),  # Ensure float conversion
            "width": int(config["DEFAULT"]["width"].strip()),  # Load width and convert to int # type: ignore
            "height": int(config["DEFAULT"]["height"].strip())  # Load height and convert to int
        
        }

        # Display the keybind viewer
        display_keybinds(keybind_data, settings)
    except FileNotFoundError:
        print(f"Error: JSON file '{json_file}' not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON file format.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()

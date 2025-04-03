import json
import sys
import configparser
import tkinter as tk
from tkinter import ttk


def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def load_keybinds(json_file):
    with open(json_file, "r") as file:
        return json.load(file)


def display_keybinds(keybind_data, settings):
    # Tkinter root window setup
    root = tk.Tk()
    root.title("xwkh")

    # Handle window size and appearance
    root.geometry("600x400")
    root.resizable(False, False)
    root["bg"] = settings["background_color"]
    root.attributes('-alpha', settings["opacity"])

    # Function to exit the application
    def exit_application(event):
        root.destroy()  # Close the Tkinter window

    # Bind the ESC key to the exit function
    root.bind('<Escape>', exit_application)

    # Display the message
    msg_label = ttk.Label(
        root,
        text=keybind_data["message"],
        foreground=settings["font_color"],
        background=settings["background_color"],
        anchor="center",
        font=(settings["font"], 12, "bold")
    )
    msg_label.pack(fill=tk.X, pady=10)

    # Create a scrollable frame
    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    canvas = tk.Canvas(frame, background=settings["background_color"])
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Add keybinds to the scrollable frame
    for idx, (key, keybind) in enumerate(keybind_data["keybinds"].items(), start=1):
        keybind_label = tk.Label(
            scrollable_frame,
            text=f"{idx}. {keybind['keys']} - {keybind['description']}",
            font=(settings["font"], 10),
            foreground=settings["font_color"],
            background=settings["background_color"],
            anchor="w"
        )
        keybind_label.pack(anchor="w", pady=5)

    # Start tkinter event loop
    root.mainloop()


def parse_args(config, default_json_index):
    """Parse command-line arguments to determine which JSON file to load."""
    # Get JSON file mappings
    json_files = config["DEFAULT"]["json_files"].split(",")
    json_file = None

    # Parse arguments to select JSON file
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
    
    return json_file


def main():
    """Main function to load configuration, keybinds, and display the GUI."""
    config_file = "config.ini"
    config = load_config(config_file)
    default_file_index = int(config["OPTIONS"]["default_json_file"])

    # Resolve the JSON file to load from CLI arguments or config
    json_file = parse_args(config, default_file_index)

    try:
        # Load the JSON file and extract settings
        keybind_data = load_keybinds(json_file)
        settings = {
            "background_color": config["DEFAULT"]["background_color"],
            "font": config["DEFAULT"]["font"],
            "font_color": config["DEFAULT"]["font_color"],
            "opacity": float(config["DEFAULT"]["opacity"])
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

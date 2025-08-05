import json
import sys
import configparser
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QScrollArea, QWidget, QVBoxLayout, QLabel, QGridLayout, QGraphicsOpacityEffect
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QEvent

def get_config_file():
    home_config_path = os.path.join(os.path.expanduser("~"), ".config", "xwkh", "config.ini")
    fallback_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "config.ini")
    
    if os.path.isfile(home_config_path):
        return home_config_path
    elif os.path.isfile(fallback_config_path):
        return fallback_config_path
    else:
        raise FileNotFoundError("Config file not found.")

def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def load_keybinds(json_file):
    with open(json_file, "r") as file:
        return json.load(file)

def exit(obj, event):
    if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
        obj.close()
        return True
    return False


def display_keybinds(keybind_data, settings):
    app = QApplication(sys.argv)
    
    window = QMainWindow()
    window.setWindowTitle("xwkh")
    
    width = settings["width"]
    height = settings["height"]
    window.setFixedSize(width, height)

    window.setStyleSheet(f"""
        QMainWindow {{
            background-color: {settings['background_color']};
        }}
    """)
    opacity = max(0.0, min(1.0, settings["opacity"]))    
    opacity_effect = QGraphicsOpacityEffect()
    opacity_effect.setOpacity(opacity) 
    window.setGraphicsEffect(opacity_effect)
    # window.setWindowOpacity(opacity)

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setStyleSheet("QScrollArea { border: none; }")


    scroll_content = QWidget()
    grid_layout = QGridLayout(scroll_content)
    grid_layout.setContentsMargins(10, 10, 10, 10)
    grid_layout.setSpacing(10)


    scroll_content.setStyleSheet(f"background-color: {settings['background_color']};")


    font = QFont(settings["font"], 10)
    row = 0
    for key, keybind in keybind_data["keybinds"].items():
        keys_label = QLabel(keybind['keys'])
        keys_label.setFont(font)
        keys_label.setStyleSheet(f"color: {settings['font_color']};")
        keys_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        description_label = QLabel(keybind['description'])
        description_label.setFont(font)
        description_label.setStyleSheet(f"color: {settings['font_color']};")
        description_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        description_label.setWordWrap(True)

        grid_layout.addWidget(keys_label, row, 0)
        grid_layout.addWidget(description_label, row, 1)
        row += 1

    grid_layout.setColumnStretch(1, 1)

    grid_layout.setRowStretch(row, 1)

    scroll_area.setWidget(scroll_content)
    
    window.setCentralWidget(scroll_area)
    window.eventFilter = lambda obj, event: exit(window, event)
    window.installEventFilter(window)

    window.show()
    app.exec()



def parse_args(json_files, default_json_index):
    json_file = None

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.startswith("-"):
            try:
                index = int(arg[1:]) - 1
                if 0 <= index < len(json_files):
                    json_file = json_files[index]
                else:
                    print(f"Error: Invalid JSON file option '{arg}'. Defaulting...")
            except ValueError:
                print(f"Error: Invalid argument format '{arg}'. Defaulting...")


    if not json_file:
        json_file = json_files[default_json_index]

    return json_file

def main():
    try:
        config_file = get_config_file()
        config = load_config(config_file)

        default_file_index = int(config["OPTIONS"]["default_json_file"].strip())

        json_files = [file.strip() for file in config["DEFAULT"]["json_files"].split(",")]
        
        json_files_combined = []
        for json_file in json_files:
            home_json_path = os.path.join(os.path.expanduser("~"), ".config", "xwkh", json_file)
            fallback_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "configs", json_file)

            if os.path.isfile(home_json_path):
                json_files_combined.append(home_json_path)
            elif os.path.isfile(fallback_json_path):
                json_files_combined.append(fallback_json_path)

        if not json_files_combined:
            raise FileNotFoundError("No valid JSON keybind files found.")
        
        selected_json_file = parse_args(json_files_combined, default_file_index)

        keybind_data = load_keybinds(selected_json_file)
        settings = {
            "background_color": config["DEFAULT"]["background_color"],
            "font": config["DEFAULT"]["font"],
            "font_color": config["DEFAULT"]["font_color"],
            "opacity": float(config["DEFAULT"]["opacity"].strip()),
            "width": int(config["DEFAULT"]["width"].strip()),
            "height": int(config["DEFAULT"]["height"].strip())
        }

        display_keybinds(keybind_data, settings)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON file format.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
import pygame_interface as ui

DEFAULT_SIZE = [100, 100]
DEFAULT_POS = [0, 0]
DEFAULT_COLOR = ui.get_color(255, 255, 255, 255)
DEFAULT_TEXT = "Default Text"
DEFAULT_FONT = ui.get_font("monospace", 20)

# GUI
gui_manager = ui.UI()  # Initialize UI manager

# Box
box = ui.Box()
box.pos = DEFAULT_POS
box.size = DEFAULT_SIZE
box.color = DEFAULT_COLOR
gui_manager.objects["Box 1"] = box

# Text Button
text_button = ui.Textbox(DEFAULT_FONT)
text_button.pos = DEFAULT_POS
text_button.size = DEFAULT_SIZE
text_button.text = DEFAULT_TEXT
text_button.color = DEFAULT_COLOR
gui_manager.objects["Text Button 1"] = text_button



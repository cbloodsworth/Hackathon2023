import pygame_interface as ui

from grid import *

# Fonts

# GUI
gui_manager = ui.UI()  # Initialize UI manager

# Start Game Button
start_game_btn = ui.Textbox()
start_game_btn.pos = screen_center
start_game_btn.size = [300, 100]
start_game_btn.text = "Begin Your Journey"
gui_manager.buttons["start_game_btn"] = start_game_btn

# Alert Text Box

alert_box = ui.Textbox()
alert_box.pos = [860, 150]
alert_box.size = [200, 120]
alert_box.enabled = False
gui_manager.objects["alert_box"] = alert_box

# Backpack Button
backpack_btn = ui.Textbox()
backpack_btn.pos = [900, 550]
backpack_btn.size = [120, 120]
backpack_btn.text = "Backpack"
backpack_btn.enabled = False
gui_manager.buttons["backpack_btn"] = backpack_btn

# Backpack Inventory
backpack_inventory = ui.Box()
backpack_inventory.pos = screen_center
backpack_inventory.size = [500, 500]
backpack_inventory.enabled = False
gui_manager.objects["backpack_inventory"] = backpack_inventory

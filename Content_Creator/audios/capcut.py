from keyboard import press_and_release
from time import sleep
import pyautogui
import keyboard



sleep(5)
#press_and_release('ctrl+i')
sleep(1)
keyboard.write('G:/Part-2/Exports/Templates/template1.mp4')
press_and_release('enter')
sleep(1)
# Set the initial position (start of the drag)
start_x, start_y = 243, 237  # Coordinates of the item you want to drag

# Set the target position (end of the drag)
end_x, end_y = 397, 825  # Coordinates where you want to drop the item

# Move the mouse to the starting position
pyautogui.moveTo(start_x, start_y)

# Click and hold the mouse button to start dragging
pyautogui.mouseDown()

# Move the mouse to the target position (dragging the item)
pyautogui.moveTo(end_x, end_y, duration=1)  # duration=1 for smooth dragging

# Release the mouse button to drop the item
pyautogui.mouseUp()#
#pyautogui.click(507,187)
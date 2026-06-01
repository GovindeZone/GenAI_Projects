import pyautogui
import time
import subprocess

file_name = "PyAutoGUI_Test.docx"

# Step 1
pyautogui.alert("Step 1: Start → Click OK and don't touch mouse/keyboard")
time.sleep(3)

# Step 2 - Open Word
pyautogui.alert("Step 2: Opening Microsoft Word")
subprocess.Popen("start winword", shell=True)
time.sleep(8)

# Step 3 - Type text
pyautogui.alert("Step 3: Typing text")
pyautogui.write("This is Pyautogui Test", interval=0.05)

# Step 4 - Save window
pyautogui.alert("Step 4: Opening Save window")
pyautogui.hotkey('ctrl', 's')
time.sleep(3)

# Step 5 - File name
pyautogui.alert("Step 5: Typing file name")
pyautogui.write(file_name, interval=0.05)
time.sleep(1)

# ✅ Step 6 - Go to Desktop (FIXED)
pyautogui.alert("Step 6: Moving to Desktop using keyboard")

pyautogui.hotkey('alt', 'd')   # Focus address bar
time.sleep(1)

pyautogui.write("Desktop")     # Just type Desktop (NOT full path)
pyautogui.press('enter')
time.sleep(2)

# Step 7 - Save
pyautogui.alert("Step 7: Saving file")
pyautogui.press('enter')
time.sleep(2)

# Close Word (optional)
pyautogui.hotkey('alt', 'f4')

pyautogui.alert("Completed: File saved on Desktop")
import pyautogui
import time
import webbrowser

# Open browser with Google
webbrowser.open("https://www.google.com")

# Wait for browser to load
time.sleep(5)

# Click search bar
pyautogui.click(x=759, y=458)

# Type search query
pyautogui.write("PBKS vs MI", interval=0.08)
pyautogui.press("enter")

# Wait for search results
time.sleep(4)

# Click first search result
pyautogui.click(x=721, y=418)

# Wait for page to open completely
time.sleep(3)

# Take screenshot
screenshot = pyautogui.screenshot()

# Save screenshot
screenshot.save("search_result.png")

print("Screenshot saved successfully.")
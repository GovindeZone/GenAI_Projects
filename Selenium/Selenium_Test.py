import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Launch browser
driver = webdriver.Chrome()
driver.maximize_window()

# Open website
driver.get("https://demoqa.com/automation-practice-form")

wait = WebDriverWait(driver, 10)

# -----------------------------
# Remove Ads / Overlay (Important for DemoQA)
# -----------------------------
driver.execute_script("document.body.classList.remove('ReactModal__Body--open')")

# -----------------------------
# Enter First Name
# -----------------------------
first_name = wait.until(EC.visibility_of_element_located((By.ID, "firstName")))
first_name.send_keys("Raja")

# -----------------------------
# Enter Last Name
# -----------------------------
driver.find_element(By.ID, "lastName").send_keys("Kumar")

# -----------------------------
# Select Gender (Radio Button)
# -----------------------------
gender = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[text()='Male']")))
gender.click()

# -----------------------------
# Select Hobbies (Checkbox)
# -----------------------------
driver.find_element(By.XPATH, "//label[text()='Sports']").click()
driver.find_element(By.XPATH, "//label[text()='Reading']").click()

# -----------------------------
# Scroll Down to State Dropdown
# -----------------------------
state = wait.until(EC.presence_of_element_located((By.ID, "state")))
driver.execute_script("arguments[0].scrollIntoView(true);", state)
time.sleep(1)

# -----------------------------
# Click State Dropdown
# -----------------------------
wait.until(EC.element_to_be_clickable((By.ID, "state"))).click()

# Select NCR
wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='NCR']"))).click()

# -----------------------------
# Click City Dropdown
# -----------------------------
city = wait.until(EC.element_to_be_clickable((By.ID, "city")))
driver.execute_script("arguments[0].scrollIntoView(true);", city)
time.sleep(1)

city.click()

# Select Delhi
wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Delhi']"))).click()

# -----------------------------
# Wait and Close
# -----------------------------
time.sleep(3)
driver.quit()
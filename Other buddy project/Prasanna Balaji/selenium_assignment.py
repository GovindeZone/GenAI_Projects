from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


# ----------------------------
# CONFIG
# ----------------------------

URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"

# Optional:
# service = Service("path/to/chromedriver")

driver = webdriver.Chrome()
driver.maximize_window()

wait = WebDriverWait(driver, 10)


try:
    # ----------------------------
    # OPEN WEBSITE
    # ----------------------------
    driver.get(URL)

    print("Opened SauceDemo")

    # ----------------------------
    # LOGIN
    # ----------------------------

    username_input = wait.until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )

    password_input = driver.find_element(By.ID, "password")

    login_button = driver.find_element(By.ID, "login-button")

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)

    login_button.click()

    print("Login submitted")

    # ----------------------------
    # VERIFY LOGIN SUCCESS
    # ----------------------------

    wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "title"))
    )

    page_title = driver.find_element(By.CLASS_NAME, "title").text

    assert page_title == "Products"

    print("Login successful")

    # ----------------------------
    # ADD PRODUCT TO CART
    # ----------------------------

    add_to_cart_btn = driver.find_element(
        By.ID,
        "add-to-cart-sauce-labs-backpack"
    )

    add_to_cart_btn.click()

    print("Product added to cart")

    # ----------------------------
    # VERIFY CART COUNT
    # ----------------------------

    cart_badge = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "shopping_cart_badge")
        )
    )

    assert cart_badge.text == "1"

    print("Cart badge verified")

    # ----------------------------
    # OPEN CART
    # ----------------------------

    cart_link = driver.find_element(
        By.CLASS_NAME,
        "shopping_cart_link"
    )

    cart_link.click()

    print("Opened cart")

    # ----------------------------
    # VERIFY PRODUCT IN CART
    # ----------------------------

    cart_item = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "inventory_item_name")
        )
    )

    assert cart_item.text == "Sauce Labs Backpack"

    print("Cart verification successful")

    # ----------------------------
    # CHECKOUT
    # ----------------------------

    checkout_btn = driver.find_element(By.ID, "checkout")
    checkout_btn.click()

    print("Checkout page opened")

    # ----------------------------
    # ENTER CUSTOMER INFO
    # ----------------------------

    driver.find_element(By.ID, "first-name").send_keys("John")
    driver.find_element(By.ID, "last-name").send_keys("Doe")
    driver.find_element(By.ID, "postal-code").send_keys("600001")

    driver.find_element(By.ID, "continue").click()

    print("Customer information submitted")

    # ----------------------------
    # FINISH ORDER
    # ----------------------------

    finish_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "finish"))
    )

    finish_btn.click()

    print("Order completed")

    # ----------------------------
    # VERIFY SUCCESS MESSAGE
    # ----------------------------

    success_msg = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "complete-header")
        )
    )

    assert success_msg.text == "Thank you for your order!"

    print("TEST PASSED")

    time.sleep(3)

except TimeoutException as e:
    print("Timeout occurred:", e)

except AssertionError as e:
    print("Assertion failed:", e)

except Exception as e:
    print("Unexpected error:", e)

finally:
    driver.quit()
    print("Browser closed")
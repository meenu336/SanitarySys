# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import unittest
# import time
# class LoginTest(unittest.TestCase):
#     def setUp(self):
#         self.driver = webdriver.Chrome()  # Initialize your WebDriver
#         self.driver.get("http://127.0.0.1:3000/login/")  # Replace with your login page URL

#     def test_valid_login(self):
#         username = "Mohan1"
#         password = "Mohan@1"

#         # Find username and password fields
#         username_field = WebDriverWait(self.driver, 30).until(
#             EC.presence_of_element_located((By.ID, "username"))  # Update with your username field locator
#         )
#         password_field = WebDriverWait(self.driver, 30).until(
#             EC.presence_of_element_located((By.ID, "password"))  # Update with your password field locator
#         )

#         # Enter username and password
#         username_field.send_keys(username)
#         password_field.send_keys(password)

#         # Trigger change events after entering username and password
#         self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", username_field)
#         self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", password_field)

#         # Find and click the login button
#         login_button = WebDriverWait(self.driver, 30).until(
#             EC.element_to_be_clickable((By.ID, "login-button"))  # Update with your login button locator
#         )
#         login_button.click()

#         # Add assertions to verify successful login
#         expected_url = "/home/"
#         self.assertIn(expected_url, self.driver.current_url)  # Update with assertion to check if expected_url is present in the current URL
#     def tearDown(self):
#         self.driver.quit()

# if __name__ == "__main__":
#     unittest.main()


# # from selenium import webdriver
# # from selenium.webdriver.common.keys import Keys
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC

# # # Set up the WebDriver (assuming Chrome here)
# # driver = webdriver.Chrome()
# # try:
# #     # Open the login page
# #     driver.get("http://127.0.0.1:3000/login/")  # Change the URL accordingly
    
# #     # Fill out the login form with sample data
# #     username_input = driver.find_element(By.NAME, "username")
# #     password_input = driver.find_element(By.NAME, "password")
# #     username_input.send_keys("ashok@gmail.com")
# #     password_input.send_keys("ashok")
    
# #     # Submit the login form
# #     driver.find_element(By.ID, "login-button").click()
    
# #     # Navigate to the add product page
# #     driver.get("http://127.0.0.1:3000/addproduct/")  # Change the URL accordingly
    
# #     # Fill out the form with sample data
# #     driver/

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import unittest

# class LoginAndAddToCartTest(unittest.TestCase):
#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.get("http://127.0.0.1:3000/login/")

#     def test_login_and_add_to_cart(self):
#         username = "Mohan1"
#         password = "Mohan@1"

#         # Find username and password fields, and perform login
#         username_field = WebDriverWait(self.driver, 30).until(
#             EC.presence_of_element_located((By.ID, "username"))
#         )
#         password_field = WebDriverWait(self.driver, 30).until(
#             EC.presence_of_element_located((By.ID, "password"))
#         )

#         username_field.send_keys(username)
#         password_field.send_keys(password)

#         # Trigger change events after entering username and password
#         self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", username_field)
#         self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", password_field)

#         login_button = WebDriverWait(self.driver, 30).until(
#             EC.element_to_be_clickable((By.ID, "login-button"))
#         )
#         login_button.click()

#         # Wait for the login process to complete and then move to the target page
#         WebDriverWait(self.driver, 30).until(
#             EC.url_matches("http://127.0.0.1:3000/home/")
#         )

#         # Navigate to the 'http://127.0.0.1:3000/shower/built-in/' page
#         self.driver.get("http://127.0.0.1:3000/shower/built-in/")

#         # Wait for the 'Add to Cart' button and click it
#         # add_to_cart_button = WebDriverWait(self.driver, 30).until(
#         #     EC.element_to_be_clickable((By.ID, "add-to-cart-button"))
#         # )
#         # add_to_cart_button.click()

#         # # Wait for the 'http://127.0.0.1:3000/cart/' page to load
#         # WebDriverWait(self.driver, 30).until(
#         #     EC.url_matches("http://127.0.0.1:3000/cart/")
#         # )

#         # # Interact with the 'product-name' element on the cart page
#         # product_name_element = WebDriverWait(self.driver, 30).until(
#         #     EC.presence_of_element_located((By.ID, "Showerzz"))
#         # )
#         # # Assuming you want to input some text in the 'product-name' field
#         # product_name_element.send_keys("showerzz")

#         # # You can perform further actions/assertions as needed

#     def tearDown(self):
#         self.driver.quit()

# if __name__ == "_main_":
#     unittest.main()

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # Set up the WebDriver (assuming Chrome here)
# driver = webdriver.Chrome()
# try:
#     # Open the login page
#     driver.get("http://127.0.0.1:3000/login/")  # Change the URL accordingly
    
#     # Fill out the login form with sample data
#     username_input = driver.find_element(By.NAME, "username")
#     password_input = driver.find_element(By.NAME, "password")
#     username_input.send_keys("ashok@gmail.com")
#     password_input.send_keys("ashok")
    
#     # Submit the login form
#     driver.find_element(By.ID, "login-button").click()
    
#     # Navigate to the add product page
#     driver.get("http://127.0.0.1:3000/addproduct/")  # Change the URL accordingly
    
#     # Fill out the form with sample data
#     driver.find_element(By.ID, "product-name").send_keys("dishower")
#     driver.find_element(By.ID, "category-name").send_keys("shower")
#     driver.find_element(By.ID, "subcategory-name").send_keys("Standalone shower")
#     driver.find_element(By.ID, "quantity").send_keys("12")
#     driver.find_element(By.ID, "description").send_keys("This is a test product description.")
#     driver.find_element(By.ID, "price").send_keys("100")
#     driver.find_element(By.ID, "discount").send_keys("10")
    
#     # Submit the form
#     driver.find_element(By.ID, "add-product-button").click()
    
#     # Open the view product page
#     driver.get("http://127.0.0.1:3000/viewproduct/")  # Change the URL accordingly

#     # Include the additional code snippet here

#     # # Wait for the search input to be present with increased timeout
#     #search_input = WebDriverWait(driver, 30).until(
#     #     EC.presence_of_element_located((By.CSS_SELECTOR, ".form-inline input.form-control"))
#     # )

#     # search_input.send_keys("Test Product")
#     # search_input.send_keys(Keys.RETURN)

#     # # Wait for the table to be present after search with increased timeout
#     # WebDriverWait(driver, 5).until(
#     #     EC.presence_of_element_located((By.XPATH, "//table[@class='table']"))
#     # )

# finally:
#     # Close the browser window
#     driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class LoginAndAddToCartTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:3000/login/")

    def test_login_and_add_to_cart(self):
        username = "Mohan1"
        password = "Mohan@1"

        # Find username and password fields, and perform login
        username_field = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_field = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "password"))
        )

        username_field.send_keys(username)
        password_field.send_keys(password)

        # Trigger change events after entering username and password
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", username_field)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", password_field)

        login_button = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.ID, "login-button"))
        )
        login_button.click()

        # Wait for the login process to complete and then move to the target page
        WebDriverWait(self.driver, 30).until(
            EC.url_matches("http://127.0.0.1:3000/home/")
        )

        # Navigate to the 'http://127.0.0.1:3000/shower/built-in/' page
        self.driver.get("http://127.0.0.1:3000/shower/built-in/")

        self.driver.get("http://127.0.0.1:3000/cart/")

        # Wait for the 'Add to Cart' button and click it
        # add_to_cart_button = WebDriverWait(self.driver, 30).until(
        #     EC.element_to_be_clickable((By.ID, "add-to-cart-button"))
        # )
        # add_to_cart_button.click()

        # # Wait for the 'http://127.0.0.1:3000/cart/' page to load
        # WebDriverWait(self.driver, 30).until(
        #     EC.url_matches("http://127.0.0.1:3000/cart/")
        # )

        # # Interact with the 'product-name' element on the cart page
        # product_name_element = WebDriverWait(self.driver, 30).until(
        #     EC.presence_of_element_located((By.ID, "Showerzz"))
        # )
        # # Assuming you want to input some text in the 'product-name' field
        # product_name_element.send_keys("showerzz")

        # # You can perform further actions/assertions as needed

    def tearDown(self):
        self.driver.quit()

if __name__ == "_main_":
    unittest.main()

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import unittest

# class LoginAndAddToCartTest(unittest.TestCase):
#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.get("http://127.0.0.1:3000/login/")

#     def test_login_and_add_to_cart(self):
#         username = "Mohan1"
#         password = "Mohan@1"

#         # Find username and password fields, and perform login
#         username_field = WebDriverWait(self.driver, 30).until(
#             EC.presence_of_element_located((By.ID, "username"))
#         )
#         password_field = WebDriverWait(self.driver, 30).until(
#             EC.presence_of_element_located((By.ID, "password"))
#         )

#         username_field.send_keys(username)
#         password_field.send_keys(password)

#         # Trigger change events after entering username and password
#         self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", username_field)
#         self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", password_field)

#         login_button = WebDriverWait(self.driver, 30).until(
#             EC.element_to_be_clickable((By.ID, "login-button"))
#         )
#         login_button.click()

#         # Wait for the login process to complete and then move to the target page
#         WebDriverWait(self.driver, 30).until(
#             EC.url_matches("http://127.0.0.1:3000/home/")
#         )

#         # Navigate to the 'http://127.0.0.1:3000/shower/built-in/' page
#         self.driver.get("http://127.0.0.1:3000/shower/built-in/")
#         showers_dropdown = WebDriverWait(self.driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//a[@id='showersDropdown']"))
#        )
#         showers_dropdown.click()

# # Click on the specific built-in shower product (replace this XPATH with your product's XPATH)
#         specific_product = WebDriverWait(self.driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'shower24')]"))
# )
#         specific_product.click()

# # Wait for the product detail page to load and find the 'Add to Cart' button
#         add_to_cart_button = WebDriverWait(self.driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add to Cart')]"))
# )
#         add_to_cart_button.click()

# # Wait for the cart operation to complete
#         WebDriverWait(self.driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//div[@class='cart-header']/h1[text()='Your Cart']"))
# )

# # Now navigate to the 'cart.html' page
#         self.driver.get("http://127.0.0.1:3000/cart.html")

# # Further actions/assertions on the cart page can be added here
# # For instance, you can locate elements on the cart page and perform interactions/assertions
# # Example:
# # cart_item = WebDriverWait(self.driver, 10).until(
# #     EC.presence_of_element_located((By.XPATH, "//li[@class='cart-item']"))
# # )
# # assert "shower24" in cart_item.text

#         # Wait for the 'Add to Cart' button and click it
#         # add_to_cart_button = WebDriverWait(self.driver, 30).until(
#         #     EC.element_to_be_clickable((By.ID, "add-to-cart-button"))
#         # )
#         # add_to_cart_button.click()

#         # # Wait for the 'http://127.0.0.1:3000/cart/' page to load
#         # WebDriverWait(self.driver, 30).until(
#         #     EC.url_matches("http://127.0.0.1:3000/cart/")
#         # )

#         # # Interact with the 'product-name' element on the cart page
#         # product_name_element = WebDriverWait(self.driver, 30).until(
#         #     EC.presence_of_element_located((By.ID, "Showerzz"))
#         # )
#         # # Assuming you want to input some text in the 'product-name' field
#         # product_name_element.send_keys("showerzz")

#         # # You can perform further actions/assertions as needed

# def tearDown(self):
#         self.driver.quit()

# if __name__ == "_main_":
#     unittest.main()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to perform login
def perform_login(driver, username, password):
    driver.get("http://127.0.0.1:3000/login/")  # Replace with your login URL

    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )

    username_field.send_keys(username)
    password_field.send_keys(password)

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login-button"))
    )
    login_button.click()

# Function to add a product to the cart
def add_product_to_cart(driver, product_name):
    # Replace 'your_url_here' with the actual URL of your built-in showers page
    driver.get("http://127.0.0.1:3000/shower/built-in/")

    try:
        product_cards = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-card"))
        )

        for product_card in product_cards:
            if product_name in product_card.text:
                add_to_cart_button = product_card.find_element(By.XPATH, "//button[@type='submit']")
                add_to_cart_button.click()
                break
       
        WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//your_cart_element_xpath"))
            )


        # Navigate to the cart.html page after adding the product to the cart
        driver.get("http://127.0.0.1:3000/cart.html")  # Replace with your cart URL

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
    finally:
        # Quit the driver
        driver.quit()

# Replace with your credentials
username = "Mohan1"
password = "Mohan@1"
product_name = "showerzz"  # Replace with the desired product name

# Initialize the Chrome driver
driver = webdriver.Chrome()

try:
    # Perform login
    perform_login(driver, username, password)

    # Add product to cart and navigate to the cart.html page
    add_product_to_cart(driver, product_name)

except Exception as e:
    print(f"Exception occurred: {str(e)}")
finally:
    # Quit the driver
    driver.quit()



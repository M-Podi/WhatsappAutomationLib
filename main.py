from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import pyperclip  # To handle clipboard operations
import os
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class WhatsAppWeb:
    def __init__(self, session_dir="whatsapp_session"):
        """
        Initializes the WhatsAppWeb class.

        :param session_dir: Directory to save browser session data.
        """
        self.session_dir = session_dir
        self.driver = None

        # Ensure the session directory exists
        if not os.path.exists(self.session_dir):
            os.makedirs(self.session_dir)

    def initialize_driver(self):
        """
        Initializes the Selenium WebDriver with automatic driver management and session persistence.
        """
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir={os.path.abspath(self.session_dir)}")

        # Uncomment the next line to run Chrome in headless mode
        # chrome_options.add_argument("--headless")

        # Automatically download and use the correct version of ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def open_whatsapp(self):
        """
        Opens WhatsApp Web in the browser.
        """
        if not self.driver:
            raise Exception("Driver not initialized. Call initialize_driver() first.")

        self.driver.get("https://web.whatsapp.com/")
        print("Please scan the QR code if required...")

        # Wait for successful login
        time.sleep(5)
        print("Logged in successfully!")

    def close(self):
        """
        Closes the WebDriver and browser.
        """
        if self.driver:
            self.driver.quit()
            print("Browser closed.")
        else:
            print("Driver not initialized.")

    def run(self):
        """
        Main function to initialize the driver, open WhatsApp Web, and manage the session.
        """
        try:
            self.initialize_driver()
            self.open_whatsapp()
        except Exception as e:
            print(f"An error occurred: {e}")

    def send_message(self, contact_name, message):
        """
        Searches for a contact, navigates to the chat, and sends a message.

        :param contact_name: The name of the contact to search for.
        :param message: The message to send to the contact (supports emojis via clipboard).
        """
        try:
            # Step 1: Find the search box (first instance of 'selectable-text')
            search_box = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "p.selectable-text.copyable-text"))
            )
            search_box.click()  # Activate the search box
            search_box.send_keys(contact_name + Keys.ENTER)  # Search for the contact and press ENTER

            print(f"Searching for contact: {contact_name}")

            # Step 2: Wait for the chat to load (the second input box will appear)
            message_box = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-placeholder="Type a message"]'))
            )

            # Step 3: Use clipboard to paste the message with emojis
            pyperclip.copy(message)  # Copy the message to the clipboard
            message_box.click()  # Ensure the message box is active
            message_box.send_keys(Keys.CONTROL, 'v')  # Paste the clipboard content
            message_box.send_keys(Keys.ENTER)  # Send the message
            print(f"Message sent to {contact_name}: {message}")
        except Exception as e:
            print(f"An error occurred while sending the message to {contact_name}: {e}")


    def send_media(self, contact_name, file_path):
        """
        Searches for a contact, navigates to the chat, and sends media (images, audio, documents).

        :param contact_name: The name of the contact to search for.
        :param file_path: The full path to the media file to send.
        """
        try:
            # Validate file existence
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"The file path does not exist: {file_path}")

            # Step 1: Search for the contact
            search_box = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@contenteditable='true'][@data-tab='3']")
                )
            )
            search_box.click()
            search_box.clear()
            search_box.send_keys(contact_name + Keys.ENTER)
            print(f"Searching for contact: {contact_name}")

            attachments = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Attach"]'))
            )
            attachments.click()


            image_box = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
                )
            )


            image_box.send_keys(os.path.abspath(file_path))

            send_button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Send"]'))
            )
            send_button.click()

        except Exception as e:
            print(f"An error occurred while sending the media to {contact_name}: {e}")

    def get_last_message_type(self, contact_name):
        """
        Navigates to a WhatsApp Web chat and identifies the type of the last received message.

        :param contact_name: Name of the contact or group to navigate to.
        :return: Prints and returns the type of the last received message.
        """
        try:
            # Step 1: Search for the contact
            search_box = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@contenteditable='true'][@data-tab='3']")
                )
            )
            search_box.click()
            search_box.clear()
            search_box.send_keys(contact_name + Keys.ENTER)
            print(f"Searching for contact: {contact_name}")
            time.sleep(3)  # Allow time for the chat to load

            # Step 2: Locate the last received message
            last_message = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class*='message-in']"))
            )[-1]

            # Step 3: Define detection logic for message types
            message_types = {
                "text": {
                    "selector": "span.selectable-text.copyable-text",
                    "action": lambda element: f"Text message: {element.text}",
                },
                "video": {
                    "selector": 'svg[data-icon="media-play"]',
                    "action": lambda element: "Video message",
                },
                "image": {
                    "selector": 'img[src^="blob:https://web.whatsapp.com"]',
                    "action": lambda element: "Image message",
                },
                "document": {
                    "selector": 'div[style*="background-image: url(\'blob:"]',
                    "action": lambda element: f"Document: {element.get_attribute('title')}",
                },
            }

            # Step 4: Identify the message type
            for msg_type, data in message_types.items():
                elements = last_message.find_elements(By.CSS_SELECTOR, data["selector"])
                if elements:
                    # Execute the action for the identified message type
                    result = data["action"](elements[0])
                    print(result)
                    return result

            # If no match, handle unknown message type
            print("Unknown message type")
            return "Unknown message type"

        except Exception as e:
            print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    whatsapp = WhatsAppWeb()
    whatsapp.run()

    whatsapp.get_last_message_type("John Doe")

    time.sleep(5)
    # Close the browser session
    whatsapp.close()


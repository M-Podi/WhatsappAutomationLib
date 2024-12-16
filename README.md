
# WhatsApp Web Automation Bot

A Python-based automation script using Selenium WebDriver to interact with WhatsApp Web. The bot can:
- Navigate to a specific chat.
- Identify the type of the last received message (text, image, video, document).
- Send media (images, videos, documents) and text messages to a contact or group.

## Requirements
- Python 3.7+
- Google Chrome (latest version)
- ChromeDriver (managed by `webdriver-manager`)

## Installation

1. **Clone the Repository**:

2. **Install Dependencies**:
   Install the required Python packages:
   ```bash
   pip install selenium webdriver-manager pyperclip
   ```

3. **Set Up ChromeDriver**:
   The script uses `webdriver-manager` to manage ChromeDriver automatically. Ensure your Chrome browser is up to date.

## Usage

### 1. Run the Script


### 2. Log In to WhatsApp Web
When prompted, scan the QR code using your mobile device.

### 3. Interact with the Bot
After logging in, use the bot to perform various tasks like sending messages and identifying the last message type.

### Example Functions

#### **Get Last Message Type**
```python
contact_name = "John Doe"
message_type = bot.get_last_message_type(contact_name)
print(f"Last message type: {message_type}")
```

#### **Send a Message**
```python
contact_name = "John Doe"
bot.send_message(contact_name, "Hello, how are you? 😊")
```

#### **Send Media**
```python
contact_name = "John Doe"
file_path = "/path/to/image.jpg"
bot.send_media(contact_name, file_path)
```

## Notes
- **Session Persistence**: The bot retains your session data (e.g., logged-in status) using Chrome's `user-data-dir`. You won't need to scan the QR code repeatedly unless you clear the session directory.
- **Selectors Maintenance**: WhatsApp Web's structure may change, requiring updates to element locators (XPath, CSS selectors).

## Troubleshooting
1. **ChromeDriver Version Error**:
   - Ensure your Chrome browser is up to date.
   - Delete cached drivers in `~/.wdm/` if issues persist.

2. **Element Not Found**:
   - WhatsApp Web's UI may have updated. Verify selectors using your browser's developer tools.

3. **Stale Element Exception**:
   - This occurs when an element is dynamically updated. Use explicit waits (`WebDriverWait`) to handle such scenarios.

## Future Enhancements
- Support for more message types (e.g., audio, stickers, location).
- Add functionality to reply to messages or handle group-specific tasks.


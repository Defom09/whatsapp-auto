import time
from flask import Flask, request, jsonify, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import webbrowser
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_messages', methods=['POST'])
def send_messages():
    try:
        # Retrieve numbers and message from the form
        numbers = request.form['numbers'].strip().split('\n')
        message = request.form['message']

        # Configure Chrome options to use Chromium in Render
        options = Options()
        options.add_argument("--start-maximized")  # Maximize the browser window
        options.binary_location = "/usr/bin/chromium"  # Path to Chromium binary in Render

        # Set up ChromeDriver service
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # Open WhatsApp Web
        driver.get("https://web.whatsapp.com/")
        print("Please scan the QR code on WhatsApp Web.")

        # Wait for QR code scanning
        WebDriverWait(driver, 600).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[3]/div/div[3]/header'))
        )
        print("QR code scanned successfully!")

        # Send messages to each number
        for number in numbers:
            number = number.strip()
            if not number:
                continue

            # Open the chat with the specified number
            driver.get(f"https://web.whatsapp.com/send?phone={number}&text={message}")
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )

            # Send the message
            driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]').send_keys(Keys.ENTER)
            time.sleep(2)  # Wait between sending messages

        driver.quit()
        return render_template('success.html')  # Show success page

    except Exception as e:
        print("An error occurred:", e)
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    # Automatically open the app in the default browser (for local usage, not necessary on Render)
    webbrowser.open("http://127.0.0.1:5000")
    
    # Get the port from the environment variable, default to 5000 if not set by Render
    port = int(os.getenv('PORT', 5000))
    
    # Run the app with the correct host and port for Render
    app.run(debug=True, host='0.0.0.0', port=port)

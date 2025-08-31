from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def check_whatsapp_login_status(driver):
    """Check if WhatsApp Web is already logged in"""
    try:
        # Wait for either QR code or chat interface
        WebDriverWait(driver, 10).until(
            lambda d: d.find_elements(By.CSS_SELECTOR, "canvas[aria-label='Scan me!']") or 
                     d.find_elements(By.CSS_SELECTOR, "[data-testid='chat-list']") or
                     d.find_elements(By.CSS_SELECTOR, "div[data-testid='intro-md-beta-logo-dark']")
        )
        
        # Check if already logged in (chat interface visible)
        if driver.find_elements(By.CSS_SELECTOR, "[data-testid='chat-list']"):
            print("✅ WhatsApp Web is already logged in!")
            return True
            
        # Check if QR code is present (not logged in)
        if driver.find_elements(By.CSS_SELECTOR, "canvas[aria-label='Scan me!']"):
            print("❌ WhatsApp Web requires QR code scan")
            return False
            
        # Check for intro screen (not logged in)
        if driver.find_elements(By.CSS_SELECTOR, "div[data-testid='intro-md-beta-logo-dark']"):
            print("❌ WhatsApp Web is on intro screen")
            return False
            
        return False
        
    except TimeoutException:
        print("⏰ Timeout checking WhatsApp login status")
        return False

def wait_for_whatsapp_login(driver, timeout=60):
    """Wait for user to scan QR code and login"""
    print(f"⏳ Waiting up to {timeout} seconds for WhatsApp login...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Check if chat list is now visible (logged in)
            if driver.find_elements(By.CSS_SELECTOR, "[data-testid='chat-list']"):
                print("✅ WhatsApp Web login successful!")
                return True
                
            # Check if still showing QR code
            if driver.find_elements(By.CSS_SELECTOR, "canvas[aria-label='Scan me!']"):
                print("📱 Please scan QR code with your phone...")
                time.sleep(3)
                continue
                
        except Exception as e:
            print(f"Error checking login status: {e}")
            
        time.sleep(2)
    
    print("❌ Login timeout - QR code not scanned in time")
    return False

def initialize_whatsapp_driver():
    """Initialize Chrome driver and navigate to WhatsApp Web"""
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=C:/WhatsAppData")  # Persist login
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    driver.get("https://web.whatsapp.com")
    
    # Check if already logged in
    if check_whatsapp_login_status(driver):
        return driver, True  # Already logged in
    else:
        # Wait for user to scan QR code
        login_success = wait_for_whatsapp_login(driver)
        return driver, login_success

def send_whatsapp_message(phone, message):
    """Send WhatsApp message with login detection"""
    driver = None
    try:
        driver, is_logged_in = initialize_whatsapp_driver()
        
        if not is_logged_in:
            print("❌ Failed to login to WhatsApp Web")
            return False
            
        # Format phone number
        if not phone.startswith('+'):
            phone = '+' + phone.replace(' ', '').replace('-', '')
            
        # Navigate to chat
        chat_url = f"https://web.whatsapp.com/send?phone={phone}&text={message}"
        driver.get(chat_url)
        
        # Wait for and click send button
        send_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='send']"))
        )
        send_button.click()
        
        # Update Django message status
        import requests
        try:
            requests.post('http://localhost:8000/update_message_status/', {
                'phone': phone,
                'status': 'sent'
            })
        except:
            pass  # Don't fail if Django not available
            
        print(f"✅ Message sent to {phone}")
        time.sleep(2)  # Brief pause between messages
        return True
        
    except Exception as e:
        print(f"❌ Error sending message to {phone}: {e}")
        return False
    finally:
        if driver:
            driver.quit()

# Example usage
if __name__ == "__main__":
    # Test the login detection
    driver, logged_in = initialize_whatsapp_driver()
    if logged_in:
        print("Ready to send messages!")
    else:
        print("Login failed or timeout")
    driver.quit()
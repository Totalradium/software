from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import urllib.parse

class WhatsAppBot:
    def __init__(self, browser='chrome'):
        import os
        
        if browser.lower() == 'edge':
            try:
                from selenium.webdriver.edge.options import Options as EdgeOptions
                options = EdgeOptions()
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                
                # Add user data directory for Edge
                user_data_dir = os.path.join(os.getcwd(), 'whatsapp_profile_edge')
                options.add_argument(f'--user-data-dir={user_data_dir}')
                options.add_argument('--profile-directory=Default')
                
                self.driver = webdriver.Edge(options=options)
            except Exception as e:
                print(f"Edge driver failed, falling back to Chrome: {e}")
                browser = 'chrome'  # Fallback to Chrome
            
        
        if browser.lower() != 'edge':  # Chrome (default or fallback)
            from selenium.webdriver.chrome.options import Options as ChromeOptions
            options = ChromeOptions()
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            # Add user data directory for Chrome
            user_data_dir = os.path.join(os.getcwd(), 'whatsapp_profile_chrome')
            options.add_argument(f'--user-data-dir={user_data_dir}')
            options.add_argument('--profile-directory=Default')
            
            self.driver = webdriver.Chrome(options=options)
        
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 30)
        
    def is_logged_in(self):
        """Check if user is logged into WhatsApp Web"""
        try:
            self.driver.get("https://web.whatsapp.com")
            time.sleep(8)  # Increased wait time
            
            # Check for QR code (not logged in)
            try:
                self.driver.find_element(By.XPATH, '//canvas[@aria-label="Scan me!"]')
                return False
            except:
                pass
            
            # Check for chat list (logged in)
            try:
                self.driver.find_element(By.XPATH, '//div[@data-testid="chat-list"]')
                return True
            except:
                return False
                
        except Exception as e:
            print(f"Error checking login status: {e}")
            return False
    
    def wait_for_qr_scan(self):
        """Wait for user to scan QR code"""
        print("Please scan the QR code in the browser...")
        try:
            # Wait for chat list to appear (login successful)
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="chat-list"]')))
            print("Login successful!")
            return True
        except:
            print("Login timeout or failed")
            return False
    
    def send_message(self, phone, message):
        """Send message to phone number"""
        try:
            # Clean phone number
            clean_phone = phone.replace('+', '').replace('-', '').replace(' ', '')
            
            # Create WhatsApp URL
            encoded_message = urllib.parse.quote(message)
            url = f"https://web.whatsapp.com/send?phone={clean_phone}&text={encoded_message}"
            
            self.driver.get(url)
            time.sleep(random.uniform(5, 8))  # Increased wait for chat loading
            
            # Try multiple send button selectors
            send_btn = None
            try:
                # New WhatsApp send button
                send_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send"]')))
            except:
                try:
                    # Alternative selector
                    send_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="wds-ic-send-filled"]')))
                except:
                    # Fallback selector
                    send_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]')))
            
            time.sleep(random.uniform(2, 3))  # Extra wait before clicking
            send_btn.click()
            
            print(f"✅ Message sent to {phone}")
            time.sleep(random.uniform(3, 5))  # Longer wait after sending
            return True
            
        except Exception as e:
            print(f"❌ Failed to send to {phone}: {e}")
            return False
    
    def send_file(self, phone, file_path, caption=""):
        """Send PDF or other file to phone number"""
        try:
            import os
            
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"❌ File not found: {file_path}")
                return False
            
            # Clean phone number
            clean_phone = phone.replace('+', '').replace('-', '').replace(' ', '')
            
            # Go to WhatsApp Web chat
            url = f"https://web.whatsapp.com/send?phone={clean_phone}"
            self.driver.get(url)
            time.sleep(random.uniform(5, 8))
            
            # Click attachment button
            attach_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@title="Attach"]')))
            attach_btn.click()
            time.sleep(2)
            
            # Click document option
            doc_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@accept="*"]')))
            doc_btn.send_keys(file_path)
            time.sleep(3)
            
            # Add caption if provided
            if caption:
                caption_box = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')))
                caption_box.send_keys(caption)
                time.sleep(1)
            
            # Send file
            send_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]')))
            send_btn.click()
            
            print(f"✅ File sent to {phone}: {os.path.basename(file_path)}")
            time.sleep(random.uniform(3, 5))
            return True
            
        except Exception as e:
            print(f"❌ Failed to send file to {phone}: {e}")
            return False
    
    def send_bulk_messages(self, phone_messages):
        """Send messages to multiple contacts"""
        success_count = 0
        for phone, message in phone_messages.items():
            if self.send_message(phone, message):
                success_count += 1
            time.sleep(random.uniform(4, 7))  # Longer delay between messages
        
        print(f"Sent {success_count}/{len(phone_messages)} messages successfully")
        return success_count
    
    def send_bulk_files(self, phone_files):
        """Send files to multiple contacts"""
        success_count = 0
        for phone, file_data in phone_files.items():
            file_path = file_data['path']
            caption = file_data.get('caption', '')
            if self.send_file(phone, file_path, caption):
                success_count += 1
            time.sleep(random.uniform(4, 7))
        
        print(f"Sent {success_count}/{len(phone_files)} files successfully")
        return success_count
    
    def close(self):
        """Close browser"""
        try:
            self.driver.quit()
        except:
            pass

# Test function
def test_whatsapp():
    bot = WhatsAppBot()
    
    try:
        if not bot.is_logged_in():
            if not bot.wait_for_qr_scan():
                print("Failed to login")
                return
        
        # Test message
        bot.send_message("+923001234567", "Test message from automation")
        
    finally:
        bot.close()

if __name__ == "__main__":
    test_whatsapp()
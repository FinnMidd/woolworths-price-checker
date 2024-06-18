import json
from playwright.sync_api import sync_playwright
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Function for getting prices from webpage
def get_price(url):
    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()
        
        try:
            page.goto(url)
            
            # Wait for dollar element to appear
            price_dollars_element = page.wait_for_selector('span.price-dollars')
            price_dollars = price_dollars_element.inner_text()
            
            # Wait for cents element to appear
            price_cents_element = page.wait_for_selector('span.price-cents')
            price_cents = price_cents_element.inner_text()
            
            # Combine price
            price = f"{price_dollars}.{price_cents}"
            
        # Error handling
        except Exception as e:
            print(f"Error: Failed to get price from {url}")
            print(e)
            price = None
        
        finally:
            browser.close()

    return price

# Function for loading items from JSON file
def load_items(filename='items.json'):
    with open(filename, 'r') as f:
        return json.load(f)

# Function for checking prices and running email function
def check_prices_and_notify():
    items = load_items()
    prices = set()
    price_changes = []
    
    for item in items:
        current_price = get_price(item['url'])
        if current_price is not None:
            prices.add(current_price)
        if current_price != item['price']:
            print(f"Price change detected for {item['name']}: {item['price']} -> {current_price}")
            item['price'] = current_price
            price_changes.append(f"{item['name']}: {item['price']} -> {current_price}")
    
    if price_changes:
        send_email_notification(price_changes)
    else:
        print("All prices match")

# Function for sending email
def send_email_notification(price_changes):
    # Email configuration
    smtp_server = 'smtp.gmail.com'  
    smtp_port = 465 
    smtp_user = os.environ.get('USER_EMAIL')  
    smtp_password = os.environ.get('USER_PASS')
    
    # Email content
    message = MIMEMultipart()
    message['From'] = smtp_user
    message['To'] = smtp_user
    message['Subject'] = 'Woolworths Price Change Detected'
    
    body = "The following price changes were detected:\n\n" + "\n".join(price_changes)
    message.attach(MIMEText(body, 'plain'))
    

    # Send email
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, smtp_user, message.as_string())
        print("Email notification sent successfully")
    except Exception as e:
        print(f"Failed to send email notification: {e}")
    finally:
        server.quit()

if __name__ == "__main__":
    check_prices_and_notify()

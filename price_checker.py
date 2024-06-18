import json
from playwright.sync_api import sync_playwright

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

def load_items(filename='items.json'):
    with open(filename, 'r') as f:
        return json.load(f)

def check_prices():
    items = load_items()
    prices = set()
    
    for item in items:
        current_price = get_price(item['url'])
        if current_price is not None:
            prices.add(current_price)
        if current_price != item['price']:
            print(f"Price change detected for {item['name']}: {item['price']} -> {current_price}")

if __name__ == "__main__":
    check_prices()

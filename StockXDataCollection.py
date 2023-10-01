import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DataError
import re
from StockXSQLSetup import engine, Product_Info
from ScrapingDriver import get_driver, Different_Agents


# Set up SQLAlchemy session
Session = sessionmaker(bind=engine) 
session = Session() 

# Choose a random User-Agent
random_agents = random.choice(Different_Agents)

# Initialize web driver by calling from get_driver function
driver = get_driver(random_agents)

# Define the list of StockX categories to scrape
stockx_url_bases = ['trading-cards', 'collectibles']
page_number = 1

# Generate a random interval to refresh the driver
random_interval = random.randint(5,30)
start_time = time.time()

# Iterate through the StockX categories
for stockx_url_base in stockx_url_bases:
    # Iterate through every page in StockX category
    for page_number in range(1,26):
        # Build the URL
        base_url = f'https://stockx.com/{stockx_url_base}?page='
        stockx_url = base_url + str(page_number)
        driver.get(stockx_url)

        # Extract link of every product on page
        product_link_frames = driver.find_elements(By.XPATH, '//a[@data-testid="RouterSwitcherLink"]')
        product_links = [link_elem.get_attribute('href') for link_elem in product_link_frames]
        
        # Loop through product links
        for index, product_link in enumerate(product_links):
            if index % random_interval == random.randrange(5,30) : # After every 5-30 driver requests (5-30 iterations of the loop)
                driver.quit()
                random_agents = random.choice(Different_Agents) # Changes the driver
                driver = get_driver(random_agents)  # Get a new driver with a different user agent
                random_interval = random.randint(5,30)
            # When visiting product page, spend a few seconds in order to mimic human behaivour
            driver.get(product_link)
            time.sleep(random.uniform(3, 5))

            # Extract product details
            product_details = driver.find_elements(By.XPATH, '//div[@data-component="product-trait"]')
            product_names = driver.find_elements(By.XPATH, '//div[@class="css-1r22s8j"]')
            product_descriptions = driver.find_elements(By.XPATH, '//h2[@class="css-1x1nv3c"]')
            product_dict = {} # Empty dictionary, information to be added to.

            # Loop through each product detail to add to dictionary
            for detail in product_details:
                # Extract the key and value from each product detail
                detail_key = detail.find_element(By.TAG_NAME, 'span').text
                detail_value = detail.find_element(By.TAG_NAME, 'p').text
                
                # Add detail_value to dictionary if detail_key exists in that 
                if detail_key == "Release Date":
                        product_dict['Release Date'] = detail_value # Adds Release Date
                elif detail_key == "Retail Price":
                    product_dict['Retail Price'] = detail_value # Adds Retail Price
                # If Release Year is only mentioned, mention the release date is the first day of release year.
                elif detail_key == "Year":
                    if '-' in detail_value: 
                        product_dict['Release Date'] = f'01/01/{detail_value[:4]}' 
                    else:
                        product_dict['Release Date'] = f'01/01/{detail_value}'

            # Attain Primary & Secondary Product Names (Product Name, Product Line)
            for name in product_names:
                product_line_element = name.find_element(By.XPATH, './h1')
                product_line = product_line_element.text

                # The secondary product title is the text within the nested span tag within the h1 tag
                product_name_element= product_line_element.find_element(By.XPATH, './span')
                product_name = product_name_element.text

                product_dict['Product Line'] = product_line.replace(product_name, '').strip()  # Removing the secondary title part from the primary to get the actual primary title
                product_dict['Product Name'] = product_name

            # If retail price isn't mentioned in product details, check product description paragraph
            if product_descriptions:
                for description in product_descriptions:
                    description_text = description.text
                    if '$' in description_text:
                        retail_price_text = re.search(r"\$\d+(?:,\d{3})*(?:\.\d{2})?", description_text).group()
                        retail_price = float(retail_price_text.replace('$','').replace(',',''))
                        product_dict['Retail Price'] = retail_price

            # Extract resale price information
            resale_price = driver.find_elements(By.XPATH, '//p[@class="chakra-text css-13uklb6"]')
            if resale_price:
                resale_price_text = resale_price[0].text.replace('$', '').replace(',', '')
                # Check if the string is a valid number
                if resale_price_text.replace('.', '', 1).isdigit():
                    resale_price_value = float(resale_price_text)  # Convert to float after validation
                    resale_price_usd = resale_price_value * 0.75
                    product_dict['Resale Price'] = resale_price_usd  # Assign to 'Resale Price' key in the dict
                else:
                    print(f"Warning: Invalid resale price found: {resale_price[0].text}")
                    
            # Further clean up retail price data in the dictionary
            if product_dict.get('Retail Price', None):
                product_dict['Retail Price'] = float(product_dict['Retail Price'].replace('$', '').replace(',', ''))

            # Insert Product Information instance to database
            if index > 0:
                product_instance = Product_Info(
                product_line=product_dict.get('Product Line', None),
                release_date=product_dict.get('Release Date', None),
                retail_price=product_dict.get('Retail Price', None),
                product_name=product_dict.get('Product Name', None),
                resale_price=product_dict.get('Resale Price', None)
                )
                try:
                    session.add(product_instance)
                    session.commit()

                    print(f"Inserted Information On {product_dict.get('Product Line', None)}, {product_dict.get('Product Name', None)}  to database.")
                except DataError as e:
                    print(f"An error occurred: {e}")

            # Navigate back to the previous page
            driver.back()
            # Monitor elapsed time to control request frequency
            end_time = time.time()
            elapsed_time = end_time - start_time
            # Between every 2-4 minutes, program will sleep for 3-5 minutes
            if elapsed_time > random.uniform(120, 240):
                time.sleep(random.randrange(180, 300))
                start_time = time.time()
            time.sleep(random.uniform(2,4))
            
            # Sleep the program for a longer period after an extended run
            if elapsed_time > random.uniform(1800, 7200):
                print("Program will now sleep for a while...")
                time.sleep(3600, 14400)
                start_time = time.time()
    # Close driver session once program task has been complete
    driver.close()

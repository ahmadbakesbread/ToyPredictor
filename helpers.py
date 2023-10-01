import re
import datetime
from bs4 import BeautifulSoup 
'''
The purpose of this function is to extract the year off of text.
This function searches for a 4-digit number between 1900 and the current year.
'''
def yearExtractor(text):
    current_year = datetime.datetime.now().year
    # Search for a pattern that resembles a year between 1900 and the current year.
    match = re.search(r'\b(19[0-9]{2}|200[0-9]|20[0-1][0-9]|202[0-{current_year%100}])\b', text)
    return int(match.group()) if match else None


'''
The purpose of this function is to extract the brand off of the product descriptions.
This function searches the product descriptions of the eBay product and checks for keyword 'Brand'
'''
def extractBrandName(description):
    # Define a regular expression pattern to match brand information
    brand_pattern = r'Brand:([^\\n]+)'

    # Use the re module to search for the pattern in the description
    match = re.search(brand_pattern, description, re.IGNORECASE)

    if match:
        return match.group(1).strip()  # Remove leading/trailing spaces

    return None # Returns None if no brand name is found.

'''
The purpose of this function is to extract the product details in one of the divs of product page on eBay.
'''
def extract_product_details(self, item_description):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(item_description, 'html.parser')

    # Find the relevant section with product information
    product_info_section = soup.find('section', class_='product-spectification')

    # Initialize variables to store product details
    brand_name = None
    # Add more variables for other details you want to extract

    # Extract brand name and other details if available
    if product_info_section:
        brand_div = product_info_section.find('div', class_='s-name', text='Brand')
        if brand_div:
            brand_name = brand_div.find_next('div', class_='s-value').text.strip()
        # Add more code to extract other details in a similar way

    return brand_name  # Return the extracted brand name

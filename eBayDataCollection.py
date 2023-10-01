from ebaysdk.finding import Connection as Finding
import datetime
from ebaysdk.exception import ConnectionError
import os
from dotenv import load_dotenv
from ebaySQLSetup import Product, Brand, Product_History, Category, engine
from sqlalchemy.orm import sessionmaker
from helpers import yearExtractor, extract_product_details

# Set up SQLAlchemy session for database operations
Session = sessionmaker(bind=engine)
session = Session()

# Load environment variables from .env file
load_dotenv()

# Retrieve the eBay API key from environment variables
api_key = os.getenv('api_key')

# Define a mapping between product categories and search keywords
product_dictmapping = {'Trading Cards': ('One Piece', 'Yu-Gi-Oh', 'Pokemon'), 'Collectibles': ('Funko', 'Mattel', 'Lego')}

class eBayConnection:
    def __init__(self, api_key):
        # Initialize the class with the provided API key
        self.api_key = api_key

    def fetch(self):
        """
        Fetch products from eBay based on predefined categories and keywords.
        Extract relevant details from the fetched data and store them in a database.
        """
        try:
            # Create an instance of the eBay Finding API with the provided API key
            finding_api = Finding(appid=self.api_key, config_file=None)
            databaseItems = []  # List to hold items to be inserted into the database

            # Iterate over each category and keyword combination for product search
            for category, keywords in product_dictmapping.items():
                for keyword in keywords:
                    max_requests = 1000
                    request_count = 0  # Count the number of API requests made
                    i = 0
                    while i < 10:
                        # Execute the eBay 'findItemsAdvanced' API call with the current keyword
                        finding_response = finding_api.execute('findItemsAdvanced', {
                            'keywords': keyword,
                            'paginationInput': {'entriesPerPage': 100, 'pageNumber': i + 1}
                        })

                        print(f"Response: {finding_response.reply.ack}")

                        # Check if the API response contains items and was successful
                        if hasattr(finding_response.reply.searchResult, 'item') and finding_response.reply.ack == 'Success':
                            print(f"Items found: {len(finding_response.reply.searchResult.item)}")
                            assert finding_response.reply.ack == 'Success'

                            # Iterate over each item in the response to extract details
                            for item in finding_response.reply.searchResult.item:
                                release_year = yearExtractor(item.title)
                                if not release_year and hasattr(item, 'description'):
                                    release_year = yearExtractor(item.description)

                                # Extract brand name from HTML description or use the item title as a fallback
                                brand_name = item.title or (extract_product_details(item.description) if hasattr(item, 'description') else None)

                                # Construct a dictionary with the extracted product details
                                product_dict = {
                                    'title': item.title,
                                    'price': item.sellingStatus.currentPrice.value,
                                    'category': item.primaryCategory.categoryName,
                                    'listed_date': item.listingInfo.startTime,
                                    'release_date': release_year,
                                    'brand': brand_name
                                }

                                # Create instances for product, brand, category, and product history
                                product_history_instance = Product_History(
                                    date_listed=product_dict.get('listed_date'),
                                    manufactured_date=product_dict.get('release_date')
                                )
                                product_category_instance = Category(name=product_dict.get('category'))
                                brand_instance = Brand(name=brand_name)
                                ebay_product_instance = Product(
                                    product_name=product_dict.get('title'),
                                    price=float(product_dict.get('price')),
                                    brand=brand_instance
                                )

                                # Append the instances to their respective relationships
                                ebay_product_instance.product_histories.append(product_history_instance)
                                ebay_product_instance.category.append(product_category_instance)

                                # Add the product instance to the list of items to be inserted into the database
                                databaseItems.append(ebay_product_instance)
                                i += 1
                                print(f"Inserted Product Information On:\n{product_dict.get('title')}")
                                request_count += 1  # Increment request count

                            # Assert certain expected data types for quality control
                            assert isinstance(finding_response.reply.timestamp, datetime.datetime)
                            assert isinstance(finding_response.reply.searchResult.item, list)
                            assert isinstance(finding_response.dict(), dict)

                        else:
                            print("No items found.")

                        # Check if the API request limit has been reached
                        if request_count >= max_requests:
                            print("Reached API rate limit for the day.")
                            break

            # If there are items to be inserted, add them to the database
            if len(databaseItems) > 0:
                session.bulk_save_objects(databaseItems)
                session.commit()
                print(f"Inserted {len(databaseItems)} items to the database.")

        # Handle connection errors and print the error details
        except ConnectionError as e:
            print(e)
            print(e.response.dict())

# Entry point of the script
if __name__ == '__main__':
    e = eBayConnection(api_key)  # Create an instance of the eBayConnection class
    e.fetch()  # Fetch and process the eBay product data

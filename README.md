# 🚀 ToyPredictor

Welcome to **ToyPredictor**! This project aims to predict the resale value of toys using machine learning. Currently, I'm in the data engineering phase, collecting and processing data from platforms like eBay and StockX.

## 🎯 Features

- **Data Collection**: Automated scripts to scrape product data from eBay and StockX.
- **Database Setup**: SQL setup scripts to structure and store the collected data.
- **Notification Handling**: A Flask application to handle post requests and acknowledge notifications from eBay.

## 📂 Repository Structure

- **[ScrapingDriver.py](https://github.com/ahmadbakesbread/ToyPredictor/blob/main/ScrapingDriver.py)**: Sets up the web scraping driver with randomized user-agent headers.
- **[StockXDataCollection.py](https://github.com/ahmadbakesbread/ToyPredictor/blob/main/StockXDataCollection.py)**: Scrapes product data from StockX and stores in the database.
- **[StockXSQLSetup.py](https://github.com/ahmadbakesbread/ToyPredictor/blob/main/StockXSQLSetup.py)**: Defines the SQL database structure for StockX data.
- **[eBayDataCollection.py](https://github.com/ahmadbakesbread/ToyPredictor/blob/main/eBayDataCollection.py)**: Fetches product data from eBay using the eBay SDK.
- **[ebaySQLSetup.py](https://github.com/ahmadbakesbread/ToyPredictor/blob/main/ebaySQLSetup.py)**: Sets up the SQL database structure for eBay data.
- **[helpers.py](https://github.com/ahmadbakesbread/ToyPredictor/blob/main/helpers.py)**: Utility functions for data extraction and processing.
- **[postRequests.py](https://github.com/ahmadbakesbread/ToyPredictor/blob/main/postRequests.py)**: Flask app to handle post requests from eBay.

## 🚧 Under Development

- **Optimize Code**: Plans to make the data collection and processing faster.
- **Machine Learning Model**: The next phase involves building and training a machine learning model to predict toy resale values.

## ⭐ Future Goals

- Optimize the code to make it faster.
- Implement scheduled API fetches to retrieve data on specific products at designated times. 
- Begin the development of the machine learning model.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/ahmadbakesbread/ToyPredictor/issues) if you want to contribute.

#### 🐞 Known Bugs

- **Data Parsing Issues**: While collecting data from eBay and StockX, there are instances where the release date of a product isn't parsed correctly. This is due to the limited cases considered during the parsing process.

---

Thank you for checking out **ToyPredictor**. Happy coding! 🎉


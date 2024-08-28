# **Stock Bud**

## **Overview**

**Stock Bud** is a Python-based web application designed to provide users with comprehensive insights into stock performance. This tool allows users to input a stock ticker symbol and receive detailed information, including financial ratios, historical performance charts, and recent news sentiment analysis. The application is built using the powerful combination of **Streamlit** for the frontend, **yfinance** for data retrieval, and **Plotly** for interactive data visualization.

## **Key Features**

- **Stock Data**: Fetches up-to-date stock information including current price, market cap, P/E ratio, and more using the `yfinance` library.
- **Flexible Time Interval Analysis**: Users can view stock performance over various time intervals, such as daily, weekly, monthly, year-to-date, and multi-year periods. The performance is visualized using interactive candlestick charts provided by **Plotly**.
- **Sentiment Analysis**: Analyzes recent news headlines related to the selected stock using **Natural Language Processing (NLP)** with the `nltk` library, providing an overall sentiment score.
- **Data Visualization**: The application leverages **Plotly** to create dynamic, interactive charts that allow users to explore historical stock data in detail.
- **Responsive and Interactive UI**: Built with **Streamlit**, the application provides an intuitive, user-friendly interface that is both interactive and responsive, making it accessible on various devices.

## **Technical Highlights**

- **Python**: The backbone of the application, used for data retrieval, processing, and visualization. The application demonstrates strong proficiency in Python for data-driven application development.
- **Data Processing**: Efficiently handles data fetching, processing, and formatting from financial APIs like `yfinance`. The application processes large datasets to compute financial ratios and generates insights in real time.
- **Data Visualization**: Employs **Plotly** to create rich, interactive charts that visualize stock performance over selected time frames. The use of candlestick charts offers a clear view of market trends and stock volatility.
- **NLP with NLTK**: Integrates sentiment analysis using the VADER model from the `nltk` library, processing recent news articles to gauge market sentiment and its potential impact on stock performance.

## **Getting Started**

### **Prerequisites**

- **Python 3.7+**: Make sure Python is installed on your machine.
- **pip**: Ensure `pip` is installed to manage Python packages.

### **Installation**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/stock-bud.git
   cd stock-bud
   ```

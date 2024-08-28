import yfinance as yf
import streamlit as st
import nltk
import pprint
import pandas as pd
import plotly.graph_objs as go

nltk.download("vader_lexicon")
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def create_performance_chart(ticker, period, interval):
    df = yf.download(ticker, period=period, interval=interval)

    # Create a candlestick chart using Plotly
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                         open=df["Open"],
                                         high=df["High"],
                                         low=df["Low"],
                                         close=df["Close"])])

    fig.update_layout(
        title=f"{ticker} Performance ({period.capitalize()})",
        yaxis_title="Price (USD)",
        xaxis_title="Date",
        xaxis_rangeslider_visible=False
    )

    return fig

def get_news_sentiment(news_articles):
    sia = SentimentIntensityAnalyzer()
    
    sentiment_score = 0
    for article in news_articles:
        sentiment = sia.polarity_scores(article["title"])
        sentiment_score += sentiment["compound"]  
    return sentiment_score

def getTicker(ticker):
    return yf.Ticker(ticker)

def get_stock_news_yahoo(ticker, num):
    news_data = ticker.news
    return news_data[:num]

def extract_thumbnail_url(article):
    thumbnail_resolutions = article.get("thumbnail", {}).get("resolutions", [])
    return thumbnail_resolutions[-1]["url"] if thumbnail_resolutions else "https://via.placeholder.com/150"

def get_info(ticker):
    stock_info = ticker.info
    pprint.pprint(stock_info)
    currPrice = stock_info.get("currentPrice", stock_info.get("bid",0))
    info = {
        "p_e_ratio": stock_info.get("forwardPE", 0.0),
        "p_b_ratio": stock_info.get("priceToBook", 0.0),
        "roe": stock_info.get("returnOnEquity", 0.0),
        "profit_margin": stock_info.get("profitMargins", 0.0),
        "current_ratio": stock_info.get("currentRatio", 0.0),
        "quick_ratio": stock_info.get("quickRatio", 0.0),
        "summary": stock_info.get("longBusinessSummary", ""),
        "short_name": stock_info.get("shortName", ""),
        "symbol": stock_info.get("symbol",""),
        "current_price": currPrice,
        "previous_close": stock_info.get("previousClose",0)
    }
    return info

def create_sidebar(sentiment, news):
    coloured_sentiment = f":red[Negative]"
    if sentiment > 0:
        coloured_sentiment = f":green[Positive]"
    elif sentiment == 0:
        coloured_sentiment = f":orange[Neutral]"

    st.sidebar.subheader("Recent News & Sentiment")
    st.sidebar.write(f"**Overall Sentiment:** {coloured_sentiment}")
    st.sidebar.subheader("Recent News")
    for article in news:
        thumbnail_url = extract_thumbnail_url(article)
        st.sidebar.markdown(
            f"""
            <div style="display: flex; align-items: center;">
                <img src="{thumbnail_url}" width="50" style="margin-right: 10px;">
                <a href="{article["link"]}" target="_blank">{article["title"]}</a>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.sidebar.write("---")

def create_summary_table(values):
    # Unpack values
    previous_close, open_price, bid, ask, days_range, week_52_range, volume, avg_volume, \
    market_cap, beta, pe_ratio, eps, earnings_date, dividend_yield, ex_dividend_date, target_est = values
    
    # HTML and CSS for the table
    html_table = f"""
    <style>
        .summary-table {{
            width: 100%;
            max-width: 100%;
            table-layout: fixed;
            word-wrap: break-word;
            border-collapse: collapse;
        }}
        .summary-table td {{
            padding: 8px;
            border: 1px solid #ddd;
        }}
    </style>
    <table class="summary-table">
        <tr>
            <td><strong>Previous Close</strong></td>
            <td>{previous_close}</td>
            <td><strong>Market Cap</strong></td>
            <td>{market_cap}</td>
        </tr>
        <tr>
            <td><strong>Open</strong></td>
            <td>{open_price}</td>
            <td><strong>Beta (5Y Monthly)</strong></td>
            <td>{beta}</td>
        </tr>
        <tr>
            <td><strong>Bid</strong></td>
            <td>{bid}</td>
            <td><strong>PE Ratio (TTM)</strong></td>
            <td>{pe_ratio}</td>
        </tr>
        <tr>
            <td><strong>Ask</strong></td>
            <td>{ask}</td>
            <td><strong>EPS (TTM)</strong></td>
            <td>{eps}</td>
        </tr>
        <tr>
            <td><strong>Day"s Range</strong></td>
            <td>{days_range}</td>
            <td><strong>Earnings Date</strong></td>
            <td>{earnings_date}</td>
        </tr>
        <tr>
            <td><strong>52 Week Range</strong></td>
            <td>{week_52_range}</td>
            <td><strong>Forward Dividend & Yield</strong></td>
            <td>{dividend_yield}</td>
        </tr>
        <tr>
            <td><strong>Volume</strong></td>
            <td>{volume}</td>
            <td><strong>Ex-Dividend Date</strong></td>
            <td>{ex_dividend_date}</td>
        </tr>
        <tr>
            <td><strong>Avg. Volume</strong></td>
            <td>{avg_volume}</td>
            <td><strong>1y Target Est</strong></td>
            <td>{target_est}</td>
        </tr>
    </table>
    """
    
    return html_table


def get_stock_data(stock):    
    # Fetching the required data
    previous_close = stock.info.get("previousClose", "N/A")
    open_price = stock.info.get("open", "N/A")
    bid = stock.info.get("bid", "N/A")
    ask = stock.info.get("ask", "N/A")
    days_range = f"{stock.info.get("dayLow", "N/A")} - {stock.info.get("dayHigh", "N/A")}"
    week_52_range = f"{stock.info.get("fiftyTwoWeekLow", "N/A")} - {stock.info.get("fiftyTwoWeekHigh", "N/A")}"
    
    volume = stock.info.get("volume", "N/A")
    if volume != "N/A":
        volume = f"{volume:,}"

    avg_volume = stock.info.get("averageVolume", "N/A")
    
    # Format Market Cap with commas
    market_cap = stock.info.get("marketCap", "N/A")
    if market_cap != "N/A":
        market_cap = f"{market_cap:,}"
    
    beta = stock.info.get("beta", "N/A")
    pe_ratio = stock.info.get("trailingPE", "N/A")
    eps = stock.info.get("trailingEps", "N/A")
    earnings_date = stock.info.get("earningsDate", "N/A")
    dividend_yield = f"{stock.info.get("dividendRate", 0)} ({stock.info.get("dividendYield", 0) * 100}%)"
    ex_dividend_date = stock.info.get("exDividendDate", "N/A")
    target_est = stock.info.get("targetMeanPrice", "N/A")
    
    # Formatting the earnings date and ex-dividend date
    if isinstance(earnings_date, tuple):
        earnings_date = f"{earnings_date[0].date()} - {earnings_date[1].date()}" if len(earnings_date) == 2 else "N/A"
    else:
        earnings_date = earnings_date.date() if earnings_date != "N/A" else "N/A"

    
    values = [
        previous_close, open_price, bid, ask, days_range, week_52_range, volume, avg_volume, 
        market_cap, beta, pe_ratio, eps, earnings_date, dividend_yield, ex_dividend_date, target_est
    ]
    
    return values



st.set_page_config(
    page_title="Stock Bud",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded", 
)

st.title("Stock Bud")

# Ticker symbol input form
ticker = st.text_input("Enter Stock Ticker", "")

if ticker:
    curr_ticker = getTicker(ticker)
    if curr_ticker:
        info = get_info(curr_ticker)
        
        st.subheader(f"**{info.get("short_name", "")}** ({info.get("symbol","")})")

        with st.container():
            print(info.get("current_price", 0))
            print(info.get("previous_close", 0))
            price_diff = round(float(info.get("current_price", 0)) - float(info.get("previous_close", 0)),2)
            price_diff_percent = abs(round((price_diff/info.get("previous_close", 0)) * 100,2))
            st.markdown(f"""
                        <p style="font-size: 30px">Price: {info.get("current_price", "N/A")} 
                        <span style="color:{"green" if price_diff > 0 else "red"}; font-size:24px;">{price_diff} ({price_diff_percent}%)</span></p>
                        """, unsafe_allow_html=True)
            
            col_one, col_two = st.columns(2)
                
            
            with col_one:
                st.subheader("Summary")
                values = get_stock_data(curr_ticker)
                st.markdown(create_summary_table(values), unsafe_allow_html=True)

            with col_two:
                st.subheader("Performance Chart")

                # Define tabs for different time intervals
                tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
                    "1 Day", "5 Days", "1 Month", "3 Months", "6 Months", 
                    "Year-to-Date", "1 Year", "5 Years"
                ])

                # Tab 1: 1 Day
                with tab1:
                    chart = create_performance_chart(ticker, "1d", "1m")
                    st.plotly_chart(chart, use_container_width=True)

                # Tab 2: 5 Days
                with tab2:
                    chart = create_performance_chart(ticker, "5d", "5m")
                    st.plotly_chart(chart, use_container_width=True)

                # Tab 3: 1 Month
                with tab3:
                    chart = create_performance_chart(ticker, "1mo", "1d")
                    st.plotly_chart(chart, use_container_width=True)

                # Tab 4: 3 Months
                with tab4:
                    chart = create_performance_chart(ticker, "3mo", "1d")
                    st.plotly_chart(chart, use_container_width=True)

                # Tab 5: 6 Months
                with tab5:
                    chart = create_performance_chart(ticker, "6mo", "1d")
                    st.plotly_chart(chart, use_container_width=True)

                # Tab 6: Year-to-Date
                with tab6:
                    chart = create_performance_chart(ticker, "ytd", "1d")
                    st.plotly_chart(chart, use_container_width=True)

                # Tab 7: 1 Year
                with tab7:
                    chart = create_performance_chart(ticker, "1y", "1d")
                    st.plotly_chart(chart, use_container_width=True)

                # Tab 8: 5 Years
                with tab8:
                    chart = create_performance_chart(ticker, "5y", "1wk")
                    st.plotly_chart(chart, use_container_width=True)

        st.subheader("Brief Summary")
        st.write(info.get("summary", ""))

        curr_news_yahoo = get_stock_news_yahoo(curr_ticker, 10)
        sentiment = get_news_sentiment(curr_news_yahoo)
        create_sidebar(sentiment, curr_news_yahoo)
        st.markdown("---")  # Horizontal line for separation

        
else:
    st.sidebar.subheader("Enter a stock ticker for recent news")

st.markdown(
    '<p style="color:red; text-align:center; font-weight:bold;">'
    'This application is a tool for informational purposes only. '
    'The data provided may not be accurate or up-to-date. '
    'Always consult with a financial advisor to ensure that any financial decisions '
    'are appropriate for your individual needs.</p>',
    unsafe_allow_html=True
)

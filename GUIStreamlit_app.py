pip show yfinance

import streamlit as st
import yfinance as yf
import pandas as pd

# Define the app
def app():
    # Set the title of the app
    st.title('Algorithmic Trading App')

    # Create input widgets for the trading algorithm parameters
    symbol = st.sidebar.text_input('Symbol', 'AAPL')
    strategy = st.sidebar.selectbox('Strategy', ['Buy and Hold', 'Moving Average Crossover'])
    short_period = st.sidebar.slider('Short Moving Average Period', 5, 50, 20)
    long_period = st.sidebar.slider('Long Moving Average Period', 50, 200, 100)
    investment = st.sidebar.number_input('Initial Investment', value=10000)

    # Load the stock price data using the yfinance library
    stock_data = yf.download(symbol, period='1y')
    stock_data.dropna(inplace=True)

    # Define the trading algorithm
    if strategy == 'Buy and Hold':
        stock_data['Shares'] = investment // stock_data['Open']
        stock_data['Cash'] = investment - stock_data['Shares'] * stock_data['Open']
        stock_data['Value'] = stock_data['Shares'] * stock_data['Close'] + stock_data['Cash']
    elif strategy == 'Moving Average Crossover':
        stock_data['Short_MA'] = stock_data['Close'].rolling(short_period).mean()
        stock_data['Long_MA'] = stock_data['Close'].rolling(long_period).mean()
        stock_data['Signal'] = 0.0
        stock_data['Signal'][short_period:] = \
            np.where(stock_data['Short_MA'][short_period:] > stock_data['Long_MA'][short_period:], 1.0, 0.0)
        stock_data['Positions'] = stock_data['Signal'].diff()
        stock_data['Shares'] = investment // stock_data['Open']
        stock_data['Cash'] = investment - stock_data['Shares'] * stock_data['Open']
        stock_data['Value'] = stock_data['Shares'] * stock_data['Close'] + stock_data['Cash']
        stock_data['Value'] = stock_data['Shares'] * stock_data['Close'] + stock_data['Cash']

    # Display the stock price data and trading results
    st.subheader('Stock Price Data')
    st.line_chart(stock_data['Close'])

    st.subheader('Trading Results')
    st.write(f"Final Value: ${stock_data['Value'].iloc[-1]:.2f}")
    st.write(f"Total Return: {(stock_data['Value'].iloc[-1] / investment - 1) * 100:.2f}%")
    st.line_chart(stock_data[['Value', 'Cash']])
    st.line_chart(stock_data['Shares'])
    st.line_chart(stock_data['Signal'])
    st.line_chart(stock_data['Positions'])

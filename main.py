import streamlit as st
import math
from scipy.stats import norm
import yfinance as yf

def calculate_option_price(is_call, S, K, T, r, sigma):
    d1 = (math.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if is_call:
        return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    else:
        return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

def get_data(ticker):
    data = yf.download(ticker)
    latest_price_AAPL = round(data['Close'][ticker_input][-1], 2)
    latest_price_TNX = round(data['Close']['^TNX'][-1], 2)
    return latest_price_AAPL, latest_price_TNX

st.title('Black-Scholes Option Pricing')
ticker_input = st.text_input('Ticker', value='AAPL').upper()
ticker = [ticker_input, "^TNX"]
S, r = get_data(ticker)
st.write(f'Stock Price (S): {S}')
st.write(f'Risk-free Rate (r): {r}%')
r =r/100
is_call = st.selectbox('Call or Put?', ['Call', 'Put']) == 'Call'
K = st.number_input('Strike Price (K)', value=100.0, step=0.1)
T = st.number_input('Time to Expiry (T) in Days', value=10.0, step=1.0) / 365.0  # Convert days to years



sigma = st.number_input('Implied Volatility % (sigma)', value=10.0, step=0.01)
sigma = sigma/100

option_price = round(calculate_option_price(is_call, S, K, T, r, sigma),2)
st.write(f'Option Price: {option_price}')



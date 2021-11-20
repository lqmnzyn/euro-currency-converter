import streamlit as st
import pandas as pd
# from PIL import Image
import requests
import json

#-------------------------------------#
# Title

# col1, mid, col2 = st.columns([1,5,20])
# with col1:
#     st.image('currency-conv.jpg', width=200)
# with col2:
#     st.title("EURO Currency Converter App", )

st.title('EURO Currency Converter App')
st.markdown("""
This app converts the value of EURO currency to other currencies! You can open up the menu at the top left corner to select the target currency.

""")
st.markdown("""
**PLEASE BE NOTED THAT ONLY EURO (EUR) CAN BE SELECTED AS THE BASE CURRENCY IN THIS VERSION.**

""")

#-------------------------------------#
# Sidebar + Main panel
st.sidebar.header('Input Options')

## Sidebar - Currency price unit
currency_list = ['AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'GBP', 'HKD', 'HRK', 'HUF', 'IDR', 'ILS', 'INR', 'ISK', 'JPY', 'KRW', 'MXN', 'MYR', 'NOK', 'NZD', 'PHP', 'PLN', 'RON', 'RUB', 'SEK', 'SGD', 'THB', 'TRY', 'USD', 'ZAR']
eur = ['EUR']
base_price_unit = st.sidebar.selectbox('Select base currency for conversion', eur)
symbols_price_unit = st.sidebar.selectbox('Select target currency to convert to', currency_list)


# Retrieving currency data from ratesapi.io
# http://api.exchangeratesapi.io/v1/latest?access_key=d9b5810dc284100eb8c2a9662f98d9f4&format=1&base=EUR&symbols=EUR
@st.cache
def load_data():
    url = ''.join(['http://api.exchangeratesapi.io/v1/latest?access_key=d9b5810dc284100eb8c2a9662f98d9f4&format=1', base_price_unit, '&symbols=', symbols_price_unit])
    response = requests.get(url)
    data = response.json()
    base_currency = pd.Series( data['base'], name='base_currency')
    rates_df = pd.DataFrame.from_dict( data['rates'].items() )
    rates_df.columns = ['converted_currency', 'price']
    conversion_date = pd.Series( data['date'], name='date' )
    df = pd.concat( [base_currency, rates_df, conversion_date], axis=1 )
    return df

df = load_data()

st.header('Currency Conversion')

st.write(df)

#---------------------------------#
# About
expander_bar = st.expander("About")
expander_bar.markdown("""
* **Python libraries:** streamlit, pandas, pillow, requests, json
* **Data source:** [ratesapi.io](https://ratesapi.io/) which is based on data published by [European Central Bank](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html))
""")
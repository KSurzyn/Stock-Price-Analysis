import pandas as pd
import streamlit
import yfinance as yf
import datetime as dt
from dateutil.relativedelta import relativedelta
import streamlit as st
import plotly.graph_objects as go


def page_config():
    st.set_page_config(
        layout="wide")
    st.title('Stock Price App (not typical)')
    st.markdown("""
    This app performs webscraping recent buyng and selling of stock from insiders and stock price! 
    * **Python libraries:** pandas, streamlit, plotly 
    * **Data source:** [Dataroma](https://www.dataroma.com/m/ins/ins.php), Yahoo Finance
    """)
    st.write("""#  """)
    st.sidebar.header('Select Ticker YTD')


def load_dataroma_data():
    url = 'https://www.dataroma.com/m/ins/ins.php'
    table = pd.read_html(url)
    df = table[2].dropna()
    return df


def get_selected_ticker(df):
    df_company = df['Symbol▲▼']
    unique_company_list = pd.unique(df_company)
    selected_ticker = st.sidebar.selectbox('Tickers', unique_company_list)
    if type(selected_ticker) is str:
        return selected_ticker
    else:
        st.experimental_rerun()


def transform_dataroma_data(df, selected_ticker):
    df_dataroma = df[['Purchase/Sale', 'Symbol▲▼', 'Shares', 'Trans. Date▲▼', 'Amount $▲▼']]
    df_dataroma_grouped = df_dataroma.groupby(['Purchase/Sale', 'Symbol▲▼', 'Trans. Date▲▼']).sum().reset_index()
    df_dataroma_table = df_dataroma_grouped[df_dataroma_grouped['Symbol▲▼'] == selected_ticker]
    x = df_dataroma_table.drop(['Symbol▲▼'], axis=1)
    streamlit.dataframe(x)
    return x


def get_data_to_candlestick(selected_ticker):
    end_date = dt.datetime.now()
    start_date = end_date - relativedelta(years=1)
    ticker = yf.Ticker(selected_ticker)
    history = ticker.history(period="1y", start=start_date, end=end_date, interval='1d')
    history['Date'] = history.index
    return history


def draw_candlestick(history):
    candlestick = go.Candlestick(x=history['Date'],
                                 open=history['Open'],
                                 high=history['High'],
                                 low=history['Low'],
                                 close=history['Close'])
    figure = go.Figure(data=[candlestick])
    figure.update_layout(height=800)
    st.plotly_chart(figure, use_container_width=True)


page_config()
dataroma_data = load_dataroma_data()
ticker = get_selected_ticker(dataroma_data)
transform_dataroma_data(dataroma_data, ticker)

data_to_candlestick = get_data_to_candlestick(ticker)
draw_candlestick(data_to_candlestick)






from django.shortcuts import render
import json
import requests
import os

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"


REAL_TIME_DATA_API_KEY = os.environ.get('API_K_RTD')
NEWS_API_KEY = os.environ.get('API_K_N')
STOCK_DATA_HISTORY_API_KEY = os.environ.get('API_K_SDH')

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
REAL_TIME_DATA = "https://financialmodelingprep.com/api/v3/quote-short/TSLA?apikey=2d4d605c25190468fc00fe2aca6a2276"
STOCK_ENDPOINT_GAINERS = f"https://financialmodelingprep.com/api/v3/stock_market/gainers?apikey={REAL_TIME_DATA_API_KEY}"
STOCK_ENDPOINT_LOSERS  = f"https://financialmodelingprep.com/api/v3/stock_market/losers?apikey={REAL_TIME_DATA_API_KEY}"
STOCK_ENDPOINT_ACTIVE = f"https://financialmodelingprep.com/api/v3/stock_market/actives?apikey={REAL_TIME_DATA_API_KEY}"


# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# Create your views here.
def index(request):
    return render(request, 'pages/index.html')

def landing(request):
    return render(request, 'pages/landing.html')

def market(request):
    stock_parm = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': STOCK_NAME,
        'interval': '5min',
        'apikey': STOCK_DATA_HISTORY_API_KEY
        # 'apikey':'qhAGfTSCPZBvwtX5zd79_aHssRYEafLU'
    }

    new_parm = {

        'q': COMPANY_NAME,
        'apikey': NEWS_API_KEY
    }

    # response_stock = requests.get("https://www.alphavantage.co/query", params=stock_parm)
    response_stock_live_losers = requests.get(STOCK_ENDPOINT_LOSERS)
    response_stock_live_losers.raise_for_status()

    losers = open('data/top_losers.json')
    # data = json.load(losers)
    data = response_stock_live_losers.json()

    response_stock_live_gainers = requests.get(STOCK_ENDPOINT_GAINERS)
    response_stock_live_gainers.raise_for_status()
    gainers = open('data/top_gainers.json')
    # data2 = json.load(gainers)
    data2 = response_stock_live_gainers.json()

    response_stock_live_active = requests.get(STOCK_ENDPOINT_ACTIVE)
    response_stock_live_active.raise_for_status()

    data3 = response_stock_live_active.json()

    # print(type(data2[0].change))
    # print(type(data2[0]['price']))

    context = {
        'data': data,
        'data2': data2,
        'data3': data3
    }
    return render(request, 'pages/market.html', context=context)

def dashboard(request):
    return render(request, 'dashboard/charts.html')
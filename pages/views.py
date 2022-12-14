import json
import requests
import os

from django.core.mail import send_mail

from .forms import NewUserForm, EditProfileForm, ProfileForm
from .forms import NewUserForm, WatchlistForm, WatchlistDeleteForm, NewsForm, NewsDeleteForm, ThresholdForm, ThresholdDeleteForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect



from pages.models import Stock, WatchList, StockNew, Profile, Threshold

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"


# REAL_TIME_DATA_API_KEY = os.environ.get('API_K_RTD')
# NEWS_API_KEY = os.environ.get('API_K_N')
# STOCK_DATA_HISTORY_API_KEY = os.environ.get('API_K_SDH')

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
REAL_TIME_DATA = "https://financialmodelingprep.com/api/v3/quote-short/TSLA?apikey=2d4d605c25190468fc00fe2aca6a2276"
STOCK_ENDPOINT_GAINERS = f"https://financialmodelingprep.com/api/v3/stock_market/gainers?apikey=2d4d605c25190468fc00fe2aca6a2276"
STOCK_ENDPOINT_LOSERS = f"https://financialmodelingprep.com/api/v3/stock_market/losers?apikey=2d4d605c25190468fc00fe2aca6a2276"
STOCK_ENDPOINT_ACTIVE = f"https://financialmodelingprep.com/api/v3/stock_market/actives?apikey=2d4d605c25190468fc00fe2aca6a2276"
PRICE_CHANGE = f"https://financialmodelingprep.com/api/v3/stock-price-change/AAPL?apikey=2d4d605c25190468fc00fe2aca6a2276"

# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# Create your views here.
def index(request):
    return render(request, 'pages/index.html')


def landing(request):
    return render(request, 'pages/landing.html')

def market(request):

    # response_stock = requests.get("https://www.alphavantage.co/query", params=stock_parm)
    response_stock_live_losers = requests.get(STOCK_ENDPOINT_LOSERS)
    response_stock_live_losers.raise_for_status()

    # losers = open('data/top_losers.json')
    # data = json.load(losers)
    data = response_stock_live_losers.json()

    response_stock_live_gainers = requests.get(STOCK_ENDPOINT_GAINERS)
    response_stock_live_gainers.raise_for_status()
    # gainers = open('data/top_gainers.json')
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


@login_required
def dashboard(request):
    tickers = Stock.objects.all()

    return render(request, 'dashboard/charts.html', {"stocks": tickers})

def register(request):
    if request.method == "POST":
        print("entering POST")
        form = NewUserForm(request.POST)
        form2 = ProfileForm(request.POST)
        if form.is_valid():
            print("form is valid")
            user = form.save()
            profile = Profile()
            profile.profile_pic = 'profile_images/b2.jpeg'
            profile.user_id = user
            profile.user_city = ".."
            profile.user_state = ".."
            profile.user_street = ".."
            profile.user_zipcode = "12345"
            profile.save()
            user.save()
            messages.success(request, "Registration successful.")
            return redirect("login")

        else:
            print(form.errors)
            messages.error(request, "Unsuccessful registration. Invalid information.")

    else:
        print("here")
        form = NewUserForm()

    return render(request, 'registration/register.html', context={"register_form": form})


def watchlist(request, pk):
    print(pk)
    watch_list = WatchList.objects.filter(user_id=pk)
    print(watch_list.values_list())
    resp = {}
    response_stock = 'Default value'
    for elem in watch_list:
        print(elem.stock_id)
        stock_parm = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': elem.stock_id,
            'interval': '60min',
            'apikey': '2APHUBAY3C5SAEY9'
        }
        try:
            response_stock = requests.get("https://www.alphavantage.co/query", params=stock_parm)
            response_stock.raise_for_status()
            yt_date = response_stock.json()['Meta Data']['3. Last Refreshed']
            resp[elem.stock_id] = response_stock.json()['Time Series (60min)'][yt_date]['4. close']
        except:
            resp[
                'error'] = "{'Note': 'Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.'}"

        print(response_stock.json())

        # print(response_stock.json()['Time Series (60min)'][yt_date]['4. close'])


    return render(request, 'dashboard/watchlist.html', {"resp": resp})
def watchlist_new(request, pk):
    if request.method == "POST":

        form = WatchlistForm(request.POST)
        if form.is_valid():
            new_ticker = form.save(commit=False)
            for users in Profile.objects.filter(user_id=pk):
                new_ticker.user_id = users.user_id
            try:
                print(f"new_ticker: {new_ticker.stock_id}")
                my_obj = WatchList.objects.get(stock_id=new_ticker.stock_id, user_id=new_ticker.user_id)
            except:
                new_ticker.save()
            watch_list = WatchList.objects.filter(user_id=pk)
            print(watch_list.values_list())
            resp = {}
            response_stock = 'Default value'
            for elem in watch_list:
                print(elem.stock_id)
                stock_parm = {
                    'function': 'TIME_SERIES_INTRADAY',
                    'symbol': elem.stock_id,
                    'interval': '60min',
                    'apikey': '2APHUBAY3C5SAEY9'
                }
                try:
                    response_stock = requests.get("https://www.alphavantage.co/query", params=stock_parm)
                    response_stock.raise_for_status()
                    yt_date = response_stock.json()['Meta Data']['3. Last Refreshed']
                    resp[elem.stock_id] = response_stock.json()['Time Series (60min)'][yt_date]['4. close']
                except:
                    resp['error'] = "{'Note': 'Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.'}"

        return render(request, 'dashboard/watchlist.html', {"resp": resp})
    else:
        form = WatchlistForm()

    return render(request, 'dashboard/watchlist_new.html', {'form': form})

def watchlist_delete(request, pk):
    if request.method == "POST":
        form = WatchlistDeleteForm(request.POST)
        if form.is_valid():
            ticker_name = form.save(commit=False)
            for users in Profile.objects.filter(user_id=pk):
                ticker_name.user_id = users.user_id
            print(f"ticker_name: {ticker_name.stock_id}")
            try:
                my_obj = WatchList.objects.get(stock_id=ticker_name.stock_id, user_id=ticker_name.user_id)
                my_obj.delete()
            except Exception as ev:
                print(f"error deleting {ev}")
            watch_list = WatchList.objects.filter(user_id=pk)
            print(watch_list.values_list())
            resp = {}
            response_stock = 'Default value'
            for elem in watch_list:
                print(elem.stock_id)
                stock_parm = {
                    'function': 'TIME_SERIES_INTRADAY',
                    'symbol': elem.stock_id,
                    'interval': '60min',
                    'apikey': '2APHUBAY3C5SAEY9'
                }
                try:
                    response_stock = requests.get("https://www.alphavantage.co/query", params=stock_parm)
                    response_stock.raise_for_status()
                    yt_date = response_stock.json()['Meta Data']['3. Last Refreshed']
                    resp[elem.stock_id] = response_stock.json()['Time Series (60min)'][yt_date]['4. close']
                except:
                    resp[
                        'error'] = "{'Note': 'Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.'}"

        return render(request, 'dashboard/watchlist.html', {"resp": resp})
    else:
        form = WatchlistDeleteForm()

    return render(request, 'dashboard/watchlist_delete.html', {'form': form})
def news(request, pk):
    news_list = StockNew.objects.filter(user_id=pk)
    resp1 = {}
    response_news = "API call limit exhausted"
    for elem in news_list:
        company_name = Stock.objects.filter(stock_ticker__contains=elem.stock_id_id).values_list()[0][0]

        new_parm = {
            'q': company_name,
            'apikey': '38e071deaa854b62b36b3faf67fc038f'
        }
        try:
            response_news = requests.get("https://newsapi.org/v2/everything", params=new_parm)
            response_news.raise_for_status()
            response_news.json()
            news_title = [response_news.json()['articles'][i]['title'] for i in range(3)]
            news_description = [response_news.json()['articles'][i]['url'] for i in range(3)]
            message_out = []
            for x, y in zip(news_title, news_description):
                message_out.append(f"Headline: {x}  Link to news: {y} ")
            print(f"message_out : {message_out}")
            resp1[elem.stock_id_id] = message_out


        except:

            resp1['error'] = response_news

        print(f"resp1: {resp1}")
    return render(request, 'dashboard/news.html', {"resp1": resp1})

def sendmail(request, pk):
    # news_list = StockNew.objects.filter(user_id=pk)
    resp1 = {}
    response_news = "API call limit exhausted"
    # for elem in news_list:
    company_name = Stock.objects.filter(stock_ticker__contains=pk).values_list()[0][0]

    new_parm = {
            'q': company_name,
            'apikey': '38e071deaa854b62b36b3faf67fc038f'
    }
    try:
        response_news = requests.get("https://newsapi.org/v2/everything", params=new_parm)
        response_news.raise_for_status()
        response_news.json()
        news_title = [response_news.json()['articles'][i]['title'] for i in range(3)]
        news_description = [response_news.json()['articles'][i]['url'] for i in range(3)]
        message_out = []
        for x, y in zip(news_title, news_description):
            message_out.append(f"Headline: {x}  Link to news: {y} ")
            send_mail(
                f'{x}',
                f'{y}',
                'phuclinh9802@gmail.com',
                ['phuclinh9802@gmail.com'],
                fail_silently=False
            )
        print(f"message_out : {message_out}")
        # resp1[elem.stock_id_id] = message_out


    except:

        resp1['error'] = response_news


    print("hitting")
    return render(request, 'dashboard/mailsent.html')

def news_new(request, pk):
    if request.method == "POST":

        form = NewsForm(request.POST)
        if form.is_valid():

            form.instance.user = pk
            new_ticker = form.save(commit=False)

            for users in Profile.objects.filter(user_id=pk):
                new_ticker.user_id = users.user_id
            try:
                print(f"new_ticker: {new_ticker.stock_id}")
                my_obj = StockNew.objects.get(stock_id=new_ticker.stock_id, user_id=new_ticker.user_id)
            except:
                new_ticker.save()

            news_list = StockNew.objects.filter(user_id=pk)
            resp1 = {}
            response_news = "API call limit exhausted"
            for elem in news_list:
                company_name = Stock.objects.filter(stock_ticker__contains=elem.stock_id_id).values_list()[0][0]

                new_parm = {
                    'q': company_name,
                    'apikey': '38e071deaa854b62b36b3faf67fc038f'
                }
                try:
                    response_news = requests.get("https://newsapi.org/v2/everything", params=new_parm)
                    response_news.raise_for_status()
                    response_news.json()
                    news_title = [response_news.json()['articles'][i]['title'] for i in range(3)]
                    news_description = [response_news.json()['articles'][i]['url'] for i in range(3)]
                    message_out = []
                    for x, y in zip(news_title, news_description):
                        message_out.append(f"Headline: {x}  Link to news: {y} ")
                    print(f"message_out : {message_out}")
                    resp1[elem.stock_id_id] = message_out


                except:

                    resp1['error'] = response_news

                print(f"resp1: {resp1}")

        return render(request, 'dashboard/news.html', {"resp1": resp1})
    else:
        form = NewsForm()

    return render(request, 'dashboard/news_new.html', {'form': form})


def news_delete(request, pk):
    if request.method == "POST":
        form = NewsDeleteForm(request.POST)
        if form.is_valid():
            ticker_name = form.save(commit=False)
            for users in Profile.objects.filter(user_id=pk):
                ticker_name.user_id = users.user_id
            print(f"ticker_name: {ticker_name.stock_id}")
            try:
                my_obj = StockNew.objects.get(stock_id=ticker_name.stock_id, user_id=ticker_name.user_id)
                my_obj.delete()
            except Exception as ev:
                print(f"error deleting {ev}")
            news_list = StockNew.objects.filter(user_id=pk)
            resp1 = {}
            response_news = "API call limit exhausted"
            for elem in news_list:
                company_name = Stock.objects.filter(stock_ticker__contains=elem.stock_id_id).values_list()[0][0]

                new_parm = {
                    'q': company_name,
                    'apikey': '38e071deaa854b62b36b3faf67fc038f'
                }
                try:
                    response_news = requests.get("https://newsapi.org/v2/everything", params=new_parm)
                    response_news.raise_for_status()
                    response_news.json()
                    news_title = [response_news.json()['articles'][i]['title'] for i in range(3)]
                    news_description = [response_news.json()['articles'][i]['url'] for i in range(3)]
                    message_out = []
                    for x, y in zip(news_title, news_description):
                        message_out.append(f"Headline: {x}  Link to news: {y} ")
                    print(f"message_out : {message_out}")
                    resp1[elem.stock_id_id] = message_out


                except:

                    resp1['error'] = response_news

                print(f"resp1: {resp1}")

        return render(request, 'dashboard/news.html', {"resp1": resp1})
    else:
        form = NewsDeleteForm()

    return render(request, 'dashboard/news_delete.html', {'form': form})

def userupdate(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save()
            profile.save()
            return render(request, 'dashboard/index.html')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'dashboard/userupdate.html', {'form': form})

def threshold(request, pk):
    print(pk)
    watch_list = Threshold.objects.filter(user_id=pk)
    print(watch_list.values_list())
    resp = {}
    response_stock = 'Default value'
    for elem in watch_list:
        print(elem.stock_id)
        stock_parm = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': elem.stock_id,
            'interval': '60min',
            'apikey': '2APHUBAY3C5SAEY9'
            }
        try:
            response_stock = requests.get("https://www.alphavantage.co/query", params=stock_parm)
            response_stock.raise_for_status()
            yt_date = response_stock.json()['Meta Data']['3. Last Refreshed']
            resp[elem.stock_id] = response_stock.json()['Time Series (60min)'][yt_date]['4. close']
        except:
            resp['error']  = "{'Note': 'Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.'}"



        print(response_stock.json())

        # print(response_stock.json()['Time Series (60min)'][yt_date]['4. close'])


    return render(request, 'dashboard/threshold.html', {"resp": resp, "watch_list": watch_list})

def threshold_new(request, pk):
    if request.method == "POST":

        form = ThresholdForm(request.POST)
        if form.is_valid():
            new_ticker = form.save(commit=False)
            for users in Profile.objects.filter(user_id=pk):
                new_ticker.user_id = users.user_id
            try:
                print(f"new_ticker: {new_ticker.stock_id}")
                my_obj = Threshold.objects.get(stock_id=new_ticker.stock_id, user_id=new_ticker.user_id)
            except:
                new_ticker.save()
            watch_list = Threshold.objects.filter(user_id=pk)
            print(watch_list.values_list())
            resp = {}
            response_stock = 'Default value'
            for elem in watch_list:
                print(elem.stock_id)
                stock_parm = {
                    'function': 'TIME_SERIES_INTRADAY',
                    'symbol': elem.stock_id,
                    'interval': '60min',
                    'apikey': '2APHUBAY3C5SAEY9'
                }
                try:
                    response_stock = requests.get("https://www.alphavantage.co/query", params=stock_parm)
                    response_stock.raise_for_status()
                    yt_date = response_stock.json()['Meta Data']['3. Last Refreshed']
                    resp[elem.stock_id] = response_stock.json()['Time Series (60min)'][yt_date]['4. close']
                except:
                    resp['error'] = "{'Note': 'Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.'}"

        return render(request, 'dashboard/threshold.html', {"resp": resp, "watch_list": watch_list})
    else:
        form = ThresholdForm()

    return render(request, 'dashboard/threshold_new.html', {'form': form})

def threshold_delete(request, pk):
    if request.method == "POST":
        form = ThresholdDeleteForm(request.POST)
        if form.is_valid():
            ticker_name = form.save(commit=False)
            for users in Profile.objects.filter(user_id=pk):
                ticker_name.user_id = users.user_id
            print(f"ticker_name: {ticker_name.stock_id}")
            try:
                my_obj = Threshold.objects.get(stock_id=ticker_name.stock_id, user_id=ticker_name.user_id)
                my_obj.delete()
            except Exception as ev:
                print(f"error deleting {ev}")
            watch_list = Threshold.objects.filter(user_id=pk)
            print(watch_list.values_list())
            resp = {}
            response_stock = 'Default value'
            for elem in watch_list:
                print(elem.stock_id)
                stock_parm = {
                    'function': 'TIME_SERIES_INTRADAY',
                    'symbol': elem.stock_id,
                    'interval': '60min',
                    'apikey': '2APHUBAY3C5SAEY9'
                }
                try:
                    response_stock = requests.get("https://www.alphavantage.co/query", params=stock_parm)
                    response_stock.raise_for_status()
                    yt_date = response_stock.json()['Meta Data']['3. Last Refreshed']
                    resp[elem.stock_id] = response_stock.json()['Time Series (60min)'][yt_date]['4. close']
                except:
                    resp[
                        'error'] = "{'Note': 'Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.'}"

        return render(request, 'dashboard/threshold.html', {"resp": resp, "watch_list": watch_list})
    else:
        form = ThresholdDeleteForm()

    return render(request, 'dashboard/threshold_delete.html', {'form': form})
from django.shortcuts import render
import json
# Create your views here.
def index(request):
    return render(request, 'pages/index.html')

def landing(request):
    return render(request, 'pages/landing.html')

def market(request):
    losers = open('data/top_losers.json')
    data = json.load(losers)

    gainers = open('data/top_gainers.json')
    data2 = json.load(gainers)

    # print(type(data2[0].change))
    # print(type(data2[0]['price']))

    context = {
        'data': data,
        'data2': data2
    }
    return render(request, 'pages/market.html', context=context)

def dashboard(request):
    return render(request, 'dashboard/charts.html')
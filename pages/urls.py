from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.landing, name='landing'),
    path('market/', views.market, name='market'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('news/', views.news, name='news'),
    path('userupdate/<int:pk>', views.userupdate, name='userupdate'),
    path('accounts/register/', views.register, name='register'),
    path('sendmail/', views.sendmail, name='sendmail'),
]


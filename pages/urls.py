from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.landing, name='landing'),
    path('market/', views.market, name='market'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('watchlist/<str:pk>/list', views.watchlist, name='watchlist'),
    path('watchlist/<str:pk>/create/', views.watchlist_new, name='watchlist_new'),
    path('watchlist/<str:pk>/delete/', views.watchlist_delete, name='watchlist_delete'),
    path('threshold/<str:pk>/list', views.threshold, name='threshold'),
    path('threshold/<str:pk>/create/', views.threshold_new, name='threshold_new'),
    path('threshold/<str:pk>/delete/', views.threshold_delete, name='threshold_delete'),
    path('news/<str:pk>/list', views.news, name='news'),
    path('news/<str:pk>/create/', views.news_new, name='news_new'),
    path('news/<str:pk>/delete/', views.news_delete, name='news_delete'),
    path('sendmail/<str:pk>/list', views.sendmail, name='sendmail'),
    path('accounts/register/', views.register, name='register'),
    path('userupdate/<int:pk>', views.userupdate, name='userupdate'),
    # path('landing/', views.landing, name='landing')
]


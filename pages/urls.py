from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('market/', views.market, name='market'),
    path('dashboard/', views.dashboard, name='dashboard')
    # path('landing/', views.landing, name='landing')
]

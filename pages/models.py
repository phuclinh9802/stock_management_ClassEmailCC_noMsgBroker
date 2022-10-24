import uuid

from django.db import models
from django.forms import DateField
from django.urls import reverse


# Create your models here.
class Role(models.Model):
    """Model representing a book genre."""
    role_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               help_text="Unique ID for role")

    role_name = models.CharField(
        max_length=200,
        help_text='Enter role name')

    def __str__(self):
        """String for representing the Model object."""
        return self.role_id


class Profile(models.Model):
    """Model representing a Profile."""
    profile_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                  help_text="Unique ID for profile")

    profile_street = models.TextField(
        max_length=50,
        help_text='Enter profile street name')

    profile_city = models.CharField(
        max_length=20,
        help_text='Enter profile city name')

    profile_state = models.CharField(
        max_length=20,
        help_text='Enter profile state name')

    profile_zipcode = models.CharField(
        max_length=10,
        help_text='Enter profile zipcode name')

    user_id = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.profile_id


class Users(models.Model):
    """Model representing Users."""
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               help_text="Unique ID for User")

    user_first_name = models.CharField(
        max_length=50,
        help_text='Enter user first name')

    user_last_name = models.CharField(
        max_length=20,
        help_text='Enter user last name')

    user_email = models.EmailField(
        max_length=254,
        help_text='Enter user Email Address')

    stock_id = models.ForeignKey('Stock', on_delete=models.SET_NULL, null=True)

    role_id = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.user_id


class Watch_List(models.Model):
    """Model representing a Watch List."""
    watchlist_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                    help_text="Unique ID for watchlist")

    user_watchlist_name = models.CharField(
        max_length=50,
        help_text='Enter the watchlist name')

    user_watchlist_date_created = DateField(help_text='Enter the watchlist created date')

    user_id = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True)

    stock_id = models.ForeignKey('Stock', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.watchlist_id


class Stock(models.Model):
    """Model representing a Stock."""
    stock_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                help_text="Unique ID for stock")

    stock_name = models.CharField(
        max_length=20,
        help_text='Enter the stock name')

    stock_ticker = models.CharField(
        max_length=20,
        help_text='Enter the stock ticker')

    stock_quantity = models.CharField(
        max_length=20,
        help_text='Enter the stock quantity')

    stock_active_quantity = models.CharField(
        max_length=20,
        help_text='Enter the stock active quantity')

    stock_day_percentage = models.CharField(
        max_length=20,
        help_text='Enter the stock day percentage')

    stock_highest_price = models.CharField(
        max_length=20,
        help_text='Enter the stock highest price')

    stock_lowest_price = models.CharField(
        max_length=20,
        help_text='Enter the stock lowest price')

    stock_open_price = models.CharField(
        max_length=20,
        help_text='Enter the stock open price')

    stock_date = models.DateField(help_text='Enter the stock date')

    user_id = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True)

    watchlist_id = models.ForeignKey('Watch_List', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.stock_id


class Preference(models.Model):
    """Model representing a stock Preference."""
    preference_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                     help_text="Unique ID for preference")

    user_id = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True)

    stock_id = models.ForeignKey('Stock', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.preference_id


class Stocks_list(models.Model):
    """Model representing a stocks list."""
    stocks_list_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                      help_text="Unique ID for Stock List")

    stock_id = models.ForeignKey('Stock', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.stocks_list_id


class New(models.Model):
    """Model representing News."""
    news_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               help_text="Unique ID for the news")

    news_title = models.CharField(
        max_length=50,
        help_text='Enter the stock news title')

    news_content = models.TextField(
        max_length=5000,
        help_text='Enter the stock news content')

    news_date = models.DateField(help_text='Enter the News date')

    stock_id = models.ForeignKey('Stock', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.news_id


class Threshold(models.Model):
    """Model representing Thresholds."""
    threshold_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                    help_text="Unique ID for threshold")

    threshold_status =(
        ('d', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    threshold_percentage_change = models.CharField(
        max_length=500,
        help_text='Enter the stock threshold percentage change content')

    threshold_price_change = models.CharField(
        max_length=500,
        help_text='Enter the stock threshold price change content')

    stock_id = models.ForeignKey('Stock', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.threshold_id
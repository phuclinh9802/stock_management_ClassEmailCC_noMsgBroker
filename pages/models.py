from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user_id = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, primary_key=True)
    profile_pic = models.ImageField(upload_to='profile_images', null=True)
    user_street = models.TextField(
        max_length=50,
        help_text='Enter street name', null=True)

    user_city = models.CharField(
        max_length=20,
        help_text='Enter city name', null=True)

    user_state = models.CharField(
        max_length=20,
        help_text='Enter state name', null=True)

    user_zipcode = models.CharField(
        max_length=10,
        help_text='Enter zipcode name', null=True)
    def __str__(self):
        return str(self.user_id)



# Create your models here.

class Stock(models.Model):
    """Model representing a Stock."""

    stock_name = models.CharField(
        max_length=20,
        help_text='Enter the stock name', null=True)

    stock_ticker = models.CharField(
        max_length=4,
        help_text='Enter the stock ticker', primary_key=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.stock_ticker

class WatchList(models.Model):
    """Model representing a Watch List."""

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)


class StockNew(models.Model):
    """Model representing News."""

    stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)

    news_title = models.CharField(
        max_length=500,
        help_text='Enter the stock news title', null=True)

    news_content = models.TextField(
        max_length=5000,
        help_text='Enter the stock news content', null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.news_title


class Threshold(models.Model):
    """Model representing Thresholds."""
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)


    threshold_percentage_change = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text='Enter the stock threshold percentage change content', null=True
    )

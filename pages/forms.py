from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import WatchList, StockNew, Threshold


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")
		widgets = {
			'username': forms.TextInput(attrs={'class': 'username'}),
			'email': forms.TextInput(attrs={'class': 'email'}),
			'password1': forms.TextInput(attrs={'class': 'password1'}),
			'password2': forms.TextInput(attrs={'class': 'password2'}),
		}

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class WatchlistForm(forms.ModelForm):

   class Meta:
       model = WatchList
       fields = ('stock_id',)

class WatchlistDeleteForm(forms.ModelForm):
   class Meta:
       model = WatchList
       fields = ('stock_id', )

class NewsForm(forms.ModelForm):

   class Meta:
       model = StockNew
       fields = ('stock_id', )

class NewsDeleteForm(forms.ModelForm):
   class Meta:
       model = StockNew
       fields = ('stock_id', )

class ThresholdForm(forms.ModelForm):

   class Meta:
       model = Threshold
       fields = ('stock_id', 'threshold_percentage_change')

class ThresholdDeleteForm(forms.ModelForm):
   class Meta:
       model = Threshold
       fields = ('stock_id', )

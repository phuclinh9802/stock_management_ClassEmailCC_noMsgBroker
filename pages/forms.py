from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Profile
from .models import WatchList, StockNew

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


class EditProfileForm(ModelForm):
	class Meta:
		model = User
		fields = ("email", "first_name", "last_name")

class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		fields = ("user_street", "user_city", "user_state", "user_zipcode")
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

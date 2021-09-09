from django.contrib.auth.password_validation import (
    password_validators_help_text_html)
from django.core.exceptions import ValidationError
from django.db import transaction as tx
from django.db import IntegrityError
from django.utils import timezone
from django.utils.html import mark_safe
from django import forms

from ..invite.signals import invite_is_accepted
from apps.users.models import User



class SignUpWithCode(forms.Form):

	code 	= forms.CharField(label="Code",required=True,
			widget=forms.TextInput(attrs={'placeholder':'eg.ABCD-EFGH-IJKL'}))



class RegisterForm(forms.Form):

	error_messages = {
	"duplicate_username":"A user with that username already exists.",
	"passwords_mismatch":"The two password fields didn't match.",
	"not_enough_passwords_length":"Password length must 5 or more alphanumeric characters.",
	}


	email 	   	    = forms.EmailField(label='Email',
									required=True,
									widget=forms.EmailInput())

	username     	= forms.CharField(label="username",
									required=True,
									widget=forms.TextInput())


	password1 		= forms.CharField(
        label=('Password'), required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=("Enter a strong password"))

	password2 		= forms.CharField(
        label=("Password confirmation"), required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=("Enter the same password as above, for verification."))

	# ordering fields from email.
	field_order = ['email']

	def __init__(self,*args,user=None,**kwargs):
		self.user = user
		super(RegisterForm,self).__init__(*args,**kwargs)
		# e-mail
		self.fields['email'].initial = self.user.email
		self.fields['email'].disabled = True
		# username
		self.fields['username'].initial = self.user.username


	def validate_user_is_active(self,user):
		qs = User._default_manager
		if qs.filter(email__iexact=user.email,is_active=True):
			raise ValidationError('You are already verified,please login')
		return


	def clean_username(self):
		username 	= self.cleaned_data['username']
		users = User._default_manager.exclude(username__iexact=self.user.username)
		if self.user.username != username:
			# user is changing username
			qs = users.filter(username__iexact=username)
			if qs.exists():
				raise forms.ValidationError(self.error_messages['duplicate_username'],code='duplicate_username')
			return self.cleaned_data['username']
		return self.cleaned_data['username']


	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 != password2:
			raise forms.ValidationError(self.error_messages['passwords_mismatch'],code='passwords_mismatch')
		if len(password2) <= 5:
			raise forms.ValidationError(self.error_messages['not_enough_passwords_length'],code='not_enough_passwords_length')
		return password2


	def save(self,commit=True,**kwargs):
		user = self.user

		user.username = self.cleaned_data['username']
		user.set_password(self.cleaned_data['password2']) 
		user.is_active = True
		user.date_joined = timezone.now()

		# call signal to alter invite state
		invite_is_accepted.send(sender=None,user=user)

		if commit:
			try:
				user.save()
			except IntegrityError:
				raise ValueError("User is already registered")
		return user
		


class LoginForm(forms.Form):
	username     	= forms.CharField(label="Your user-name",required=True,widget=forms.TextInput(attrs={
		'placeholder':'eg. kkophi','required':True,'autofocus':True
		}))
	password 	    = forms.CharField(label="Your password",widget=forms.PasswordInput(attrs={
		'placeholder': '*************'
		}))
	
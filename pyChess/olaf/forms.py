from django import forms

from django.contrib.auth import authenticate

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from olaf.validators import *

class LoginForm ( forms.Form ):
	username = forms.CharField (
		label = "Username",
		max_length = 64,
		validators = [ validate_username_login_availability ]
	)
	password = forms.CharField (
		label = "Password",
		widget = forms.PasswordInput (),
	)

	def clean ( self ):
		super ( LoginForm, self ).clean ()

		username = self.cleaned_data.get ( 'username' )
		password = self.cleaned_data.get ( 'password' )
		user = authenticate ( username = username, password = password )

		if ( (username is not None) and (password is not None) and (user is None) ):
			self.add_error ( 'password', ValidationError ( _( "Wrong Password" ), code = "incorrect_password" ) )

class RegisterForm ( forms.Form ):
	username = forms.CharField (
		label = "Username",
		max_length = 64,
		validators = [
			RegexValidator (
				regex = "^[a-zA-Z][a-zA-Z0-9_]*$",
				message = "Username should start with an alphabetic character and can only contain characters, numbers and underscore",
				code = "invalid_username"
			),
			validate_username_register_availability,
		]
	)

	email = forms.EmailField (
		label = "Email",
		validators = [ validate_email_register_availability ]
	)

	password = forms.CharField (
		label = "Password",
		widget = forms.PasswordInput (),
	)
	confirm_password = forms.CharField (
		label = "Confirm Password",
		widget = forms.PasswordInput ()
	)

	def clean ( self ):
		super ( RegisterForm, self ).clean ()

		password = self.cleaned_data.get ( 'password' )
		confirm_password = self.cleaned_data.get ( 'confirm_password' )

		if ( (password is not None) and (confirm_password is not None) and password != confirm_password ):
			self.add_error ( 'confirm_password', ValidationError ( _( "Passwords Dont Match" ), "no_password_match" ) )

class UsernameOrEmailForm ( forms.Form ):#TODO needs validator
	search_key = forms.CharField (
		label = "Username or Email",
		max_length = 64
	)

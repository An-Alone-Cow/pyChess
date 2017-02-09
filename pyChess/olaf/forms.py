from django import forms

class LoginForm ( forms.Form ):
	username = forms.CharField ( label = "Username", max_length = 64 )
	password = forms.CharField ( label = "Password", widget = forms.PasswordInput () )

class RegisterForm ( LoginForm ):
	email = forms.EmailField ( label = "Email" )
	confirm_password = forms.CharField ( label = "Confirm Password", widget = forms.PasswordInput () )

	field_order = [ 'username', 'email', 'password', 'confirm_password' ]

class UsernameOrEmailForm ( forms.Form ):
	search_key = forms.CharField ( label = "Username or Email", max_length = 64 )

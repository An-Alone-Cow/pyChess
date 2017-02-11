from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from olaf.models import *

def login_user ( request, form ):
	username = form.cleaned_data [ 'username' ]
	password = form.cleaned_data [ 'password' ]
	user = authenticate ( username = username, password = password )

	login ( request, user )

	return None

def register_user ( request, form ):
	username = form.cleaned_data [ 'username' ]
	password = form.cleaned_data [ 'password' ]
	email = form.cleaned_data [ 'email' ]

	user = User.objects.create_user ( username, password = password )
	user.save ()
	userdata = UserData ( master = user )
	userdata.save ()
	custom_email_field = CustomEmailField ( email = email, is_primary = True, user = userdata )
	custom_email_field.save ()
	userdata.save ()
	user.save ()

	return None

def logout_user ( request ):
	logout ( request )

	return None

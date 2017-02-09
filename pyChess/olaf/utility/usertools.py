from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from ..models import *

def login_user ( request, form ):
	username = form.cleaned_data [ 'username' ]
	password = form.cleaned_data [ 'password' ]
	user = authenticate ( username = username, password = password )

	login ( request, user )

	return None

def register_user ( form ):
	username = form.cleaned_data [ 'username' ]
	password = form.cleaned_data [ 'password' ]
	email = form.cleaned_data [ 'email' ]

	user = User.objects.create_user ( username, password = password )
	user.save ()
	userdata = UserData ( master = user )
	userdata.save ()
	customemailfield = CustomEmailField ( email = email, is_primary = True, user = userdata )
	customemailfield.size ()
	userdata.save ()
	user.save ()

	return None

def logout_user ( request ):
	logout ( request )

	return None

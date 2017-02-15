from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.core.mail import send_mail

from django.utils import timezone
from django.urls import reverse

from olaf.models import *

def login_user ( request, form ):
	username = form.cleaned_data [ 'username' ]
	password = form.cleaned_data [ 'password' ]
	user = authenticate ( username = username, password = password )

	login ( request, user )

	recent = user.userdata.recent_game
	if ( recent is not None ):
		request.session [ 'game_id' ] = recent.id
	else:
		request.session.pop ( 'game_id', default = None )

	request.session.set_expiry ( 0 )

	return None

def register_user ( request, form ):
	username = form.cleaned_data [ 'username' ]
	password = form.cleaned_data [ 'password' ]
	email = form.cleaned_data [ 'email' ]


	user = User.objects.create_user ( username, password = password )

	userdata = UserData ( master = user )
	userdata.save ()

	custom_email_field = CustomEmailField ( email = email, is_primary = True, user = userdata )
	custom_email_field.save ()

	token = ExpirableTokenField ( token = '', user = userdata, expiration_time = timezone.now () )
	token.save ()


	token = PasswordResetTokenGenerator ().make_token ( user )
	send_mail(
	    'Email Activation',
    	'Click on <a href = \"%s\">this link</a> to activate your account' % ("http://" + request.META["HTTP_HOST"] + reverse ( 'olaf:activate_account', args = (token,) )),
    	'icp95.project@gmail.com',
    	[email],
    	fail_silently=False,
	)

	token_field = user.userdata.token
	token_field.token = token
	token_field.expiration_time = timezone.now () + timezone.timedelta(days=3)
	token_field.save ()

	return None

def init_pass_reset_token ( request, form ):
	search_key = form.cleaned_data [ 'search_key' ]

	user = User.objects.filter ( username = search_key ).first ()
	if ( user is None ):
		user = User.objects.filter ( userdata__email_list__email = search_key ).first ()
		email = search_key
	else:
		email = user.userdata.email_list.filter ( is_primary = True ).first ().email

	
	token = PasswordResetTokenGenerator ().make_token ( user )
	send_mail(
	    'Email Activation',
    	'Click on <a href = \"%s\">this link</a> to re-set your password' % ("http://" + request.META["HTTP_HOST"] + reverse ( 'olaf:reset_password_action', args = (token,) ) ),
    	'icp95.project@gmail.com',
    	[email],
    	fail_silently=False,
	)

	token_field = user.userdata.token
	token_field.token = token
	token_field.expiration_time = timezone.now () + timezone.timedelta(days=1)
	token_field.save ()

def reset_password_action ( request, form, token ):
	user = User.objects.get ( userdata__token__token = token )
	password = form.cleaned_data [ 'password' ]

	user.set_password ( password )

def resend_activation_email ( request, form ):
	search_key = form.cleaned_data [ 'search_key' ]

	user = User.objects.filter ( username = search_key ).first ()
	if ( user is None ):
		user = User.objects.filter ( userdata__email_list__email = search_key ).first ()
		email = search_key
	else:
		email = user.userdata.email_list.filter ( is_primary = True ).first ().email

	
	token = PasswordResetTokenGenerator ().make_token ( user )
	send_mail(
	    'Email Activation',
    	'Click on <a href = \"%s\">this link</a> to activate your account' % ("http://" + request.META["HTTP_HOST"] + reverse ( 'olaf:activate_account', args = (token,) ) ),
    	'icp95.project@gmail.com',
    	[email],
    	fail_silently=False,
	)

	token_field = user.userdata.token
	token_field.token = token
	token_field.expiration_time = timezone.now () + timezone.timedelta(days=3)
	token_field.save ()

def logout_user ( request ):
	logout ( request )

	return None

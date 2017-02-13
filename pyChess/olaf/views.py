from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse

from .forms import *
from .utility import usertools

# Create your views here.

def index ( request ):
	args = {}

	message = request.session.get ( 'message' )
	if ( message is not None ):
		args [ 'message' ] = message
		del request.session [ 'message' ]

	return render ( request, 'olaf/index.html', args )

form_operation_dict = {#TODO keep an eye one like
	'login' : ( usertools.login_user, LoginForm, 'olaf/login.html', {}, 'index', {} ),
	'register' : ( usertools.register_user, RegisterForm, 'olaf/register.html', {}, 'index', { 'message' : "An Activation Email has been Sent to You" } ),
}
def form_operation ( request, oper, is_auth = False ):
	func, FORM, fail_template, fail_args, success_url, success_args = form_operation_dict [ oper ]

	if ( request.user.is_authenticated == is_auth ):
		if ( request.method == 'POST' ):
			form = FORM ( request.POST )

			if ( form.is_valid () ):
				func ( request, form )

				for key in success_args:
					request.session [ key ] = success_args [ key ]
				return HttpResponseRedirect ( reverse ( success_url, args = () ) )
		else:
			form = FORM ()

		fail_args [ 'form' ] = form
		return render ( request, fail_template, fail_args )
	else:
		return HttpResponseRedirect ( reverse ( 'index', args = () ) )

@login_required
def user_form_operation ( request, oper ):
	return form_operation ( request, oper, True )

def logout_user ( request ):
	usertools.logout_user ( request )

	return HttpResponseRedirect ( reverse ( 'index', args = () ) )

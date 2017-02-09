from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse

from .forms import *
from .utility import usertools

# Create your views here.

def index ( request ):#TODO
	return HttpResponse("Hello, world. You're at the polls index.")

form_operation_dict = {#TODO keep an eye one like
	'login' : ( usertools.login_user, LoginForm, 'olaf/login.html', {}, 'olaf/index.html', {} ),
	'register' : ( usertools.register_user, RegisterForm, 'olaf/register.html', {}, 'olaf/index.html', { 'message' : "An Activation Email has been Sent to You" } ),
}
def form_operation ( request, oper ):
	func, FORM, fail_template, fail_args, success_template, success_args = form_operation_dict [ oper ]

	if ( request.method == 'POST' ):
		form = FORM ( request )

		if ( form.is_valid () ):
			func ( request, form )
			return render ( request, success_template, success_args )
	else:
		form = FORM ()

	fail_args [ 'form' ] = form
	return render ( request, fail_template, fail_args )

@login_required
def user_form_operation ( request, oper ):
	return form_operation ( request, oper )

def logout_user ( request ):
	usertools.logout_user ( request )

	return HttpResponseRedirect ( reverse ( 'index', args = () ) )

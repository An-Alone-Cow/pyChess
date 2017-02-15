from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse

from django.utils import timezone

from olaf.models import *
from olaf.forms import *
from olaf.utility import usertools

def index ( request ):
	args = {}

	message = request.session.pop ( 'message', default = None )
	if ( message is not None ):
		args [ 'message' ] = message

	if ( request.user.is_authenticated ):
		f = lambda a : str ( a.date () ) + " - " + str ( a.hour ) + ":" + str ( a.minute ) + ":" + str ( a.second )
		args [ 'game_board' ] = [[ 0 ] * 8] * 8
		args [ 'game_list' ] = list ([str ( game.id ), f ( game.creation_time )] for game in request.user.userdata.game_history.filter ( result = 0 ).order_by ( '-creation_time' ) )

		return render ( request, 'olaf/index_logged_in.html', args )
	else:
		args [ 'login_form' ] = LoginForm ()
		args [ 'register_form' ] = RegisterForm ()
		args [ 'score' ] = list ( [user.master.username, user.wins, user.loses, user.ties] for user in UserData.objects.filter ( is_active = True ) )[ : 15]

		return render ( request, 'olaf/index_not_logged_in.html', args )

#html files!!!!
form_operation_dict = {
	'login' : (
		usertools.login_user,
		LoginForm,
		'olaf/login.html',
		{},
		'index',
		{ 'message' : "You're logged in. :)"}
	),
	'register' : (
		usertools.register_user,
		RegisterForm,
		'olaf/register.html',
		{},
		'index',
		{ 'message' : "An activation email has been sent to you" }
	),
	'password_reset_request' : (
		usertools.init_pass_reset_token,
		ForgotPasswordUsernameOrEmailForm,
		'olaf/password_reset_request.html',
		{},
		'index',
		{ 'message' : "An email containing the password reset link will be sent to your email"}
	),
	'reset_password' : (
		usertools.reset_password_action,
		PasswordChangeForm,
		'olaf/reset_password.html',
		{},
		'olaf:login',
		{ 'message' : "Password successfully changed, you can login now" }
	),
	'resend_activation_email' : (
		usertools.resend_activation_email,
		ResendActivationUsernameOrEmailForm,
		'olaf/resend_activation_email.html',
		{},
		'index',
		{ 'message' : "Activation email successfully sent to your email" }
	),
}
def form_operation ( request, oper, *args ):
	func, FORM, fail_template, fail_args, success_url, success_args = form_operation_dict [ oper ]

	if ( request.method == 'POST' ):
		form = FORM ( request.POST )

		if ( form.is_valid () ):
			func ( request, form, *args )

			for key in success_args:
				request.session [ key ] = success_args [ key ]
			return HttpResponseRedirect ( reverse ( success_url ) )
	else:
		form = FORM ()

	message = request.session.pop ( 'message', default = None )
	if ( message is not None ):
		fail_args [ 'message' ] = message

	fail_args [ 'form' ] = form
	return render ( request, fail_template, fail_args )

#view functions

def login_user ( request ):
	if ( request.user.is_authenticated ):
		return HttpResponseRedirect ( reverse ( 'index' ) )

	return form_operation ( request, 'login' )

def register_user ( request ):
	if ( request.user.is_authenticated ):
		return HttpResponseRedirect ( reverse ( 'index' ) )

	return form_operation ( request, 'register' )

def password_reset_request ( request ):
	if ( request.user.is_authenticated ):
		return HttpResponseRedirect ( reverse ( 'index' ) )

	return form_operation ( request, 'password_reset_request' )

def reset_password_action ( request, token ):
	if ( request.user.is_authenticated ):
		return HttpResponseRedirect ( reverse ( 'index' ) )

	tk = ExpirableTokenField.objects.filter ( token = token ).first ()
	if ( tk is None ):
		request.session [ 'message' ] = "Broken link"
		return HttpResponseRedirect ( reverse ( 'index' ) )
	else:
		if ( timezone.now () <= tk.expiration_time ):
			return form_operation ( request, 'reset_password', token )
		else:
			request.session [ 'message' ] = "Link expired, try getting a new one"
			return HttpResponseRedirect ( reverse ( 'olaf:reset_password' ) )

def activate_account ( request, token ):
	if ( request.user.is_authenticated ):
		return HttpResponseRedirect ( reverse ( 'index' ) )

	tk = ExpirableTokenField.objects.filter ( token = token ).first ()
	if ( tk is None ):
		request.session [ 'message' ] = "Broken link"
		return HttpResponseRedirect ( reverse ( 'index' ) )
	else:
		if ( timezone.now () <= tk.expiration_time ):
			if ( tk.user.is_active ):
				request.session [ 'message' ] = "Account already active"
				return HttpResponseRedirect ( reverse ( 'index' ) )
			else:
				userdata = tk.user
				userdata.is_active = True
				userdata.save ()

				request.session [ 'message' ] = "Your account has been activated successfully"
				return HttpResponseRedirect ( reverse ( 'olaf:login' ) )
		else:
			request.session [ 'message' ] = "Link expired, try getting a new one"
			return HttpResponseRedirect ( reverse ( 'olaf:resend_activation_email' ) )

def resend_activation_email ( request ):
	if ( request.user.is_authenticated ):
		return HttpResponseRedirect ( reverse ( 'index' ) )

	return form_operation ( request, 'resend_activation_email' )

def logout_user ( request ):
	usertools.logout_user ( request )

	return HttpResponseRedirect ( reverse ( 'index' ) )

def scoreboard ( request ):
	if ( request.method == 'POST' ):
		username = request.POST.get ( 'username' )
		user = User.objects.filter ( username = username ).first ()

		if ( user is None ):
			request.session [ 'message' ] = "User not found"
			return HttpResponseRedirect ( reverse ( 'olaf:scoreboard' ) )
		else:
			return HttpResponseRedirect ( reverse ( 'olaf:user_profile', args = (username, ) ) )
	else:
		args = {}

		message = request.session.pop ( 'message', default = None )
		if ( message is not None ):
			args [ 'message' ] = message

		lst = [ (user.master.username, user.wins, user.loses, user.ties) for user in UserData.objects.filter ( is_active = True ) ]
		args [ 'lst' ] = lst

		return render ( request, 'olaf/scoreboard.html', args )
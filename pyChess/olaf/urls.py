from django.conf.urls import url

from . import views

app_name = 'olaf'
urlpatterns = [#function assignment
	url ( r'^login/$', views.login_user, name = 'login' ),
	url ( r'^register/$', views.register_user, name = 'register' ),
	url ( r'^reset_password/$', views.password_reset_request, name = 'reset_password' ),
	url ( r'^reset_password/([0-9A-Za-z\-]*)/?$', views.reset_password_action, name = 'reset_password_action' ),
	url ( r'^activate/([0-9A-Za-z\-]*)/?$', views.activate_account, name = 'activate_account' ),
	url ( r'^resend_email/$', views.resend_activation_email, name = 'resend_activation_email' ),
	url ( r'^logout/?$', views.logout_user, name = 'logout' ),
	url ( r'^scoreboard/?$', views.scoreboard, name = 'scoreboard' ),
	url ( r'^move/?$', views.move, name = 'move_parser' ),

	#url ( r'^profile/?$', , name = 'profile' ),
	#url ( r'^user/([a-zA-Z][a-zA-Z0-9_]*)/?$', , name = 'user_profile' ),
]
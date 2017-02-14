from django.conf.urls import url

from . import views

app_name = 'olaf'
urlpatterns = [#function assignment
	url ( r'^login/$', , name = 'login' ),
	url ( r'^register/$', , name = 'register' ),
	url ( r'^reset_password/$', , name = 'reset_password' ),
	url ( r'^reset_password/([0-9A-Za-z\-]*)/?$', , name = 'reset_password_action' ),
	url ( r'^activate/([0-9A-Za-z\-]*)/?$', , name = 'activate_account' ),
	url ( r'^resend_email/$', , name = 'resend_activation_email' ),
	url ( r'^logout/?$', , name = 'logout' ),

	url ( r'^profile/?$', , name = 'profile' ),

	url ( r'^user/([a-zA-Z][a-zA-Z0-9_]*)/?$', , name = 'user_profile' ),
	url ( r'^scoreboard/?$', , name = 'scoreboard' )
]
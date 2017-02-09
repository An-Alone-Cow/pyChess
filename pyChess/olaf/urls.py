from django.conf.urls import url

from . import views

app_name = 'olaf'
urlpatterns = [
	url ( r'^login/?$', views.form_operation, { 'oper' : 'login' }, name = 'login' ),
	url ( r'^register/?$', views.form_operation, { 'oper' : 'register' }, name = 'register' ),
	url ( r'^logout/?$', views.logout_user, name = 'logout' ),
]

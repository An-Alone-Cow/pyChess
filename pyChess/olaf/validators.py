from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from .models import CustomEmailField as CEField

def validate_username_register_availability ( value ):
	user = User.objects.filter ( username = value ).first ()

	if ( user is not None ):
		raise ValidationError (
			_( "Username is already taken." ),
			code = "username_unavailable"
		)

def validate_username_login_availability ( value ):
	user = User.objects.filter ( username = value ).first ()

	if ( user is None ):
		raise ValidationError (
			_( "Username doesnt exist" ),
			code = "username_doesnt_exist"
		)
	else:
		if ( not user.userdata.is_active ):
			raise ValidationError (
				_( "User not activated yet." ),
				code = "user_not_active"
			)

def validate_username_login_activatability ( value ):
	user = User.objects.filter ( username = value ).first ()

	if ( user is not None ):
		if ( not user.userdata.is_active ):
			raise ValidationError (
				_( "User not activated yet." ),
				code = "user_not_active"
			)

def validate_email_register_availability ( value ):
	email = CEField.objects.filter ( email = value ).first ()

	if ( email is not None ):
		raise ValidationError (
			_( "Email unavailable" ),
			code = "email_unavailable"
		)

def validate_user_search_key ( value ):
	email = CEField.objects.filter ( email = value ).first ()
	email2 = CEField.objects.filter ( user__username = value ).first ()

	if ( (email is None) and (email2 is None) ):
		raise ValidationError (
			_( "No user or email found" ),
			code = "invalid_search_key"
		)

def validate_user_search_key_activatability ( value ):
	user = User.objects.filter ( username = value ).first ()
	user2 = User.objects.filter ( userdata__email_list__email = value ).first ()

	if ( user is not None ):
		if ( not user.userdata.is_active ):
			raise ValidationError (
				_( "User not activated yet." ),
				code = "user_not_active"
			)
	else:
		if ( user2 is not None ):
			if ( not user2.userdata.is_active ):
				raise ValidationError (
					_( "User not activated yet." ),
					code = "user_not_active"
				)

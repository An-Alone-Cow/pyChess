from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from .models import CustomEmailField as CEField

def validate_username_register_availability ( value ):
	user = User.objects.filter ( username = value ).first ()

	if ( user is not None ):
		raise ValidationError (
			_( "Username Unavailable" ),
			code = "username_unavailable"
		)

def validate_username_login_availability ( value ):
	user = User.objects.filter ( username = value ).first ()

	if ( user is None ):
		raise ValidationError (
			_( "Username Doesnt Exist" ),
			code = "username_doesnt_exist"
		)

def validate_email_register_availability ( value ):
	email = CEField.objects.filter ( email = value ).first ()

	if ( email is not None ):
		raise ValidationError (
			_( "Email Unavailable" ),
			code = "email_unavailable"
		)

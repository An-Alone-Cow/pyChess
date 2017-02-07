from django.core.validators import validate_email

def email_is_valid ( string ):
	try:
	    validate_email ( string )
	    return True
	except validate_email.ValidationError:
	    return False

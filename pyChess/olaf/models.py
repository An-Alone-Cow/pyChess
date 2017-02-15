from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

class UserData ( models.Model ):
	master = models.OneToOneField ( User, on_delete = models.CASCADE )

	wins = models.IntegerField ( default = 0 )
	ties = models.IntegerField ( default = 0 )
	loses = models.IntegerField ( default = 0 )

	is_active = models.BooleanField ( default = False )

	@property
	def recent_game ( self ):
		if ( hasattr ( self, 'game_history' ) ):
			return self.game_history.filter ( is_recent = True ).first ()
		return None

	class Meta:
		ordering = [ '-wins', 'loses', '-ties' ]

class GameBoard ( models.Model ):
	INITIAL_STATE = '4qJUX2X8bojZVNRp1nOF053R9sMHhefbMuOkdSf4Uo'
	state = models.CharField ( max_length = 64, default = INITIAL_STATE )
	creation_time = models.DateTimeField ( auto_now_add = True )
	result = models.IntegerField ( default = 0 )

	is_recent = models.BooleanField ( default = False )
	user = models.ForeignKey ( UserData, on_delete = models.CASCADE, related_name = 'game_history' )

class CustomEmailField ( models.Model ):
	email = models.EmailField ( max_length = 64 )
	is_primary = models.BooleanField ( default = False )
	user = models.ForeignKey ( UserData, on_delete = models.CASCADE, related_name = 'email_list' )

class ExpirableTokenField ( models.Model ):
	token = models.CharField ( max_length = 256 )
	expiration_time = models.DateTimeField ()
	user = models.OneToOneField ( UserData, on_delete = models.CASCADE, related_name = 'token' )
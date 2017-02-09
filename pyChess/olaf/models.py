from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

class UserData ( models.Model ):
	master = models.OneToOneField ( User, on_delete = models.CASCADE )
	name = models.CharField ( default = '', max_length = 64 )

	wins = models.IntegerField ( default = 0 )
	ties = models.IntegerField ( default = 0 )
	loses = models.IntegerField ( default = 0 )

	is_active = models.BooleanField ( default = False )

class GameBoard ( models.Model ):
	INITIAL_STATE = "1" * 64 #TODO
	state = models.CharField ( max_length = 64, default = INITIAL_STATE )
	creation_time = models.DateTimeField ( auto_now_add = True )
	result = models.IntegerField ( default = 0 )

	is_recent = models.BooleanField ( default = False )
	user = models.ForeignKey ( UserData, on_delete = models.CASCADE, related_name = 'game_history' )

class CustomEmailField ( models.Model ):
	email = models.EmailField ( max_length = 64 )
	is_primary = models.BooleanField ( default = False )
	user = models.ForeignKey ( UserData, on_delete = models.CASCADE, related_name = 'email_list' )

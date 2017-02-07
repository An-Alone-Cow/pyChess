from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

class UserData ( models.Model ):
	master = models.OneToOneField ( User, on_delete = models.CASCADE )
	name = models.CharField ( max_length = 64 )

	wins = models.IntegerField ( default = 0 )
	ties = models.IntegerField ( default = 0 )
	loses = models.IntegerField ( default = 0 )

class GameBoard ( models.Model ):
	initial_state = "1" * 64 #TODO
	state = models.CharField ( max_length = 64, default = initial_state )
	creation_time = models.DateTimeField ( auto_now_add = True )
	result = models.IntegerField ( default = 0 )

	is_recent = models.BooleanField ( default = False )
	user = models.ForeignKey ( UserData, on_delete = models.CASCADE, related_name = 'game_history' )

class CustomEmailField ( models.Model ):
	email = models.CharField ( max_length = 64 )
	is_primary = models.BooleanField ( default = False )
	user = models.ForeignKey ( UserData, on_delete = models.CASCADE, related_name = 'email_list' )

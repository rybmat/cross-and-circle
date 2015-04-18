from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Player(models.Model):
	user = models.OneToOneField(User)
	won = models.PositiveIntegerField(default=0)
	lost = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.user.username


class GameBoard(models.Model):
	f_00 = models.CharField(max_length=1, null=True, blank=True)
	f_01 = models.CharField(max_length=1, null=True, blank=True)
	f_02 = models.CharField(max_length=1, null=True, blank=True)
	f_10 = models.CharField(max_length=1, null=True, blank=True)
	f_11 = models.CharField(max_length=1, null=True, blank=True)
	f_12 = models.CharField(max_length=1, null=True, blank=True)
	f_20 = models.CharField(max_length=1, null=True, blank=True)
	f_21 = models.CharField(max_length=1, null=True, blank=True)
	f_22 = models.CharField(max_length=1, null=True, blank=True)


class Game(models.Model):
	started = models.DateTimeField(auto_now_add=True)
	finished = models.DateTimeField(null=True, blank=True, default=None)
	player_a = models.ForeignKey(Player, related_name='player_a')
	player_b = models.ForeignKey(Player, related_name='player_b')
	winner = models.ForeignKey(Player, null=True, blank=True, default=None)
	board = models.OneToOneField(GameBoard)

	def __str__(self):
		return self.player_a + ' vs ' + player_b


class GameRequest(models.Model):
	requesting = models.ForeignKey(Player, related_name='requesting')
	requested = models.ForeignKey(Player, related_name='requested')
	date = models.DateTimeField(auto_now_add=True)


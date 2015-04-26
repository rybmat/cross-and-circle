from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
	started = models.DateTimeField(auto_now_add=True)
	finished = models.DateTimeField(null=True, blank=True, default=None)
	player_a = models.ForeignKey(User, related_name='player_a')
	player_b = models.ForeignKey(User, related_name='player_b')
	winner = models.ForeignKey(User, null=True, blank=True, default=None)

	def __str__(self):
		return self.player_a + ' vs ' + player_b

	def is_finished(self):
		return self.winner is not None

class Move(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True)
	player = models.ForeignKey(User, related_name='all_moves')
	position = models.PositiveSmallIntegerField()
	game = models.ForeignKey(Game)

	class Meta:
		unique_together = ("game", "position",)

	def __str__(self):
		return ' '.join([str(self.id), self.player.username, str(self.game.id), str(self.position)])


class GameRequest(models.Model):
	requesting = models.ForeignKey(User, related_name='requesting')
	requested = models.ForeignKey(User, related_name='requested')
	date = models.DateTimeField(auto_now_add=True)


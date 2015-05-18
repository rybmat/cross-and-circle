from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

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


class POEToken(models.Model):
	token = models.CharField(max_length=50, unique=True)


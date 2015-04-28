from rest_framework import serializers
from datetime import datetime
import models

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
	games = serializers.HyperlinkedIdentityField(view_name='user-games', lookup_field='username')
	stats = serializers.HyperlinkedIdentityField(view_name='user-stats', lookup_field='username')
	class Meta:
		model = models.User
		fields = ('url', 'username', 'email', 'password', 'games', 'stats')
		extra_kwargs = {'password': {'write_only': True}, 'games': {'read_only': True}, 'stats': {'read_only': True}}
		lookup_field = 'username'

	def create(self, validated_data):
		user = models.User(
			email=validated_data.get('email', ''),
			username=validated_data['username']
		)
		user.set_password(validated_data['password'])
		user.save()
		return user

	def update(self, user, validated_data):
		user.username = validated_data.get('username', user.username)
		user.email = validated_data.get('email', user.email)
		if 'password' in validated_data:
			user.set_password(validated_data['password'])
		user.save()

		return user


class GameRequestSerializer(serializers.HyperlinkedModelSerializer):
	requesting = serializers.SlugRelatedField(queryset=models.User.objects.all(), slug_field='username')
	requested = serializers.SlugRelatedField(queryset=models.User.objects.all(), slug_field='username')
	class Meta:
		model = models.GameRequest
		extra_kwargs = {'date': {'read_only': True}}
		fields = ('id', 'url', 'requesting', 'requested', 'date')


class GameSerializer(serializers.HyperlinkedModelSerializer):
	player_a = serializers.SlugRelatedField(queryset=models.User.objects.all(), slug_field='username')
	player_b = serializers.SlugRelatedField(queryset=models.User.objects.all(), slug_field='username')
	winner = serializers.SlugRelatedField(queryset=models.User.objects.all(), slug_field='username')
	moves = serializers.HyperlinkedIdentityField(view_name='game-moves', read_only=True)

	class Meta:
		model = models.Game
		fields = ('id', 'url', 'started', 'player_a', 'player_b', 'winner', 'finished', 'moves')


class MoveSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Move

	def to_representation(self, obj):
		res = {
			'timestamp': obj.timestamp,
			'player': obj.player.username,
			'position': obj.position,
			'game': obj.game.id
		}
		return res

	def to_internal_value(self, data):
		if 'player' in data:
			data['player'] = user_or_validationerror('player', data['player']).pk

			if 'game' in data:
				try:
					game = models.Game.objects.get(pk=data['game'])
					if game.is_finished():
						raise serializers.ValidationError({'detail': 'game is finished'})
					
					players = (game.player_a.id, game.player_b.id,)
					if data['player'] not in players:
						raise serializers.ValidationError({'player': 'player otside of game'})
					
					moves = game.move_set.order_by('-timestamp').values()

					if (len(moves) == 0 and data['player'] == game.player_a) or (len(moves) > 0 and data['player'] == moves[0]['player_id']):
						raise serializers.ValidationError({'player': 'Second player is taking turn'})

				except models.Game.DoesNotExist:
					raise serializers.ValidationError({'details': 'game with given id does not exist'})

		if 'position' in data and data['position'] not in range(9):
			raise serializers.ValidationError({'position': 'position index shoud be in range 0..8'})

		return super(MoveSerializer, self).to_internal_value(data)


# def required_fields(req, data):
# 	for r in req:
# 		if r not in data:
# 			raise serializers.ValidationError({'detail': 'Missing parameters'})


def user_or_validationerror(fieldname, username):
	try:
		u = models.User.objects.get(username=username)
	except models.User.DoesNotExist:
		raise serializers.ValidationError({fieldname: 'User not found'})
	return u

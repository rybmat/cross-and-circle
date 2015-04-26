from rest_framework import serializers
from datetime import datetime
import models

class PlayerSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.User
		fields = ('username', 'email', 'password')
		extra_kwargs = {'password': {'write_only': True}}

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


class GameRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.GameRequest
		extra_kwargs = {'date': {'read_only': True}}

	def to_representation(self, obj):
		result = {
			"id": obj.id,
			"date": str(obj.date),
			"requesting": obj.requesting.username,
			"requested": obj.requested.username,
		}
		return result

	def to_internal_value(self, data):
		required_fields(['requesting', 'requested'], data)
		requesting_u = user_or_validationerror('requesting', data['requesting'])
		requested_u = user_or_validationerror('requested', data['requested'])

		return {'requesting': requesting_u, 'requested': requested_u}


class GameSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Game
		extra_kwargs = {}

	def to_representation(self, obj):
		result = {
			'id': obj.id,
			'started': obj.started,
			'finished': obj.finished,
			'player_a': obj.player_a.username,
			'player_b': obj.player_b.username,
			'winner': obj.winner.username if obj.winner is not None else None,
		}

		return result

	def to_internal_value(self, data):
		
		if 'player_a' in data:
			data['player_a'] = user_or_validationerror('player_a', data['player_a']).pk
		if 'player_b' in data:
			data['player_b'] = user_or_validationerror('player_b', data['player_b']).pk
		
		if 'winner' in data:
			data['winner'] = user_or_validationerror('winner', data['winner']).pk
			data['finished'] = datetime.now().isoformat()
		
		return super(GameSerializer, self).to_internal_value(data)


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
						raise serializers.ValidationError({'details': 'game is finished'})
					
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


def required_fields(req, data):
	for r in req:
		if r not in data:
			raise serializers.ValidationError({'details': 'Missing parameters'})


def user_or_validationerror(fieldname, username):
	try:
		u = models.User.objects.get(username=username)
	except models.User.DoesNotExist:
		raise serializers.ValidationError({fieldname: 'User not found'})

	return u

from rest_framework import serializers
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
		if 'requesting' not in data or 'requested' not in data:
			raise serializers.ValidationError({'details': 'Missing parameters'})

		try:
			requesting_u = models.User.objects.get(username=data['requesting'])
		except models.User.DoesNotExist:
			raise serializers.ValidationError({'requesting': 'User not found'})
		try:
			requested_u = models.User.objects.get(username=data['requested'])
		except models.User.DoesNotExist:
			raise serializers.ValidationError({'requested': 'User not found'})

		return {'requesting': requesting_u, 'requested': requested_u}


class GameSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Game

class MoveSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Move

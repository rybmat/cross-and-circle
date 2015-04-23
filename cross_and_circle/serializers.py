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


class GameSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Game

class MoveSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Move

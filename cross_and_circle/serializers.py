from rest_framework import serializers
import models

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.User
		fields = ('username', 'email', 'password')
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		user = models.User(
			email=validated_data['email'],
			username=validated_data['username']
		)
		user.set_password(validated_data['password'])
		user.save()
		return user

class UserUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.User
		fields = ('username', 'email', 'password')
		extra_kwargs = {'password': {'write_only': True, 'required': False}, 'username': {'required': False}}

	def update(self, user, validated_data):
		user.username = validated_data.get('username', user.username)
		user.email = validated_data.get('email', user.email)
		if 'password' in validated_data:
			user.set_password(validated_data['password'])
			user.save()

		return user


class PlayerSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	class Meta:
		model = models.Player
		fields = ('won', 'lost', 'user')
		depth = 1

	def create(self, validated_data):
		user = UserSerializer(data=validated_data['user'])
		user.is_valid()
		user = user.save()
		player = models.Player(user=user)
		player.save()
		return player


class PlayerUpdateSerializer(serializers.ModelSerializer):
	user = UserUpdateSerializer()
	class Meta:
		model = models.Player
		fields = ('won', 'lost', 'user')
		depth = 1

	def update(self, instance, validated_data):
		user_data = validated_data.get('user', {})
		user = instance.user

		user_ser = UserUpdateSerializer(user, data=user_data)
		user_ser.is_valid()
		user_ser.save()

		instance.won = validated_data.get('won', instance.won)
		instance.lost = validated_data.get('lost', instance.lost)

		instance.save()
		
		return instance


class GameRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.GameRequest
		extra_kwargs = {'date': {'read_only': True}}


class GameSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Game

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from models import *
from serializers import * 


class Players(APIView):
	def get(self, request, format=None):
		players = User.objects.all()
		serializer = PlayerSerializer(players, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = PlayerSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)	



class PlayerDetails(APIView):

	def get(self, request, player_name, format=None):
		player = get_object_or_404(User, username=player_name)
		serializer = PlayerSerializer(player)
		return Response(serializer.data)


	def put(self, request, player_name, format=None):
		player = get_object_or_404(User, username=player_name)
		d = request.data

		serializer = PlayerSerializer(player, data=d, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PlayerStats(APIView):
	def get(self, request, player_name, format=None):
		return HttpResponse('player ' + player_name + 'stats - class_view')


class PlayerGames(APIView):
	def get(self, request, player_name, format=None):
		return HttpResponse('player ' + player_name + 'games - class_view')



class Games(APIView):
	def get(self, request, format=None):
		games = Game.objects.all()
		serializer = GameSerializer(games, many=True)
		return Response(serializer.data)

	# TODO: Remove, only for debuging
	def post(self, request, format=None):
		serializer = GameSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)	


class GameDetails(APIView):
	def get(self, request, id, format=None):
		game = get_object_or_404(Game, pk=id)
		serializer = GameSerializer(game)
		return Response(serializer.data)

	def put(self, request, id, format=None):
		game = get_object_or_404(Game, pk=id)
		if game.is_finished():
			# 405 Method Not Allowed (?)
			return Response({"details": "Can not modify finished game"}, status=status.HTTP_403_FORBIDDEN)

		if 'player_a' in request.data or 'player_b' in request.data:
			return Response({"details": "Can not modify players"}, status=status.HTTP_403_FORBIDDEN)

		serializer = GameSerializer(game, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			GameSerializer.Meta.extra_kwargs = bck
			return Response(serializer.data)
		GameSerializer.Meta.extra_kwargs = bck
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GameBoard(APIView):
	def get(self, request, id, format=None):
		return HttpResponse('game board' + id + ' - class_view')


class Requests(APIView):
	def get(self, request, format=None):
		params = {}
		if 'requesting' in request.query_params:
			params['requesting'] = get_object_or_404(User, username=request.query_params['requesting'])
		if 'requested' in request.query_params:
			params['requested'] = get_object_or_404(User, username=request.query_params['requested'])

		requests = GameRequest.objects.all().filter(**params)
		serializer = GameRequestSerializer(requests, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = GameRequestSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestDetails(APIView):
	def get(self, request, id, format=None):
		obj = get_object_or_404(GameRequest, pk=id)
		serializer = GameRequestSerializer(obj)
		return Response(serializer.data)

	def delete(self, request, id, format=None):
		# TODO: create new Game item
		obj = get_object_or_404(GameRequest, pk=id)
		obj.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

	def post(self, request, id, format=None):	# without that delete does not work
		return Response({})


class Moves(APIView):
	def get(self, request, format=None):
		return HttpResponse('Moves - class_view number')

	def post(self, request, format=None):
		pass


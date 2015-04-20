from django.http import Http404, HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from models import *
from serializers import * 


class Players(APIView):
	def get(self, request, format=None):
		players = Player.objects.all()
		serializer = PlayerSerializer(players, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = PlayerSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)	


class PlayerDetails(APIView):
	def get_player(self, plname):
		try:
			return Player.objects.get(user__username=plname)
		except Player.DoesNotExist:
			raise Http404

	def get(self, request, player_name, format=None):
		player = self.get_player(player_name)
		serializer = PlayerSerializer(player)
		return Response(serializer.data)


	def put(self, request, player_name, format=None):
		player = self.get_player(player_name)
		d = request.data
		d.setdefault('user', {})

		serializer = PlayerUpdateSerializer(player, data=d)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	# def delete(self, request, player_name, format=None):
	# 	pass


class PlayerStats(APIView):
	def get(self, request, player_name, format=None):
		return HttpResponse('player ' + player_name + 'stats - class_view')


class PlayerGames(APIView):
	def get(self, request, player_name, format=None):
		return HttpResponse('player ' + player_name + 'games - class_view')



class Games(APIView):
	def get(self, request, format=None):
		return HttpResponse('games - class_view')

	def post(self, request, format=None):
		pass


class GameDetails(APIView):
	def get(self, request, id, format=None):
		return HttpResponse('game ' + id + ' - class_view')

	def put(self, request, id, format=None):
		pass


class GameBoard(APIView):
	def get(self, request, id, format=None):
		return HttpResponse('game board' + id + ' - class_view')



class Requests(APIView):
	def get(self, request, format=None):
		return HttpResponse('request - class_view')

	def post(self, request, format=None):
		pass


class RequestPerPlayer(APIView):
	def get(self, request, player_name, format=None):
		return HttpResponse('request ' + player_name + ' - class_view')


class RequestDetails(APIView):
	def get(self, request, id, format=None):
		return HttpResponse('request ' + id + ' - class_view number')

	def put(self, request, id, format=None):
		pass

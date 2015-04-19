from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

class Players(APIView):
	def get(self, request, format=None):
		return HttpResponse('players - class_view')

	def post(self, request, format=None):
		pass


class PlayerDetails(APIView):
	def get(self, request, player_name, format=None):
		return HttpResponse('player ' + player_name + ' - class_view')

	def put(self, request, player_name, format=None):
		pass

	def delete(self, request, player_name, format=None):
		pass


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

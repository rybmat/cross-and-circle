from django.http import Http404, HttpResponse

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

def get_player(plname):
	try:
		return User.objects.get(username=plname)
	except User.DoesNotExist:
		raise Http404

class PlayerDetails(APIView):

	def get(self, request, player_name, format=None):
		player = get_player(player_name)
		serializer = PlayerSerializer(player)
		return Response(serializer.data)


	def put(self, request, player_name, format=None):
		player = get_player(player_name)
		d = request.data
		d.setdefault('user', {})

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
		params = {}
		if 'requesting' in request.query_params:
			params['requesting'] = get_player(request.query_params['requesting'])
		if 'requested' in request.query_params:
			params['requested'] = get_player(request.query_params['requested'])

		requests = GameRequest.objects.all().filter(**params)
		serializer = GameRequestSerializer(requests, many=True)
		result = serializer.data
		print result
		for r in result:
			r['requesting'] = User.objects.get(pk=r['requesting']).username
			r['requested'] = User.objects.get(pk=r['requested']).username

		return Response(result)

	def post(self, request, format=None):
		requested, requesting = request.data['requested'], request.data['requesting']
		if 'requesting' in request.data and 'requested' in request.data:
			request.data['requested'] = get_player(requested).pk
			request.data['requesting'] = get_player(requesting).pk

			serializer = GameRequestSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				res = serializer.data
				res['requested'] = requested
				res['requesting'] = requesting
				return Response(res, status=status.HTTP_201_CREATED)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		return Response({"details": "to less parameters"}, status=status.HTTP_400_BAD_REQUEST)


class RequestDetails(APIView):
	def get(self, request, id, format=None):
		return HttpResponse('request ' + id + ' - class_view number')

	def put(self, request, id, format=None):
		pass

	def delete(self, request, format=None):
		pass


class Moves(APIView):
	def get(self, request, format=None):
		return HttpResponse('Moves - class_view number')

	def post(self, request, format=None):
		pass

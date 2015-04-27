from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime

from models import *
from serializers import * 


class Players(ListCreateAPIView):
	queryset = User.objects.all()
	serializer_class = PlayerSerializer
	lookup_field = 'username'


class PlayerDetails(RetrieveUpdateAPIView):
	queryset = User.objects.all()
	serializer_class = PlayerSerializer # TODO: make password non required while update
	lookup_field = 'username'


class PlayerGames(APIView):
	def get(self, request, username, format=None):
		player = get_object_or_404(User, username=username)
		if 'opponent' in request.query_params:
			opponent = get_object_or_404(User, username=request.query_params['opponent'])
			games = Game.objects.all().filter(Q(player_a=player) | Q(player_b=player), Q(player_a=opponent) | Q(player_b=opponent))
		else:
			games = Game.objects.all().filter(Q(player_a=player) | Q(player_b=player))

		serializer = GameSerializer(games, many=True, context={'request':self.request})
		return Response(serializer.data)



class PlayerStats(APIView):
	def get(self, request, username, format=None):
		player = get_object_or_404(User, username=username)
		
		if 'opponent' in request.query_params:
			opponent = get_object_or_404(User, username=request.query_params['opponent'])
			games = Game.objects.all().filter(Q(player_a=player) | Q(player_b=player), Q(player_a=opponent) | Q(player_b=opponent)).exclude(winner=None)
		else:
			games = Game.objects.all().filter(Q(player_a=player) | Q(player_b=player)).exclude(winner=None)

		all_games = len(games)
		won_games = len(games.filter(winner=player))
		lost_games = all_games - won_games

		return Response({"games": all_games, "won": won_games, "lost": lost_games})



class Games(ListAPIView):
	serializer_class = GameSerializer

	def get_queryset(self):
		params = {}
		if 'player_a' in self.request.query_params:
			params['player_a'] = get_object_or_404(User, username=self.request.query_params['player_a'])
		if 'player_b' in self.request.query_params:
			params['player_b'] = get_object_or_404(User, username=self.request.query_params['player_b'])

	 	return Game.objects.all().filter(**params)



class GameDetails(RetrieveAPIView):
	queryset = Game.objects.all()
	serializer_class = GameSerializer



class Requests(ListCreateAPIView):
	serializer_class = GameRequestSerializer

	def get_queryset(self):
		params = {}
		if 'requesting' in self.request.query_params:
			params['requesting'] = get_object_or_404(User, username=self.request.query_params['requesting'])
		if 'requested' in self.request.query_params:
			params['requested'] = get_object_or_404(User, username=self.request.query_params['requested'])
		return GameRequest.objects.all().filter(**params)



class RequestDetails(RetrieveDestroyAPIView):
	queryset = GameRequest.objects.all()
	serializer_class = GameRequestSerializer



class Moves(APIView):
	def get(self, request, id, format=None):
		game = get_object_or_404(Game, pk=id)
		moves = Move.objects.all().filter(game=game)
		serializer = MoveSerializer(moves, many=True)
		return Response(serializer.data)

	def post(self, request, id, format=None):
		request.data['game'] = id
		serializer = MoveSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()

			winner = check_winner(id)
			if winner:
				game = get_object_or_404(Game, pk=id)
				game.winner = User.objects.get(username=winner)
				game.finished = datetime.now()
				game.save()
			return Response({"move": serializer.data, "winner": winner}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Accepted(APIView):
	def post(self, request, format=None):
		if not 'request-id' in request.data:
			return Response({"details": "request-id is required"}, status=status.HTTP_400_BAD_REQUEST)

		req = get_object_or_404(GameRequest, pk=request.data['request-id'])
		
		game = Game()
		game.player_a = req.requesting
		game.player_b = req.requested
		game.save()
		game_ser = GameSerializer(game)

		req.delete()
		return Response(game_ser.data, status=status.HTTP_201_CREATED)


"""0 1 2
   3 4 5
   6 7 8
"""
win_sequences = (
	(0,1,2,), (3,4,5,), (6,7,8,),
	(0,3,6,), (1,4,7,), (2,5,8,),
	(0,4,8,), (2,4,6,),
)
def check_winner(game_id):
	moves = Move.objects.all().filter(game_id=game_id)
	board = [None for i in range(9)]
	for m in moves:
		board[m.position] = m.player.username

	for s in win_sequences:
		if board[s[0]] is not None and board[s[0]] == board[s[1]] and board[s[0]] == board[s[2]]:
			return board[s[0]]
	return None



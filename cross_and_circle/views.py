from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q

from models import *
from serializers import * 
from permissions import *

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.exceptions import *

from datetime import datetime
from uuid import uuid4

class Token(APIView):
	def get(self, request):
		token = uuid4()
		return Response({"token": token})

# all
class Players(ListCreateAPIView):
	permission_classes = (permissions.AllowAny,)
	queryset = User.objects.all()
	serializer_class = PlayerSerializer
	lookup_field = 'username'

	def perform_create(self, serializer):
		check_poe_tocken(self.request)
		serializer.save()


# read for all, modify for owner
class PlayerDetails(RetrieveUpdateAPIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsCurrentPlayerOrReadOnly)
	queryset = User.objects.all()
	serializer_class = PlayerSerializer
	lookup_field = 'username'


# all
class PlayerGames(ListAPIView):
	permission_classes = (permissions.AllowAny,)
	serializer_class = GameSerializer
	lookup_url_kwarg = 'username'

	def get_queryset(self):
		username = self.kwargs.get(self.lookup_url_kwarg)
		player = get_object_or_404(User, username=username)
		params = {}
		in_progress = self.request.query_params.get('in_progress', None)
		if in_progress:
			params['finished'] = None

		if 'opponent' in self.request.query_params:
			opponent = get_object_or_404(User, username=self.request.query_params['opponent'])
			games = Game.objects.all().filter(Q(player_a=player) | Q(player_b=player), Q(player_a=opponent) | Q(player_b=opponent), **params)
		else:
			games = Game.objects.all().filter(Q(player_a=player) | Q(player_b=player), **params)
		return games


# all
class PlayerStats(APIView):
	permission_classes = (permissions.AllowAny,)

	def get(self, request, username, format=None):
		player = get_object_or_404(User, username=username)
		
		if 'opponent' in request.query_params:
			opponent = get_object_or_404(User, username=request.query_params['opponent'])
			games = Game.objects.all().filter(Q(player_a=player) | Q(player_b=player), Q(player_a=opponent) | Q(player_b=opponent)).exclude(finished=None)
		else:
			games = Game.objects.all().filter(Q(player_a=player) | Q(player_b=player)).exclude(finished=None)

		all_games = len(games)
		won_games = len(games.filter(winner=player))
		draws = len(games.filter(winner=None, finished__isnull=False))
		lost_games = all_games - won_games - draws

		return Response({"games": all_games, "won": won_games, "lost": lost_games, "draws": draws})


# all
class Games(ListAPIView):
	permission_classes = (permissions.AllowAny,)
	serializer_class = GameSerializer

	def get_queryset(self):
		params = {}
		if 'player_a' in self.request.query_params:
			params['player_a'] = get_object_or_404(User, username=self.request.query_params['player_a'])
		if 'player_b' in self.request.query_params:
			params['player_b'] = get_object_or_404(User, username=self.request.query_params['player_b'])
		
		in_progress = self.request.query_params.get('in_progress', None)
		if in_progress:
			params['winner'] = None
		elif in_progress is not None:
			return Game.objects.all().filter(**params).exclude(winner=None)

	 	return Game.objects.all().filter(**params)


# all
class GameDetails(RetrieveAPIView):
	permission_classes = (permissions.AllowAny,)
	queryset = Game.objects.all()
	serializer_class = GameSerializer


# authenticated
class Requests(ListCreateAPIView):
	serializer_class = GameRequestSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	def get_queryset(self):
		params = {}
		if 'requesting' in self.request.query_params:
			params['requesting'] = get_object_or_404(User, username=self.request.query_params['requesting'])
		if 'requested' in self.request.query_params:
			params['requested'] = get_object_or_404(User, username=self.request.query_params['requested'])
		return GameRequest.objects.all().filter(**params)

	def perform_create(self, serializer):
		check_poe_tocken(self.request)
		serializer.save(requesting=self.request.user)


# read for authenticated, delete for requesting or requested
class RequestDetails(RetrieveDestroyAPIView):
	queryset = GameRequest.objects.all()
	serializer_class = GameRequestSerializer
	permission_classes = (permissions.IsAuthenticated, IsRequestedOrRequesting)


# read for all, create for players of game
class Moves(APIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def get(self, request, pk, format=None):
		game = get_object_or_404(Game, pk=pk)
		moves = Move.objects.all().filter(game=game)
		serializer = MoveSerializer(moves, many=True)
		return Response(serializer.data)

	def post(self, request, pk, format=None):
		request.data['game'] = pk
		request.data['player'] = request.user
		serializer = MoveSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()

			winner = check_winner(pk)
			if winner:
				game = get_object_or_404(Game, pk=pk)
				if winner != "No Winner":
					game.winner = User.objects.get(username=winner)
				game.finished = datetime.now()
				game.save()
			return Response({"move": serializer.data, "winner": winner}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# requested only
class Accepted(APIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	def post(self, request, format=None):
		if not 'request-id' in request.data:
			print request.data
			return Response({"detail": "request-id is required"}, status=status.HTTP_400_BAD_REQUEST)

		req = get_object_or_404(GameRequest, pk=request.data['request-id'])
		if is_requested(request, req):
			game = Game()
			game.player_a = req.requesting
			game.player_b = req.requested
			game.save()
			game_ser = GameSerializer(game, context={"request": request})

			req.delete()
			return Response(game_ser.data, status=status.HTTP_201_CREATED)
		else:
			return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)


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

	if len(list(moves)) == 9:
		return "No Winner"
	return None


def check_poe_tocken(request):
	if 'token' not in request.query_params:
		raise MethodNotAllowed("POST", detail="POE token missing")

	token = POEToken(token=request.query_params['token'])

	try:
		token.save()
	except Exception as e:
		raise MethodNotAllowed("POST", detail="POE token duplication")



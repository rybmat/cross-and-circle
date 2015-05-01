from rest_framework import permissions

class IsCurrentPlayerOrReadOnly(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		else:
			return obj == request.user

class IsRequestedOrRequesting(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		else:
			return request.user in (obj.requesting, obj.requested,)

# class IsRequested(permissions.BasePermission):
# 	def has_object_permission(self, request, view, obj):
# 		if request.method in permissions.SAFE_METHODS:
# 			return True
# 		else:
# 			return request.user == obj.requested

# class IsGamePlayer(permissions.BasePermission):
# 	def has_object_permission(self, request, view, obj):
# 		if request.method in permissions.SAFE_METHODS:
# 			return True
# 		else:
# 			return request.user == obj.game.player_a or request.user == obj.game.player_b


def is_requested(request, obj):
	return request.user == obj.requested

def is_game_player(request, game):
	return request.user in (obj.game.player_a, obj.game.player_b,)
'use strict';

/* Services */

var cacServices = angular.module('cacServices', ['ngWebSocket']);
	cacServices.factory('WebSock', ['$websocket',
		function($websocket) {
			var dataStream = $websocket('ws://localhost:8880/ws');

			var methods = {
		      	send: function(data) {
		      		dataStream.send(JSON.stringify(data));
		      	},
		      	onMessage: function(foo) {
		      		return dataStream.onMessage(foo);
		      	}
		    };
		    return methods;
		}]);

	cacServices.factory('GameRequests', ['$localStorage', 'Restangular', 
		function($localStorage, Restangular) {
			var resource = Restangular.one('requests/');

			var methods = {
				send: function(opponent, poeToken) {
					var payload = {requested: opponent};
					var h = {'Authorization': 'Token ' + $localStorage.loggedUserToken};
					return resource.post('', payload, {"token": poeToken}, h);
				},
				getList: function(pageNum) {
					return resource.get({page: pageNum, requested: $localStorage.loggedUsername});
				},
				accept: function(reqId) {
					var h = {'Authorization': 'Token ' + $localStorage.loggedUserToken};
					return Restangular.all('accepted-requests/').post({"request-id": reqId}, {}, h);
				}
			}

			return methods;
		}]);

	cacServices.factory('AuthToken', ['Restangular', 
		function (Restangular) {
			var methods = {
				get: function(uname, pass) {
					return Restangular.all('api-token-auth/').post(
						{"username": uname, "password": pass});
				}
			}
			return methods;
		}]);

	cacServices.factory('PoeToken', ['Restangular', 
		function (Restangular) {
			var poeTokenRes = Restangular.one('token/');

			var methods = {
				get: function() {
					return poeTokenRes.get();
				}
			}
			return methods;
		}]);

	cacServices.factory('Players', ['Restangular', 
		function (Restangular) {

			var methods = {
				get: function(uname) {
					return Restangular.one('players/' + uname + '/').get();
				},
				stats: function(uname) {
					return Restangular.one('players/' + uname+ '/stats/').get();
				},
				create: function(user, poe) {
					return Restangular.all('players/').post(
						user, {token: poe});
				},
				games: function(uname, p) {
					return Restangular.one('players/' + uname+ '/games/?in_progress=true').get({page: p});
				}
			}

			return methods;
		}]);

	cacServices.factory('Game', ['$localStorage', 'Restangular', 
		function ($localStorage, Restangular) {
			var resource = Restangular.one('games/');

			var methods = {
				get: function(id) {
					return Restangular.one('games/' + id + '/').get();
				},

				moves: function(id) {
					return Restangular.one('games/' + id + '/moves/').get();
				},

				makeMove: function(gameId, position) {
					var h = {'Authorization': 'Token ' + $localStorage.loggedUserToken};
					return Restangular.all('games/' + gameId + '/moves/').post({"position": position}, {}, h);
				}
			}

			return methods;
		}]);
	
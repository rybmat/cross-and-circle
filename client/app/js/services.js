'use strict';

/* Services */

var cacServices = angular.module('cacServices', ['ngWebSocket']);
	cacServices.factory('WebSock', ['$websocket',
		function($websocket) {
			var dataStream = $websocket('ws://localhost:8880/ws');

			dataStream.onMessage(function(message) {
		        console.log(message);
	      	});

			var methods = {
		      	send: function(data) {
		      		dataStream.send(JSON.stringify(data));
		      	}
		    };
		    return methods;
		}]);

	cacServices.factory('GameRequests', ['$localStorage', 'Restangular', 
		function($localStorage, Restangular) {
			var resource = Restangular.one('requests/');
			var h = {'Authorization': 'Token ' + $localStorage.loggedUserToken};

			var methods = {
				send: function(opponent, poeToken) {
					var payload = {requested: opponent};

					return resource.post('', payload, {"token": poeToken}, h);
				},
				getList: function(pageNum) {
					return resource.get({page: pageNum, requested: $localStorage.loggedUsername});
				},
				accept: function(reqId) {
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
				}
			}

			return methods;
		}]);
	
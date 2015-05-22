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

	cacServices.factory('Auth', ['WebSock', function(WebSock) {
		var username = null;
		var token = null;

		// TODO: use locall storage maybe?
		var methods = {
			getToken: function() {
				return token;
			},
			setToken: function(t) {
				token = t;
			},
			getUsername: function() {
				return username;
			},
			setUsername: function(u) {
				username = u;
				WebSock.send({type: "hello", username: u});	// register user at websocket server
			}
		}
		return methods;
	}]);

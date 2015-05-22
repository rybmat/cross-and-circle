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
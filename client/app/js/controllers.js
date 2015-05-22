'use strict';

/* Controllers */

var cacControllers = angular.module('cacControllers', []);
	
	cacControllers.controller('LoginCtrl', ['$scope', 'Restangular', 'Auth', 
		function($scope, Restangular, Auth) {
			var tokenRes = Restangular.all('api-token-auth/');

			$scope.login = function(username, password) {
				tokenRes.post({"username":$scope.username, "password":$scope.password}).then(function(resp) {
							console.log("token", resp.token);
				 	$scope.errors = null;
					Auth.setUsername($scope.username);
					Auth.setToken(resp.token);
					// TODO: redirect
				}, function(resp) {
				  	console.log(resp);
					$scope.errors = resp.data.non_field_errors;
				});

			}
		}]);

	cacControllers.controller('RegisterCtrl', ['$scope', '$window', 'Restangular', 'Auth', 
		function($scope, $window, Restangular, Auth) {
			$scope.master = {};

			var poeTokenRes = Restangular.one('token/');
			var usersRes = Restangular.all('players/');

			var poeToken = null;
			poeTokenRes.get().then(function(resp) {
				poeToken = resp.token
				console.log(resp.token);
			}, function(resp) {	
				$scope.errors = resp.data;
				console.log(resp);
			});

			$scope.register = function(user) {
				$scope.$broadcast('show-errors-check-validity');

				if (!this.form.$valid){ console.log('form invalid'); return;}
				usersRes.post(user, {token: poeToken}).then(function(resp) {
					console.log(resp);
					$window.location.href = '/app/#login';
				}, function(resp) {
					$scope.errors = resp.data;
					console.log(resp);
				});
			}
		}]);




'use strict';

/* Controllers */

var cacControllers = angular.module('cacControllers', []);
	
	cacControllers.controller('MainCtrl', ['$location', '$scope', 'Restangular',
		function($location, $scope, Restangular) {
			$scope.loggedUsername = null;
			$scope.loggedUserToken = null;
			$scope.loggedIn = false;


			// TODO: try to read from local storage
			
			$scope.$watch(function() { return $location.path(); }, function(newValue, oldValue){  
			    if ($scope.loggedIn == false && newValue != '/register'){  
			            $location.path('/register');  
			    }  
			});

			var tokenRes = Restangular.all('api-token-auth/');

			$scope.login = function(username, password) {
				tokenRes.post({"username":username, "password":password}).then(function(resp) {
							
				 	$scope.errors = null;
					$scope.loggedUsername = username;
					$scope.loggedUserToken = resp.token;
					$scope.loggedIn = true;

					console.log("token", $scope.loggedUserToken);
					$location.path('/login');
					console.log('aaa');
				}, function(resp) {
				  	console.log(resp);
					$scope.loginErrors = resp.data;
				});

			}
		}])


	cacControllers.controller('LoginCtrl', ['$scope', 'Restangular', 
		function($scope, Restangular) {
			$scope.signIn = function() {
				$scope.$broadcast('show-errors-check-validity');
				if (!this.form.$valid){ console.log('form invalid'); return;}

				$scope.login($scope.username, $scope.password);
			}
		}]);

	cacControllers.controller('RegisterCtrl', ['$scope', '$location', 'Restangular', 
		function($scope, $location, Restangular) {
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
					$scope.login(user.username, user.password);
				}, function(resp) {
					$scope.errors = resp.data;
					console.log(resp);
				});
			}
		}]);




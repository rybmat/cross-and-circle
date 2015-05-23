'use strict';

/* Controllers */

var cacControllers = angular.module('cacControllers', []);
	
	cacControllers.controller('MainCtrl', ['$localStorage', 'WebSock', '$location', '$scope', 'Restangular',
		function($localStorage, WebSock, $location, $scope, Restangular) {
			// $scope.loggedUsername = null;
			// $scope.loggedUserToken = null;
			// $scope.loggedIn = false;

			$scope.storage = $localStorage;
			
			$scope.$watch(function() { return $location.path(); }, function(newValue, oldValue){  
			    if ($scope.storage.loggedIn == false && newValue != '/register'){  
			            $location.path('/register');  
			    }  
			});

			var tokenRes = Restangular.all('api-token-auth/');

			$scope.login = function(username, password) {
				tokenRes.post({"username":username, "password":password}).then(function(resp) {
							
				 	$scope.errors = null;
					$scope.storage.loggedUsername = username;
					$scope.storage.loggedUserToken = resp.token;
					$scope.storage.loggedIn = true;
					WebSock.send({type: "hello", username: username});
					//TODO: remember in local storage

					console.log("token", $scope.storage.loggedUserToken);
					$location.path('/menu');
				}, function(resp) {
				  	console.log(resp);
					$scope.loginErrors = resp.data;
				});

				//TODO: listen for messages and do sth
			}

			$scope.logout = function() {
				WebSock.send({type: "bye", username: $scope.loggedUsername});
				$scope.storage.loggedUsername = null;
				$scope.storage.loggedUserToken = null;
				$scope.storage.loggedIn = false;

				$location.path('/register');

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

	cacControllers.controller('MenuCtrl', ['$scope', 'Restangular', 
		function($scope, Restangular) {
			$scope.items = [];	// should contain at least {key: , value:}
			var statsRes = Restangular.one('players/' + $scope.storage.loggedUsername + '/stats/');

			$scope.stats = function() {
				statsRes.get().then(function(resp) {
					console.log(resp);
					$scope.items = [{key:"Games total", value:resp.games}, 
						{key:"Won", value:resp.won},
						{key:"Lost", value:resp.lost}];
				});
			}
		}]);




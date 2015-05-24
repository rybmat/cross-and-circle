'use strict';

/* Controllers */

var cacControllers = angular.module('cacControllers', []);
	
	cacControllers.controller('MainCtrl', ['$localStorage', 'WebSock', '$location', '$scope', 'AuthToken',
		function($localStorage, WebSock, $location, $scope, AuthToken) {

			$scope.storage = $localStorage;
			
			$scope.$watch(function() { return $location.path(); }, function(newValue, oldValue){  
			    if ($scope.storage.loggedIn == false && newValue != '/register'){  
			            $location.path('/register');  
			    }  
			});

			$scope.login = function(username, password) {
				AuthToken.get(username, password).then(function(resp) {			
				 	$scope.errors = null;
					$scope.storage.loggedUsername = username;
					$scope.storage.loggedUserToken = resp.token;
					$scope.storage.loggedIn = true;
					WebSock.send({type: "hello", username: username});

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

	cacControllers.controller('LoginCtrl', ['$scope', 
		function($scope) {
			$scope.signIn = function() {
				$scope.$broadcast('show-errors-check-validity');
				if (!this.form.$valid){ console.log('form invalid'); return;}

				$scope.login($scope.username, $scope.password);
			}
		}]);

	cacControllers.controller('RegisterCtrl', ['Players', 'PoeToken', '$scope', '$location', 
		function(Players, PoeToken, $scope, $location) {
			$scope.master = {};

			var poeToken = null;
			PoeToken.get().then(function(resp) {
				poeToken = resp.token
				console.log(resp.token);
			}, function(resp) {	
				$scope.errors = resp.data;
				console.log(resp);
			});

			$scope.register = function(user) {
				$scope.$broadcast('show-errors-check-validity');

				if (!this.form.$valid){ console.log('form invalid'); return;}
				Players.create(user, poeToken).then(function(resp) {
					console.log(resp);
					$scope.login(user.username, user.password);
				}, function(resp) {
					$scope.errors = resp.data;
					console.log(resp);
				});
			}
		}]);

	cacControllers.controller('MenuCtrl', ['Players', 'PoeToken', 'GameRequests', '$scope', 
		function(Players, PoeToken, GameRequests, $scope) {
			$scope.items = [];	// should contain at least {key: , value:, foo:""}
			
			$scope.stats = function() {
				$scope.head = "Your stats";
				$scope.showForm = null;
				Players.stats($scope.storage.loggedUsername).then(function(resp) {
					console.log(resp);
					$scope.items = [{key:"Games total", value:resp.games}, 
						{key:"Won", value:resp.won},
						{key:"Lost", value:resp.lost}];
				});
			}
			
			$scope.newGame = function() {
				$scope.head = "New game";
				$scope.showForm = "true";
				$scope.opponent = "";
				$scope.errors = []
				PoeToken.get().then(function(resp) {
					$scope.poeToken = resp.token;
					console.log('token', resp.token);
				}, function(resp) {	
					$scope.errors = ['Error has occured, please contact with support.'];
					console.log(resp);
				});
			}

			$scope.makeRequest = function() {
				if (!this.form.$valid){ console.log('form invalid'); return;}
				if ($scope.opponent == $scope.storage.loggedUsername) {
					$scope.errors = ['You can not send request to yourself!'];
					return;
				}

				Players.get($scope.opponent).then(function(resp) {
					GameRequests.send($scope.opponent, $scope.poeToken).then(
						function(resp) {
							$scope.errors = ['Request sent! Please wait for accepting the request.'];
						}, function(resp) {
							$scope.errors = ['Error has occured, please contact with support.'];
							console.log(resp);
						});
				}, function(resp) {
					$scope.errors = ['Such player does not exists'];
				});
			}

			$scope.getPage = function(foo, next) {
				$scope.items = [];
					if (next == true) {
						$scope.page += 1;
					} else if ($scope.page > 1) {
						$scope.page -= 1;
					}
					foo();
		
			}

			$scope.pendingRequests = function() {
				$scope.showForm = "";
				$scope.head = "Pending requests";
				$scope.errors = []
				$scope.page = 0;

				var page = function() {
					GameRequests.getList($scope.page).then(function(resp) {
						resp.results.forEach(function(item) {
							$scope.items.push(
									{key: item.requesting, value: null, foo: $scope.acceptRequest, obj: item}
								);
						}, function() {
							$scope.page -= 1;
						});
					});
				}
				$scope.pageFoo = page;
				$scope.getPage(page, true);
			}

			$scope.acceptRequest = function(i) {
				console.log("accept");
			}

		}]);



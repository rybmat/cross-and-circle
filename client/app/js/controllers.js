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

			if ($scope.storage.loggedUsername) {
				WebSock.send({type: "hello", username: $scope.storage.loggedUsername});	
			}

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
				WebSock.send({type: "bye", username: $scope.storage.loggedUsername});
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

	cacControllers.controller('MenuCtrl', ['$location', 'Players', 'PoeToken', 'GameRequests', '$scope', 
		function($location, Players, PoeToken, GameRequests, $scope) {
			$scope.items = [];	// should contain at least {key: , value:, foo:""}
			
			$scope.stats = function() {
				$scope.head = "Your stats";
				$scope.view = 'list';
				$scope.showPager = null;
				Players.stats($scope.storage.loggedUsername).then(function(resp) {
					$scope.items = [{key:"Games total", value:resp.games}, 
						{key:"Won", value:resp.won},
						{key:"Lost", value:resp.lost}];
				});
			}
			
			$scope.newGame = function() {
				$scope.head = "New game";
				$scope.opponent = "";
				$scope.errors = []
				$scope.view = 'form';

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

			$scope.nextPage = function() {
				$scope.items = [];
				$scope.page += 1;			
				$scope.pageFoo();
			}

			$scope.prevPage = function() {
				if ($scope.page <= 1) {return;}
				$scope.items = [];
				$scope.page -= 1;			
				$scope.pageFoo();
			}

			$scope.pendingRequests = function() {
				$scope.view = 'list';
				$scope.head = "Pending requests";
				$scope.errors = []
				$scope.page = 0;
				$scope.showPager = true;

				$scope.pageFoo = function() {
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
				$scope.nextPage();
			}

			$scope.acceptRequest = function(i) {
				GameRequests.accept(i.obj.id).then(function(resp) {
					console.log(resp);
					// TODO: redirect to game page
				}, function(resp) {
					console.log(resp);
				});
			}

			$scope.gamesInProgress = function() {
				$scope.view = 'list';
				$scope.head = "Your Games in Progress";
				$scope.errors = []
				$scope.page = 0;
				$scope.showPager = true;

				$scope.pageFoo = function() {
					Players.games($scope.storage.loggedUsername, $scope.page).then(function(resp) {
						resp.results.forEach(function(item) {
							$scope.items.push(
									{key: item.player_a + ' vs ' + item.player_b, value: null, foo: $scope.continueGame, obj: item}
								);
						}, function() {
							$scope.page -= 1;
						});
					});
				}
				$scope.nextPage();
			}

			$scope.continueGame = function(i) {
				$location.path('/game/' + i.obj.id);
			}
		}]);

	cacControllers.controller('GameCtrl', ['Game', '$window', '$scope', '$routeParams', 
		function(Game, $window, $scope, $routeParams) {
			$scope.gameId = $routeParams.gameId;

			var canvas_elem = $window.document.getElementById("board");
			var field_height = canvas_elem.height / 3;
			var field_width = canvas_elem.width / 3;
			canvas_elem.onmousedown = onMouseClick;
			var ctx = canvas_elem.getContext("2d");
			drawBoard();

			Game.get($scope.gameId).then(function(resp) {
				$scope.player_a = resp.player_a;
				$scope.player_b = resp.player_b;
				console.log(resp);
			}, function(resp) {
				console.log(resp);
			});

			var board = [[null, null, null], [null, null, null], [null, null, null]];
			Game.moves($scope.gameId).then(function(resp) {
				resp.forEach(function(move) {
					if (move.player == $scope.storage.loggedUsername) {
						drawCircle($window.Math.floor(move.position / 3), move.position % 3);
					} else {
						drawCross($window.Math.floor(move.position / 3), move.position % 3);
					}
				});
				console.log(resp);
			}, function(resp) {
				console.log(resp);
			})

			function drawBoard() {
				var offset = 5;
				
				ctx.lineCap = "round";
				ctx.strokeStyle = "black";
				ctx.lineWidth = 3;
				ctx.beginPath();


				ctx.moveTo(field_width, offset);
				ctx.lineTo(field_width, canvas_elem.height - offset);

				ctx.moveTo(2*field_width, offset);
				ctx.lineTo(2*field_width, canvas_elem.height - offset);
				
				ctx.moveTo(offset, field_height);
				ctx.lineTo(canvas_elem.width - offset, field_height);

				ctx.moveTo(offset, 2*field_height);
				ctx.lineTo(canvas_elem.width - offset, 2*field_height);

				ctx.stroke();
				ctx.closePath();
			}

			function drawCross(row, col) {
				var offset = 0.2;
				var left = col * field_width + offset * field_width;
				var right = (col + 1) * field_width - offset * field_width;
				var top = row * field_height + offset * field_height;
				var bottom = (row + 1) * field_height  - offset * field_height;

				ctx.strokeStyle = "red";
				ctx.lineCap = "round";
				ctx.lineWidth = 10;

				ctx.beginPath();
				ctx.moveTo(left, top);
				ctx.lineTo(right, bottom);

				ctx.moveTo(right, top);
				ctx.lineTo(left, bottom);

				ctx.stroke();
				ctx.closePath();
			}

			function drawCircle(row, col) {
				var offset = 0.2;
				var x = col * field_width + 0.5 * field_width;
				var y = row * field_height + 0.5 * field_height;
				var rx = (field_width / 2) - (offset * field_width);
				var ry = (field_height / 2) - (offset * field_height);

				ctx.strokeStyle = "green";
				ctx.lineWidth = 10;

				ctx.beginPath();

				ctx.arc(x, y, rx, 0, Math.PI * 2, false);

				ctx.stroke();
				ctx.closePath();
			}

			function onMouseClick(e) {
				var row = Math.floor((e.pageY - canvas_elem.offsetTop) / field_height);
				var column = Math.floor((e.pageX - canvas_elem.offsetLeft) / field_width);
			 	drawCircle(row, column);
			}

		}]);



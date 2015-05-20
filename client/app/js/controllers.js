'use strict';

/* Controllers */

var cacControllers = angular.module('cacControllers', []);
	
	cacControllers.controller('LoginCtrl', ['$scope', 'Restangular', 'WebSock', 'Auth', 
		function($scope, Restangular, WebSock, Auth) {
			var tokenRes = Restangular.all('api-token-auth/');

			$scope.login = function(username, password) {
				tokenRes.post({"username":$scope.username, "password":$scope.password}).then(function(resp) {
							console.log("token", resp.token);
				 	$scope.errors = null;
					Auth.setUsername($scope.username);
					Auth.setToken(resp.token);
				}, function(resp) {
				  			console.log(resp);
					$scope.errors = resp.data.non_field_errors;
				});

			}
		}]);





// phonecatControllers.controller('PhoneListCtrl', ['$scope', 'Phone',
//   function($scope, Phone) {
//     $scope.phones = Phone.query();
//     $scope.orderProp = 'age';
//   }]);

// phonecatControllers.controller('PhoneDetailCtrl', ['$scope', '$routeParams', 'Phone',
//   function($scope, $routeParams, Phone) {
//     $scope.phone = Phone.get({phoneId: $routeParams.phoneId}, function(phone) {
//       $scope.mainImageUrl = phone.images[0];
//     });

//     $scope.setImage = function(imageUrl) {
//       $scope.mainImageUrl = imageUrl;
//     }
//   }]);

'use strict';

/* Controllers */

var cacControllers = angular.module('cacControllers', []);
	
	cacControllers.controller('LoginCtrl', ['$scope', 'Restangular', function($scope, Restangular) {
		var tokenRes = Restangular.all('api-token-auth/');

		$scope.login = function(username, password) {
			tokenRes.post({"username":$scope.username, "password":$scope.password}).then(function(resp) {
			   console.log("token", resp.token);
			 }, function() {
			  console.log("There was an error saving");
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

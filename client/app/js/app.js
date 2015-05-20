'use strict';

/* App Module */

var crossAndCircle = angular.module('crossAndCircle', [
  'ngRoute',
  'cacControllers',
  'cacServices',
  'restangular',
  'ngWebSocket',
]);

crossAndCircle.config(['$routeProvider', 'RestangularProvider',
  function($routeProvider, RestangularProvider) {
    $routeProvider.
      when('/login', {
        templateUrl: 'partials/login.html',
        controller: 'LoginCtrl'
      }).
      otherwise({
        redirectTo: '/login'
      });

      RestangularProvider.setBaseUrl('http://127.0.0.1:8888/rest/');
      //RestangularProvider.setRequestSuffix('.json');
      RestangularProvider.setDefaultHeaders({"Content-Type": "application/json"});
  }]);

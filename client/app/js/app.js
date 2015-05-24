'use strict';

/* App Module */

var crossAndCircle = angular.module('crossAndCircle', [
  'ngRoute',
  'cacDirectives',
  'cacControllers',
  'cacServices',
  'restangular',
  'ngWebSocket',
  'ngStorage',
  'ngResource'
]);

crossAndCircle.config(['$routeProvider', 'RestangularProvider', 
  function($routeProvider, RestangularProvider) {
    $routeProvider.
      when('/register', {
        templateUrl: 'partials/register.html',
        
      }).
      when('/menu', {
        templateUrl: 'partials/menu.html',
        controller: 'MenuCtrl'
      }).
      otherwise({
        redirectTo: '/register'
      });

      RestangularProvider.setBaseUrl('http://127.0.0.1:8888/rest/');
      //RestangularProvider.setRequestSuffix('.json');
      RestangularProvider.setDefaultHeaders({"Content-Type": "application/json"});
  }]);

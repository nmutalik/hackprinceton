// Declare app level module which depends on filters, and services
angular.module('snap-ui', ['ngResource', 'ngRoute', 'ui.bootstrap', 'ui.date'])
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/home/home.html', 
        controller: 'HomeController'})
      .when('/settings', {
        templateUrl: 'views/settings/settings.html', 
        controller: 'SettingsController'})
      .otherwise({redirectTo: '/'});
  }]);

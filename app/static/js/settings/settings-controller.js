angular.module('snap-ui')
  .controller('SettingsController', ['$scope', '$http', function($scope, $http) {
    var refreshFriends = function() {
      $http.get('/api/friends').then(
        function(response) {
          $scope.friends = response.data;
        });
    }

    refreshFriends();

    $scope.add = function() {
      $http.get('api/add/' + $scope.query.$).then(
        refreshFriends);
    };



    $scope.remove = function(friend) {
      $http.get('api/remove/' + friend.name).then(
        refreshFriends); 
    };
  }]);

angular.module('snap-ui')
  .controller('HomeController', ['$scope', '$http', '$interval', function($scope, $http, $interval) {
    var rawSnaps;
    
    $scope.numColumns = 4;

    $scope.refresh = function() {
      $http.get('/api/snaps').then(
        function(response) {
          rawSnaps = response.data;
          $scope.snaps = _.chunk(response.data, $scope.numColumns);
        });
    }

    $scope.refresh();
    
    $interval($scope.refresh, 5000);

    var pop = function(major, minor) {
      var output = rawSnaps.splice(major * $scope.numColumns + minor, 1)[0];
      $scope.snaps = _.chunk(rawSnaps, $scope.numColumns);
      return output;
    }

    $scope.accept = function(major, minor) {
      var accepted = pop(major, minor);
      $http.post('/api/accept/', accepted).then(
        function (response) {
          console.log(response);
        });
    }

    $scope.reject = function(major, minor) {
      var rejected = pop(major, minor);
      $http.post('/api/reject/', rejected).then(
        function (response) {
          console.log(response);
        });
    }
  }]);

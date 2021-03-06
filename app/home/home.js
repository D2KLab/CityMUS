(function(angular) {
  'use strict';

  angular.module('myApp.home', [])

    // Controller
    .controller('HomeCtrl', ['$scope', '$location', '$log', 'Geolocation', 'watchOptions', 'Recommendation', 'shareRecommendation', '$window', '$rootScope', 'NICE',
      function($scope, $location, $log, Geolocation, watchOptions, Recommendation, shareRecommendation, $window, $rootScope, NICE) {
        $rootScope.iframeClass = "iframe_container_1";
        $scope.selectedTrack = false;
        $scope.flag_select = false;


        $scope.$watch(Recommendation.getTracks, function() {
          $scope.songList = Recommendation.getTracks();
          $scope.flag_select = !!Object.values($scope.songList).length;

        });


        $scope.visualizePath = function() {
          $location.path('/visualization');
        };

        $scope.$watch('selectedSong', function(newValue, oldValue) {

          if (newValue != oldValue) {
            if (!newValue) {
              $scope.selectedTrack = false;
              return;
            }
            $scope.selectedTrack = true;
            for (var value of $scope.songList) {
              //console.log(key);
              if (value.label == newValue.label) {
                shareRecommendation.setPath(newValue.label, value.path);
                break;
              }
            }
          }

        });

      }
    ]);
})(angular);

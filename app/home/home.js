(function(angular) {
  'use strict';

  angular.module('myApp.home', [])

    // Controller
    .controller('HomeCtrl', ['$scope', '$location', '$log', 'Geolocation', 'watchOptions', 'Recommendation', 'shareRecommendation', '$window', '$rootScope',
      function($scope, $location, $log, Geolocation, watchOptions, Recommendation, shareRecommendation, $window, $rootScope) {
        $rootScope.iframeClass = "big_playlist";
        //console.log(watchOptions)
        $scope.selectedTrack = false;
        $scope.flag_select = false;
        $scope.$watch(Recommendation.getTracks, function() {
          $scope.songList = Recommendation.getTracks();
          $scope.flag_select = !!Object.values($scope.songList).length;
          if ($scope.flag_select){
          }
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

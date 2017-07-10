(function(angular) {
  'use strict';

  angular.module('myApp.home', [])

    // Controller
    .controller('HomeCtrl', ['$scope', '$location', '$log', 'Geolocation', 'watchOptions', 'Recommendation', 'shareRecommendation', '$window', '$rootScope',
      function($scope, $location, $log, Geolocation, watchOptions, Recommendation, shareRecommendation, $window, $rootScope) {
        $scope.spinner_visible = true;
        $rootScope.iframeClass = "big_playlist";
        //console.log(watchOptions)
        $scope.selectedTrack = false;
        $scope.flag_select = false;
        $scope.$watch(Recommendation.getTracks, function() {
          $scope.songList = Recommendation.getTracks();
          if ($scope.songList.length > 0) $scope.flag_select = true;
        });


        $scope.visualizePath = function() {
          $location.path('/visualization');
        }




        $scope.$watch('selectedSong', function(newValue, oldValue) {

          if (newValue != oldValue) {
            $scope.spinner_visible = false;
            if (newValue == null) {
              $scope.selectedTrack = false;
            } else {
              $scope.selectedTrack = true;
              for (var key in $scope.songList) {
                //console.log(key);
                if ($scope.songList[key].label == newValue.label) {
                  shareRecommendation.setPath(newValue.label, $scope.songList[key].path);
                  break;
                }
              }
            }

          }

        });

      }
    ]);
})(angular);

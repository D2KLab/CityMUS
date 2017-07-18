(function(angular) {

  'use strict';

  angular.module('myApp.visualization', [])

    // Controller
    .controller('VisualizationCtrl', ['$scope', '$location', '$log', 'Geolocation', 'watchOptions', 'Recommendation', 'shareRecommendation', '$mdDialog', '$window', '$rootScope',
      function($scope, $location, $log, Geolocation, watchOptions, Recommendation, shareRecommendation, $mdDialog, $window, $rootScope) {
        $rootScope.iframeClass = "iframe_container_2";
        $scope.data_link = shareRecommendation.getPath();

        $scope.drawEnable = true;

        $scope.inspect = function(link) {
          window.open(link, '_blank', 'location=yes,height=570,width=520,scrollbars=yes,status=yes');
        };

        $scope.songList = Recommendation.getTracks();

        $scope.$watch(Recommendation.getTracks, function() {
          $scope.songList = Recommendation.getTracks();
          var artistList = {};
          var poiList = {};
          for (var song of $scope.songList) {
            var artist = song.path[0];
            var artist_name = shareRecommendation.changeStringStyle(artist, 0)[1];
            var poi = song.path[12];
            var poi_name = shareRecommendation.changeStringStyle(poi, 12)[1];
            if (artist in artistList) artistList[artist].uri_ref.push(poi);
            else {
              artistList[artist] = {};
              artistList[artist].uri = artist;
              artistList[artist].name = artist_name;
              artistList[artist].uri_ref = [poi];
              artistList[artist].active = true;
            }
            if (poi in poiList) poiList[poi].uri_ref.push(artist);
            else {
              poiList[poi] = {};
              poiList[poi].uri = poi;
              poiList[poi].name = poi_name;
              poiList[poi].uri_ref = [artist];
              poiList[poi].active = true;
            }
            //song
          }
          var artistList_arr = Object.values(artistList);
          var poiList_arr = Object.values(poiList);

          $scope.artistData = {
            availableOptions: artistList_arr
          };

          $scope.poiData = {
            availableOptions: poiList_arr
          };

          if ($scope.data_link[0]) {
            $scope.track = $scope.data_link[0];
            $scope.path = $scope.data_link[1];

            for (let i = 0; i < $scope.artistData.availableOptions.length; i++) {
              if ($scope.artistData.availableOptions[i].uri == $scope.path[0].link) {
                $scope.artistData.selectedOption = $scope.artistData.availableOptions[i];
              }
            }
            for (let i = 0; i < $scope.poiData.availableOptions.length; i++) {
              if ($scope.poiData.availableOptions[i].uri == $scope.path[$scope.path.length - 1].link) {
                $scope.poiData.selectedOption = $scope.poiData.availableOptions[i];
              }
            }

          }
        });

        $scope.evaluateOption = function(artist) {
          return false;
        };

        $scope.changeActive = function(option) {
          var active_poi = [];
          var active_artists = [];
          if (option == 1) {
            if ($scope.artistData.selectedOption) {
              for (let i = 0; i < $scope.poiData.availableOptions.length; i++) {
                let curOption = $scope.poiData.availableOptions[i];
                if (curOption.uri_ref.indexOf($scope.artistData.selectedOption.uri) < 0)
                  curOption.active = false;
                else {
                  active_poi.push(i);
                  curOption.active = true;
                }
              }
            } else {
              for (let i = 0; i < $scope.poiData.availableOptions.length; i++) {
                let curOption = $scope.poiData.availableOptions[i];
                active_poi.push(i);
                curOption.active = true;
              }
            }
            if (active_poi.length == 1) {
              if (!$scope.drawEnable) $scope.drawEnable = true;
              $scope.poiData.selectedOption = $scope.poiData.availableOptions[active_poi[0]];
              $scope.showVisualization();
            } else {
              if ($scope.drawEnable) $scope.drawEnable = false;
            }
          } else if (option == 2) {
            if ($scope.poiData.selectedOption) {
              for (let i = 0; i < $scope.artistData.availableOptions.length; i++) {
                let curOption = $scope.artistData.availableOptions[i];

                if (curOption.uri_ref.indexOf($scope.poiData.selectedOption.uri) < 0)
                  curOption.active = false;
                else {
                  active_artists.push(i);
                  curOption.active = true;
                }
              }
            } else {
              for (let i = 0; i < $scope.artistData.availableOptions.length; i++) {
                let curOption = $scope.artistData.availableOptions[i];
                active_artists.push(i);
                curOption = true;
              }
            }
            if (active_artists.length == 1) {
              if (!$scope.drawEnable) $scope.drawEnable = true;
              $scope.artistData.selectedOption = $scope.artistData.availableOptions[active_artists[0]];
              $scope.showVisualization();
            } else {
              if ($scope.drawEnable) $scope.drawEnable = false;
            }
          }
        };


        $scope.showVisualization = function() {

          for (var song of $scope.songList) {
            if ((song.path[0] == $scope.artistData.selectedOption.uri) && (song.path[song.path.length - 1] == $scope.poiData.selectedOption.uri)) {
              for (let i = 0; i < $scope.artistData.availableOptions.length; i++) {
                let curOption = $scope.artistData.availableOptions[i];
                curOption.active = true;
              }
              for (let i = 0; i < $scope.poiData.availableOptions.length; i++) {
                let curOption = $scope.poiData.availableOptions[i];
                curOption.active = true;
              }
              shareRecommendation.setPath(song.label, song.path);
              $scope.data_link = shareRecommendation.getPath();
              if ($scope.data_link[0] !== "") {
                $scope.track = $scope.data_link[0];
                $scope.path = $scope.data_link[1];
                break;
              }
            }
          }
        };




      }
    ]);
})(angular);

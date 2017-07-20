(function(angular) {
  'use strict';



  angular.module('myApp.map', [])

    // Controller
    .controller('MapCtrl', ['$scope', '$location', '$log', 'uiGmapGoogleMapApi', 'Geolocation', 'watchOptions', 'Recommendation', 'shareRecommendation', '$mdDialog', '$rootScope', 'NICE',
      function($scope, $location, $log, uiGmapGoogleMapApi, Geolocation, watchOptions, Recommendation, shareRecommendation, $mdDialog, $rootScope, NICE) {

        $scope.spinner_visible = true;
        $rootScope.iframeClass = "iframe_container_2";

        $scope.mapGrabbed = false;
        $scope.enableDirections = false;

        var image_user = {
          url: 'files/user_mark.png'
        };

        $scope.noSharedPosition = false;

        //$scope.markers = pois;
        $scope.onClickMarker = function(marker, eventName, model) {
          $scope.show_hide_info(model);
        };


        $scope.show_hide_info = function(model) {
          var model_id = model.id;
          var model_title = model.label;
          if (model_id != "user_marker") {
            $scope.model_title = model_title;
            $scope.model_index = $scope.markers.indexOf(model);
            $scope.model_latitude = model.latitude;
            $scope.model_longitude = model.longitude;
            Recommendation.getSonglistbyPoi(model.latitude, model.longitude)
              .then(
                function(d) {
                  $scope.model_songList = d;
                  $mdDialog.show({
                    contentElement: '#myDialogMap',
                    parent: angular.element(document.body),
                    clickOutsideToClose: true
                  });
                },
                function(errResponse) {
                  console.error('Error while fetching Currencies');
                }
              );
          }
        };

        $scope.grabMap = function() {
          console.log($scope.map.center.latitude);
          console.log($rootScope.userLocation.latitude);
          console.log($scope.map.center.longitude);
          console.log($rootScope.userLocation.longitude);
          if (($scope.map.center.latitude != $rootScope.userLocation.latitude) ||
              ($scope.map.center.longitude != $rootScope.userLocation.longitude)
              )
            $scope.mapGrabbed = true;
        };

        $scope.centerToNice = function() {
          $scope.map.center = NICE;
          $scope.mapGrabbed = true;
        };

        $scope.resetPosition = function() {
          // reset user position to the one coming from GPS
          $scope.map.center = {
            latitude: $rootScope.userLocation.latitude,
            longitude: $rootScope.userLocation.longitude
          };
          $scope.map.zoom = 14;
          $scope.mapGrabbed = false;
        };

        $scope.showPath = function(song) {
          shareRecommendation.setPath(song.label, song.path);
          $location.path('/visualization');
          $mdDialog.cancel();
        };

        $scope.disableDirections = function() {
          $scope.enableDirections = false;
          directionsDisplay.setMap(null);
          directionsDisplay.setPanel(null); // clear directionpanel from the map
          directionsDisplay = new google.maps.DirectionsRenderer(); // this is to render again, otherwise your route wont show for the second time searching
        };

        $scope.switchPlaylist = function(){
          $rootScope.userLocation.latitude=$scope.model_latitude;
          $rootScope.userLocation.longitude = $scope.model_longitude;
          $rootScope.userLocation.fake = true;
          $rootScope.position_counter ++;
          $mdDialog.cancel();
        };


        var directionsDisplay = new google.maps.DirectionsRenderer();
        var directionsService = new google.maps.DirectionsService();

        $scope.getDirections = function(mode) {
          if (($rootScope.userLocation.gps) && (!$rootScope.userLocation.fake)){
            var dest_lat = $scope.markers[$scope.model_index].latitude;
            var dest_long = $scope.markers[$scope.model_index].longitude;

            var origin_lat = $rootScope.userLocation.latitude;
            var origin_long = $rootScope.userLocation.longitude;

            var request = {
              origin: new google.maps.LatLng(origin_lat, origin_long),
              destination: new google.maps.LatLng(dest_lat, dest_long),
              travelMode: mode
            };

            directionsService.route(request, function(response, status) {
              if (status === google.maps.DirectionsStatus.OK) {
                directionsDisplay.setDirections(response);
                directionsDisplay.setMap($scope.map.control.getGMap());
                directionsDisplay.setPanel(document.getElementById('directionsList'));
                directionsDisplay.setOptions({
                  suppressMarkers: true
                });
                $mdDialog.cancel();
                //$scope.directions.showList = true;
              } else {
                alert('Google route unsuccesfull!');
              }
            });
            $scope.enableDirections = true;
          }
        };
        $scope.already_set = false;

        $scope.$watch('$root.position_counter', function() {
          console.log('getting position map');

          if (!$rootScope.userLocation.latitude) return;

          let latitude = $rootScope.userLocation.latitude,
              longitude = $rootScope.userLocation.longitude;



          var position_marker = {
            id: "user_marker",
            latitude,
            longitude,
            label: 'your position',
            icon: image_user
          };

          if ($scope.markers){
            if (!$scope.mapGrabbed) $scope.markers[$scope.markers.length - 1] = position_marker;
          }

          else {
            $scope.markers = [];
            Recommendation.getPois()
                .then((d) => {
              $scope.markers = $scope.markers.concat(d);
          }, (errResponse) => {
              console.error('Error while fetching PoIs', errResponse);
            });

            $scope.map = {
              control: {},
              zoom: 14,
              options: {
                disableDefaultUI: true
              }
            };
            $scope.markers.push(position_marker);

          }



          if (!$scope.mapGrabbed){
            $scope.map.center = {
              latitude,
              longitude
            };
          }



          console.log($scope.markers);

          if ($scope.enableDirections)
            $scope.getDirections();

          $scope.spinner_visible = false;

        });



      }
    ]);
})(angular);

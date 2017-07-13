(function(angular) {
  'use strict';



  angular.module('myApp.map', [])

    // Controller
    .controller('MapCtrl', ['$scope', '$location', '$log', 'uiGmapGoogleMapApi', 'Geolocation', 'watchOptions', 'Recommendation', 'shareRecommendation', '$mdDialog', '$rootScope','NICE_CENTER',
      function($scope, $location, $log, uiGmapGoogleMapApi, Geolocation, watchOptions, Recommendation, shareRecommendation, $mdDialog, $rootScope,NICE_CENTER) {

        function distance(lat1, lon1, lat2, lon2) {
          var p = 0.017453292519943295;    // Math.PI / 180
          var c = Math.cos;
          var a = 0.5 - c((lat2 - lat1) * p)/2 +
              c(lat1 * p) * c(lat2 * p) *
              (1 - c((lon2 - lon1) * p))/2;

          return 12742 * Math.asin(Math.sqrt(a)); // 2 * R; R = 6371 km
        }


        $scope.spinner_visible = true;
        $rootScope.iframeClass = "iframe_container_2";


        $scope.enableModification = false;
        $scope.enableDirections = false;
        var lat, long;


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
            Recommendation.getSonglistbyPoi(model.latitude, model.longitude)
              .then(
                function(d) {
                  $scope.model_songList = d;
                  console.log($scope.model_songList);
                },
                function(errResponse) {
                  console.error('Error while fetching Currencies');
                }
              );
            $mdDialog.show({
              contentElement: '#myDialogMap',
              parent: angular.element(document.body),
              clickOutsideToClose: true
            });
          }
        };

        $scope.userModification = function() {
          if (!$scope.enableModification) {
            $scope.enableModification = true;
          }
        };

        $scope.centerToNice = function(){
          $scope.map.center = NICE_CENTER;
          $scope.userModification();
        };




        $scope.disableModification = function() {
          // reset user position to the one coming from GPS
          if (lat) {
            $scope.map.center = {
              latitude: lat,
              longitude: long
            };
          } else {
            $scope.map.center = NICE_CENTER;
          }
          $scope.map.zoom = 14;
          $scope.enableModification = false;
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


        var directionsDisplay = new google.maps.DirectionsRenderer();
        var directionsService = new google.maps.DirectionsService();

        $scope.getDirections = function() {
          var dest_lat = $scope.markers[$scope.model_index].latitude;
          var dest_long = $scope.markers[$scope.model_index].longitude;

          var origin_lat = lat;
          var origin_long = long;

          var request = {
            origin: new google.maps.LatLng(origin_lat, origin_long),
            destination: new google.maps.LatLng(dest_lat, dest_long),
            travelMode: google.maps.DirectionsTravelMode.DRIVING
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
        };
        $scope.already_set = false;

        $scope.$watch(Geolocation.getModification, function() {
          var coordinates = Geolocation.getCoordinates();
          var err = coordinates[2];

          if (err) {
            $scope.markers = [];
            // give me all pois
            Recommendation.getPois()
              .then((d) => {
                $scope.markers = $scope.markers.concat(d);
              }, (errResponse) => {
                console.error('Error while fetching pois', errResponse);
              });


            $scope.spinner_visible = false;
            $scope.map = {
              control: {},
              center: {
                latitude: NICE_CENTER.latitude,
                longitude: NICE_CENTER.longitude
              },
              zoom: 14,
              options: {
                disableDefaultUI: true
              }
            };

            $scope.noSharedPosition = true;
            return;
          }

          lat = coordinates[0];
          long = coordinates[1];
          if(!lat) return;

          // marker object
          var position_marker = {
            id: "user_marker",
            latitude: lat,
            longitude: long,
            label: 'your position',
            icon: image_user
          };

          if (!$scope.already_set) {
            $scope.spinner_visible = false;
            $scope.markers = [];
            Recommendation.getPois()
              .then((d) => {
                $scope.markers = $scope.markers.concat(d);
              }, (errResponse) => {
                console.error('Error while fetching Currencies');
              });

            $scope.markers.push(position_marker);
            var center;
            if (distance(NICE_CENTER.latitude,NICE_CENTER.longitude,lat,long) < 6){
              center =  {
                latitude: lat,
                longitude: long
              }
            }
            else {
              center =  {
                latitude: NICE_CENTER.latitude,
                longitude: NICE_CENTER.longitude
              };
              $scope.enableModification = true;

            }
            $scope.map = {
              control: {},
              center:center,
              zoom: 14,
              options: {
                disableDefaultUI: true
              }
            };
            $scope.already_set = true;
          } else {
            $scope.markers.push(position_marker);
            if (!$scope.enableModification) {

              $scope.map.center = {
                latitude: lat,
                longitude: long
              };
              $scope.map.zoom = 14;
            }
            if ($scope.enableDirections) {
              $scope.getDirections();
            }
          }


        });

      }
    ]);
})(angular);

(function(angular) {
  'use strict';

  const MAP_STYLE = [{
      "elementType": "geometry.fill",
      "stylers": [{
        "color": "#009688"
      }]
    },
    {
      "elementType": "labels",
      "stylers": [{
        "visibility": "off"
      }]
    },
    {
      "elementType": "labels.icon",
      "stylers": [{
        "visibility": "simplified"
      }]
    },
    {
      "elementType": "labels.text.fill",
      "stylers": [{
          "color": "#ffffff"
        },
        {
          "visibility": "on"
        }
      ]
    },
    {
      "elementType": "labels.text.stroke",
      "stylers": [{
          "color": "#2aa195"
        },
        {
          "visibility": "on"
        }
      ]
    },
    {
      "featureType": "administrative.land_parcel",
      "elementType": "labels",
      "stylers": [{
        "visibility": "off"
      }]
    },
    {
      "featureType": "landscape.man_made",
      "elementType": "geometry.fill",
      "stylers": [{
          "color": "#59c9bd"
        },
        {
          "lightness": -15
        }
      ]
    },
    {
      "featureType": "landscape.man_made",
      "elementType": "geometry.stroke",
      "stylers": [{
        "visibility": "off"
      }]
    },
    {
      "featureType": "poi",
      "elementType": "labels.text",
      "stylers": [{
        "visibility": "off"
      }]
    },
    {
      "featureType": "poi.business",
      "stylers": [{
        "visibility": "off"
      }]
    },
    {
      "featureType": "poi.park",
      "elementType": "geometry.fill",
      "stylers": [{
          "color": "#63c9a7"
        },
        {
          "lightness": -25
        }
      ]
    },
    {
      "featureType": "road",
      "elementType": "geometry.fill",
      "stylers": [{
          "color": "#2bd0c0"
        },
        {
          "visibility": "on"
        }
      ]
    },
    {
      "featureType": "road",
      "elementType": "geometry.stroke",
      "stylers": [{
        "visibility": "off"
      }]
    },
    {
      "featureType": "road",
      "elementType": "labels.icon",
      "stylers": [{
        "visibility": "off"
      }]
    },
    {
      "featureType": "road.local",
      "elementType": "labels",
      "stylers": [{
        "visibility": "off"
      }]
    },
    {
      "featureType": "road.local",
      "elementType": "labels.text",
      "stylers": [{
        "visibility": "off"
      }]
    },
    {
      "featureType": "transit",
      "stylers": [{
        "visibility": "off"
      }]
    },
    {
      "featureType": "water",
      "elementType": "geometry.fill",
      "stylers": [{
        "color": "#afd1e3"
      }]
    }
  ];

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

        $scope.grabMap = function() {
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


        var directionsDisplay = new google.maps.DirectionsRenderer();
        var directionsService = new google.maps.DirectionsService();

        $scope.getDirections = function() {
          var dest_lat = $scope.markers[$scope.model_index].latitude;
          var dest_long = $scope.markers[$scope.model_index].longitude;

          var origin_lat = $rootScope.userLocation.latitude;
          var origin_long = $rootScope.userLocation.longitude;

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

        $rootScope.$watch('userLocation', (coordinates) => {
          if (!coordinates) {
            $scope.noSharedPosition = true;
            return;
          }
          console.log('coordinates', coordinates);

          let {
            latitude,
            longitude
          } = coordinates;
          if (!latitude) return;

          // marker object
          var position_marker = {
            id: "user_marker",
            latitude,
            longitude,
            label: 'your position',
            icon: image_user
          };

          if (!$scope.markers) {
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
                disableDefaultUI: true,
                styles: MAP_STYLE
              }
            };
          }

          $scope.map.center = {
            latitude,
            longitude
          };

          $scope.markers.push(position_marker);

          if ($scope.enableDirections)
            $scope.getDirections();

          $scope.spinner_visible = false;
        });

      }
    ]);
})(angular);

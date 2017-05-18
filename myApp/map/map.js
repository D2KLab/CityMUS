'use strict';

angular.module('myApp.map', ['ngRoute'])

// Route Config
    .config(['$routeProvider', function($routeProvider) {
        $routeProvider.when('/map', {
            templateUrl: 'map/map.html',
            controller: 'MapCtrl'
        });
    }])

    // Controller
    .controller('MapCtrl', ['$scope', '$location', '$log','uiGmapGoogleMapApi','Geolocation','watchOptions',
        function($scope, $location, $log,uiGmapGoogleMapApi,Geolocation,watchOptions) {
            $scope.enableModification = false;
            $scope.enableDirections = false;

            var image_user = {
                url: 'files/user_mark.png'
            };


            var pois = [ {
                id:1,
                latitude: 43.719740,
                longitude: 7.257380,
                title: '2 tiltle'

            }, {
                id: 2,
                latitude: 43.699740,
                longitude: 7.257398,
                title: '3 title'
            }];



            $scope.noSharedPosition = false;

            var getCenterCoordinates = function(lat,long){
                return {latitude: 43.709742, longitude: 7.257396 }
            }

            $scope.map = {
                control: {},
                center: {
                    latitude: 43.709742,
                    longitude: 7.257396
                },
                zoom: 14,
            };

            $scope.markers = pois;

            var position_data = Geolocation.watchPosition(watchOptions);
            position_data.then(
                null,
                function(err) {
                    $scope.noSharedPosition = true;
                },
                function(position) {
                    $scope.position = position;


                    // marker object
                    var position_marker = {
                        id: "user_marker",
                        latitude: $scope.position.coords.latitude,
                        longitude: $scope.position.coords.longitude,
                        title: 'your position',
                        icon: image_user
                    };


                    $scope.markers.push(position_marker);

                    if (!$scope.enableModification){
                        $scope.map.center = {
                            latitude: $scope.position.coords.latitude,
                            longitude: $scope.position.coords.longitude
                        };
                        $scope.map.zoom = 14;
                    }

                    if ($scope.enableDirections){
                        $scope.getDirections();
                    }

                }
            );
            /*


*/
            $scope.onClickMarker = function(marker, eventName, model) {
                $scope.show_hide_info(model);

            };


            $scope.show_hide_info = function(model) {
                var model_id = model.id;
                var model_title = model.title;
                if (model_id!="user_marker"){
                    if (!$scope.infowindow){
                        $scope.model_title = model_title;
                        $scope.model_index = $scope.markers.indexOf(model);
                        console.log($scope.model_index);
                    }
                    $scope.infowindow = !$scope.infowindow;
                }
            }

            $scope.userModification = function(){
                if (!$scope.enableModification){
                    $scope.enableModification = true;
                }
            };

            $scope.disableModification = function(){
                $scope.map.center = {
                    latitude: $scope.position.coords.latitude,
                    longitude: $scope.position.coords.longitude
                };
                $scope.enableModification = false;
            }

            $scope.disableDirections = function(){
                alert('custom control clicked!');
                directionsDisplay.setMap(null);
                directionsDisplay.setPanel(null); // clear directionpanel from the map
                directionsDisplay = new google.maps.DirectionsRenderer(); // this is to render again, otherwise your route wont show for the second time searching

            }
            /*
            $scope.evaluateMarker = function (title) {
                console.log(title);
                console.log(3);
                return true
            };
            */



            // directions object -- with defaults


            // get directions using google maps api

            var directionsDisplay = new google.maps.DirectionsRenderer();
            var directionsService = new google.maps.DirectionsService();

            $scope.getDirections = function () {

                var dest_lat =$scope.markers[$scope.model_index].latitude;
                var dest_long =$scope.markers[$scope.model_index].longitude;

                var origin_lat = $scope.position.coords.latitude;
                var origin_long = $scope.position.coords.longitude;

                console.log(origin_lat);
                console.log(dest_lat);
                var request = {
                    origin: new google.maps.LatLng(origin_lat, origin_long),
                    destination: new google.maps.LatLng(dest_lat, dest_long),
                    travelMode: google.maps.DirectionsTravelMode.DRIVING
                };
                console.log(request)
                directionsService.route(request, function (response, status) {
                    if (status === google.maps.DirectionsStatus.OK) {
                        directionsDisplay.setDirections(response);
                        console.log($scope.map.control)
                        directionsDisplay.setMap($scope.map.control.getGMap());
                        directionsDisplay.setPanel(document.getElementById('directionsList'));
                        directionsDisplay.setOptions( { suppressMarkers: true } );
                        //$scope.directions.showList = true;
                    } else {
                        alert('Google route unsuccesfull!');
                    }
                });
                $scope.enableDirections = true;
            }





            //TODO


        }]);


'use strict';



// Declare app level module which depends on views, and components
angular.module('myApp', [
    'ngRoute',
    'ngMaterial',
    'uiGmapgoogle-maps',
    'myApp.login',
    'myApp.home',
    'myApp.map',
    'myApp.geolocation',
    'myApp.recommendation',
    'myApp.visualization'
])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.otherwise({redirectTo: '/home'});
    }])

    .config(function($sceDelegateProvider) {
        $sceDelegateProvider.resourceUrlWhitelist([
            // Allow same origin resource loads.
            'self',
            // Allow loading from outer templates domain.
            'https://open.spotify.com/**'
        ]);
    })

    .config(function(uiGmapGoogleMapApiProvider) {
        uiGmapGoogleMapApiProvider.configure({
            key: 'AIzaSyBjU3XKAi9pXb_O6-BiIqkhCOPwEcg3RMM',
            v: '3.20', //defaults to latest 3.X anyhow
            libraries: 'weather,geometry,visualization'
        });
    })

    // Check if logged in
    .run(['$rootScope', '$location', function ($rootScope, $location) {
        $rootScope.$on('$routeChangeError', function (event, next, previous, error) {
            // We can catch the error thrown when the $requireAuth promise is rejected
            // and redirect the user back to the home page
            if (error === 'AUTH_REQUIRED') {
                $location.path('/login');
            }
        });
    }])

    .constant('watchOptions', {
        timeout : 15000,
        enableHighAccuracy: false // may cause errors if true
    })


    .controller("NavCtrl",['$scope','$location','$rootScope','Geolocation','watchOptions','Recommendation','shareRecommendation','$window',
        function($scope,$location,$rootScope,Geolocation,watchOptions,Recommendation,shareRecommendation,$window){
            $scope.home_path = "/home";
            $scope.map_path = "/map";
            $scope.visualization_path = "/visualization";
            $scope.showPlaylist = false;
            $scope.isHome = false;
            $scope.isMap = false;




            var default_playlist = '5tDTLlIwA0EzoYEbEky9Ro';
            $scope.playlist_id = default_playlist;
            var position_data = Geolocation.watchPosition(watchOptions);
            position_data.then(
                null,
                function(err) {
                    $scope.showPlaylist = true;
                    $window.alert("You should share your position to use all functionalities!!!");
                },
                function(position) {
                    console.log(27);
                    var lat  = position.coords.latitude;
                    var lon = position.coords.longitude;
                    Recommendation.getRecommendation(lat,lon)
                        .then(
                            function(d) {
                                $scope.playlist_id = d.id;
                                $scope.songList = d.tracks_paths;
                                $scope.showPlaylist = true;
                            },
                            function(errResponse){
                                console.error('Error while fetching Currencies');
                            }
                        );

                });

            $scope.IsActive = function(str){
                if ($location.path()==str) return true;
                else return false;
            }





            $rootScope.$on('$locationChangeSuccess', function(event){
                if ($location.path()==$scope.login_path) {
                    $scope.showNavbar = false;$scope.isHome = false;$scope.isMap = false;

                }
                else {
                    $scope.showNavbar=true;
                    if  ($location.path()==$scope.home_path){
                        $scope.isHome = true;
                    }
                    else {
                        $scope.isHome = false;
                    }
                }
            });









    }]);
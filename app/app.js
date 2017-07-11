(function(angular) {
  'use strict';

  // Declare app level module which depends on views, and components
  angular.module('myApp', [
      'ui.router',
      'ngMaterial',
      'uiGmapgoogle-maps',
      'myApp.home',
      'myApp.map',
      'myApp.geolocation',
      'myApp.recommendation',
      'myApp.visualization'
    ])
    .config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {

      $urlRouterProvider.otherwise('/home');

      $stateProvider.state('home', {
        url: '/home',
        templateUrl: 'home/home.html',
        controller: 'HomeCtrl'
      }).state('map', {
        url: '/map',
        templateUrl: 'map/map.html',
        controller: 'MapCtrl'
      }).state('visualization', {
        url: '/visualization',
        templateUrl: 'visualization/visualization.html',
        controller: 'VisualizationCtrl'
      });

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

    .constant('watchOptions', {
      timeout: 15000,
      enableHighAccuracy: false // may cause errors if true
    })


    .controller("NavCtrl", ['$scope', '$location', '$rootScope', 'Geolocation', 'watchOptions', 'Recommendation', 'shareRecommendation', '$window',
      function($scope, $location, $rootScope, Geolocation, watchOptions, Recommendation, shareRecommendation, $window) {
          $scope.spinner_visible = true;
        $scope.showPlaylist = false;
        $scope.isHome = false;
        $scope.isMap = false;


        $scope.loading = function(){
            return $location.path() == '/home' && $scope.spinner_visible;
        };

        var default_playlist = '5tDTLlIwA0EzoYEbEky9Ro';
        $scope.playlist_id = default_playlist;
        var position_data = Geolocation.watchPosition(watchOptions);
        position_data.then(null, function(err) {
            $scope.showPlaylist = true;
            $window.alert("You should share your position to use all functionalities!!!");
          },
          function(position) {
            var lat = position.coords.latitude;
            var lon = position.coords.longitude;
            console.log('getting recommendation');
            Recommendation.getRecommendation(lat, lon)
              .then(function(d) {
                  $scope.playlist_id = d.id;
                  $scope.songList = d.tracks_paths;
                  $scope.showPlaylist = true;
                      $scope.spinner_visible = false;
                },
                function(errResponse) {
                  console.error('Error while fetching recommendation');
                    $scope.spinner_visible = false;
                }
              );

          });
      }
    ]);
})(angular);

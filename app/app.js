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

    .constant('NICE', {
      latitude: 43.709742,
      longitude: 7.257396,
      radius: 6
    })

    .controller("NavCtrl", ['$scope', '$location', '$rootScope', 'Geolocation', 'watchOptions', 'Recommendation', 'shareRecommendation', '$window', 'NICE',
      function($scope, $location, $rootScope, Geolocation, watchOptions, Recommendation, shareRecommendation, $window, NICE) {
        $rootScope.userLocation = {};
        $scope.spinner_visible = true;
        $scope.showPlaylist = false;
        $scope.isHome = false;

        $scope.loading = function() {
          return $location.path() == '/home' && $scope.spinner_visible;
        };

        $scope.isHome = function() {
          return $location.path() == '/home';
        };

        function onLocationError(err) {
          console.error("Location error", err);
          console.warn("Position unknown: setting it to Nice center");

          $rootScope.userLocation = {
            // lat: NICE.latitude,
            // lon: NICE.longitude,
            latitude: NICE.latitude,
            longitude: NICE.longitude,
            gps: false,
            err: err
          };
          console.log('getting recommendation');
          Recommendation.getRecommendation($rootScope.userLocation)
            .then(onRecommendationSuccess, onRecommendationError);
        }

        function onLocationUpdate(position) {
          let lat = position.coords.latitude,
            lon = position.coords.longitude;

          let userInNice = distance(NICE.latitude, NICE.longitude, lat, lon) < NICE.radius;

          if (!userInNice)
            console.warn("Position outside Nice: setting it to Nice center");

          let latitude = userInNice ? lat : NICE.latitude,
          longitude = userInNice ? lon : NICE.longitude;

          $rootScope.userLocation = {
            // lat: latitude,
            // lon: longitude,
            latitude,
            longitude,
            gps: userInNice
          };
          console.log('getting recommendation');
          Recommendation.getRecommendation($rootScope.userLocation)
            .then(onRecommendationSuccess, onRecommendationError);
        }

        function onRecommendationSuccess(data) {
          $scope.playlist_id = data.id;
          $scope.songList = data.tracks_paths;
          $scope.showPlaylist = true;
          $scope.spinner_visible = false;
        }

        function onRecommendationError(errResponse) {
          console.error('Error while fetching recommendation', errResponse);
          $scope.spinner_visible = false;
        }

        var default_playlist = '5tDTLlIwA0EzoYEbEky9Ro';
        $scope.playlist_id = default_playlist;
        Geolocation.watchPosition(watchOptions)
          .then(null, onLocationError, onLocationUpdate);
      }
    ]);


  function distance(lat1, lon1, lat2, lon2) {
    var p = 0.017453292519943295; // Math.PI / 180
    var c = Math.cos;
    var a = 0.5 - c((lat2 - lat1) * p) / 2 +
      c(lat1 * p) * c(lat2 * p) *
      (1 - c((lon2 - lon1) * p)) / 2;

    return 12742 * Math.asin(Math.sqrt(a)); // 2 * R; R = 6371 km
  }


})(angular);

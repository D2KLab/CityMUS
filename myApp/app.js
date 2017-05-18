'use strict';



// Declare app level module which depends on views, and components
angular.module('myApp', [
    'ngRoute',
    'uiGmapgoogle-maps',
    'myApp.login',
    'myApp.home',
    'myApp.map',
    'myApp.geolocation'
])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.otherwise({redirectTo: '/home'});
    }])

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
        timeout : 3000,
        enableHighAccuracy: false // may cause errors if true
    })


    .controller("NavCtrl",['$scope','$location','$rootScope','watchOptions',function($scope,$location,$rootScope,watchOptions){
        $scope.home_path = "/home";
        $scope.map_path = "/map";
        $scope.login_path = "/login";

        $scope.IsActive = function(str){
            if ($location.path()==str) return true;
            else return false;
        }


        $rootScope.$on('$locationChangeSuccess', function(event){
            if ($location.path()==$scope.login_path) {
                $scope.showNavbar = false;
            }
            else {
                $scope.showNavbar=true;
            }
        })





    }]);
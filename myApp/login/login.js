'use strict';

angular.module('myApp.login', ['ngRoute'])

// Route Config
    .config(['$routeProvider', function($routeProvider) {
        $routeProvider.when('/login', {
            templateUrl: 'login/login.html',
            controller: 'LoginCtrl'
        });
    }])

    // Controller
    .controller('LoginCtrl', ['$scope', '$location', '$log',
        function($scope,  $location, $log) {
            //TODO

        }]);

'use strict';

angular.module('myApp.home', ['ngRoute'])

// Route Config
    .config(['$routeProvider', function($routeProvider) {
        $routeProvider.when('/home', {
            templateUrl: 'home/home.html',
            controller: 'HomeCtrl'
        });
    }])

    // Controller
    .controller('HomeCtrl', ['$scope', '$location', '$log','Geolocation','watchOptions',
        function($scope,  $location, $log,Geolocation,watchOptions) {

            console.log(watchOptions)
            var position_data = Geolocation.watchPosition(watchOptions);
            position_data.then(
                null,
                function(err) {
                    // error
                },
                function(position) {
                    var lat  = position.coords.latitude;
                    var long = position.coords.longitude;

                });
            //TODO


    }]);


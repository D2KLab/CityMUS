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
    .controller('HomeCtrl', ['$scope', '$location', '$log','Geolocation','watchOptions','Recommendation','shareRecommendation','$window',
        function($scope,  $location, $log,Geolocation,watchOptions,Recommendation,shareRecommendation,$window) {
            //console.log(watchOptions)
            $scope.selectedTrack = false;
            $scope.flag_select = false;
            $scope.$watch(Recommendation.getTracks, function() {
                $scope.songList = Recommendation.getTracks();
                if ($scope.songList.length != 0) $scope.flag_select = true;
            });


            $scope.visualizePath = function(){
                $location.path('/visualization');
            }




            $scope.$watch('selectedSong', function(newValue, oldValue) {

                if (newValue != oldValue){
                    if (newValue == null) {
                        $scope.selectedTrack = false;
                    }
                    else {
                        $scope.selectedTrack = true;
                        for (var key in $scope.songList){
                            //console.log(key);
                            if ($scope.songList[key].label == newValue.label){
                                shareRecommendation.setPath(newValue.label,$scope.songList[key].path);
                                break;
                            }
                        }
                    }

                }

            });







    }]);


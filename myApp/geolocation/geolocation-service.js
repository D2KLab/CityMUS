'use strict';


angular.module('myApp.geolocation.service', [])

    .factory('Geolocation', ['$q','watchOptions',function($q,watchOptions) {

        var lat='';
        var long='';
        var error='';
        var modification = 0;

        return {

            watchPosition: function (options) {
                console.log(444);
                var q = $q.defer();

                var watchID = navigator.geolocation.watchPosition(function (result) {
                    console.log(8888);
                    lat = result.coords.latitude;
                    long = result.coords.longitude;
                    q.notify(result);
                    modification += 1;
                    if (modification > 1000){
                        modification = 1;
                    }
                }, function (err) {
                    console.log(8234);
                    error = err;
                    q.reject(err);
                    modification += 1;
                    if (modification > 1000){
                        modification = 1;
                    }
                }, watchOptions);

                q.promise.watchID = watchID;

                return q.promise;
            },


            getCoordinates:function () {
                return [lat,long,error];
            },
            setCoordinates:function (lat_,long_,err_) {
            },

            getModification:function () {
                return modification;
            },

            clearWatch: function (watchID) {
                return navigator.geolocation.clearWatch(watchID);
            }
        };

    }]);

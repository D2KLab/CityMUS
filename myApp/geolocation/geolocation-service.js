'use strict';


angular.module('myApp.geolocation.service', [])

    .factory('Geolocation', ['$q',function($q) {

        return {
            getCurrentPosition: function (options) {
                var q = $q.defer();

                navigator.geolocation.getCurrentPosition(function (result) {
                    q.resolve(result);
                }, function (err) {
                    q.reject(err);
                }, options);

                return q.promise;
            },

            watchPosition: function (options) {
                var q = $q.defer();

                var watchID = navigator.geolocation.watchPosition(function (result) {
                    q.notify(result);
                    console.log(result)
                }, function (err) {
                    q.reject(err);
                }, options);

                q.promise.cancel = function () {
                    navigator.geolocation.clearWatch(watchID);
                };

                q.promise.clearWatch = function (id) {
                    navigator.geolocation.clearWatch(id || watchID);
                };

                q.promise.watchID = watchID;

                return q.promise;
            },

            clearWatch: function (watchID) {
                return navigator.geolocation.clearWatch(watchID);
            }
        };

    }]);

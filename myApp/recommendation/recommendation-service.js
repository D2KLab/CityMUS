'use strict';


angular.module('myApp.recommendation.service', [])

    .factory('Recommendation', ['$q','Geolocation',function($q,Geolocation) {

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

        function compare(a,b) {
            if (a.distance > b.distance)
                return -1;
            else return 1;
        };


        var computeDistance = function(lat1,lon1,lat2,lon2){
            function toRad(x) {
                return x * Math.PI / 180;
            }

            var R = 6371; // km
            var x1 = lat2-lat1;
            var dLat = x1.toRad();
            var x2 = lon2-lon1;
            var dLon = x2.toRad();
            var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                Math.cos(lat1.toRad()) * Math.cos(lat2.toRad()) *
                Math.sin(dLon/2) * Math.sin(dLon/2);
            var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
            var d = R * c;
            return d
        }

        var getListenPoi = function (myLat,myLong){
            var poi_distances = []
            for (var p in pois) {
                var poi_lat = p.latitude;
                var poi_long = p.longitude;
                var distance = computeDistance(poi_lat,poi_long);
                var obj = {
                    id : p.id,
                    distance: distance
                }
                poi_distances.push(obj);
            }
            poi_distances.sort(compare);
            var tot = poi_distances[0].distance + poi_distances[1].distance + poi_distances[2].distance;
            var rand = Math.random();
            var threshold_1 =  poi_distances[0].distance / tot;
            var threshold_2 = poi_distances[1].distance / tot;
            var threshold_3 = poi_distances[2].distance / tot;
            if (rand <= threshold_1){
                return
            }
            else if ()
                switch case return


        }


        var position_data = Geolocation.watchPosition(watchOptions);
        position_data.then(
            null,
            function(err) {
                $scope.noSharedPosition = true;
            },
            function(position) {

                var latitude = position.latitude;
                var longitude = position.longitude;

            }
        );

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
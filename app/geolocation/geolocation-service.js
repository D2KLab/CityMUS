(function(angular) {

  'use strict';

  angular.module('myApp.geolocation.service', [])
    .factory('Geolocation', ['$q', 'watchOptions', function($q, watchOptions) {

      var lat, long;
      var error;
      var modification = 0;

      return {

        watchPosition: function(options) {
          console.log('watching position');
          var q = $q.defer();

          var watchID = navigator.geolocation.watchPosition(function(result) {
            lat = result.coords.latitude;
            long = result.coords.longitude;
            console.log('position found: ', lat, long);
            q.notify(result);
            modification += 1;
            if (modification > 1000) {
              modification = 1;
            }
          }, function(err) {
            console.error(err);
            error = err;
            q.reject(err);
            modification += 1;
            if (modification > 1000) {
              modification = 1;
            }
          }, watchOptions);

          q.promise.watchID = watchID;

          return q.promise;
        },


        getCoordinates: function() {
          return [lat, long, error];
        },
        setCoordinates: function(lat_, long_, err_) {},

        getModification: function() {
          return modification;
        },

        clearWatch: function(watchID) {
          return navigator.geolocation.clearWatch(watchID);
        }
      };

    }]);
})(angular);

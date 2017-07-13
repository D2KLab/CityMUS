(function(angular) {
  'use strict';

  const server_address = 'http://localhost:5000';
  angular.module('myApp.recommendation.service', [])
    .factory('Recommendation', ['$q', '$http', 'Geolocation', function($q, $http) {
      var tracks = [];

      return {
        getPois: function() {
          return $http.get(server_address + '/pois')
            .then(
              function(response) {
                return response.data;
              },
              function(errResponse) {
                console.error('Error while fetching users');
                return $q.reject(errResponse);
              }
            );
        },

        getRecommendation: function(lat, lon) {
          return $http.get(server_address + '/create_playlist?lat=+' + lat + '&lon=' + lon)
            .then(function(response) {
              tracks = [];
              for (let key of Object.keys(response.data.tracks_paths)) {
                let v = response.data.tracks_paths[key];
                v.key = key;
                tracks.push(v);
              }
              return response.data;
            }, function(errResponse) {
              console.error('Error while fetching users');
              return $q.reject(errResponse);
            });
        },
        getSonglistbyPoi: function(lat, lon) {
          return $http.get(server_address + '/create_playlist?lat=+' + lat + '&lon=' + lon)
            .then(
              function(response) {
                return response.data.tracks_paths;
              },
              function(errResponse) {
                console.error('Error while fetching users');
                return $q.reject(errResponse);
              }
            );
        },
        getTracks: function() {
          return tracks;
        }
      };


      //43.7274
      //7.30667

    }])
    .factory('shareRecommendation', function() {
      var path = [];
      var track = '';
      var null_res_1 = 0;
      var null_res_2 = 0;

      var changeStringStyle = function(x, j) {
        var r = /\\u([\d\w]{4})/gi;
        x = x.replace(r, function(match, grp) {
          return String.fromCharCode(parseInt(grp, 16));
        });
        x = unescape(x);
        var y = x.split(/\/|#/);
        var res = y[y.length - 1].replace(/_/g, " ").replace("Category:", "");

        /*if ((res.length > 14) && (j !== 0) && (j !== 12) && (j !== 6)) {
          res = res.substr(0, 14) + '...';
        }
        */
        return [x, res];
      };

      var setPath = function(trackname, path_dirty) {

        track = trackname;
        null_res_1 = 0;
        null_res_2 = 0;
        path = [];
        var avg_resource = '';

        for (let i in path_dirty) {
          let p = path_dirty[i];
          if (p) {
            var res = changeStringStyle(path_dirty[i], i);
            if (i == 6) avg_resource = res[0];
            path.push({"link":res[0],"label":res[1]});
          } else {
            if (i < 6) null_res_1++;
            else null_res_2++;
          }
        }


        for (let i = 0; i < path.length; i++) {
          var col;
          if (i % 2 == 0) {
            if (i == path.length - 1) {
              col = 'transparent';
              path[i].positions_colors = col;
            } else if (i == 0) {
              col = 'red';
              path[i].positions_colors = col;
            } else if (i == 6 - null_res_1) {
              col = '#f0bf5c';
              path[i].positions_colors = col;
            } else {
              col = 'transparent';
              path[i].positions_colors = col;
            }
          } else path[i].positions_colors = '';
        }
      };

      var getPath = function() {
        return [track, path,6 - null_res_1];
      };

      return {
        setPath,
        getPath,
        changeStringStyle,
        getTrack: () => track
      };
    });
})(angular);

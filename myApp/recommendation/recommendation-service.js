'use strict';


angular.module('myApp.recommendation.service', [])

    .factory('Recommendation', ['$q','$http','Geolocation',function($q,$http) {

        var server_address = 'http://127.0.0.1:5000';


        var tracks = [];

        return {
            getPois: function() {
                return $http.get(server_address+'/pois')
                    .then(
                        function(response){
                            return response.data;
                        },
                        function(errResponse){
                            console.error('Error while fetching users');
                            return $q.reject(errResponse);
                        }
                    );
            },

            getRecommendation: function(lat,lon) {
                return $http.get(server_address+'/create_playlist?lat=+'+lat+'&lon='+lon)
                    .then(
                        function(response){
                            tracks = response.data.tracks_paths;
                            return response.data;
                        },
                        function(errResponse){
                            console.error('Error while fetching users');
                            return $q.reject(errResponse);
                        }
                    );
            },
            getSonglistbyPoi: function(lat,lon) {
                return $http.get(server_address+'/create_playlist?lat=+'+lat+'&lon='+lon)
                    .then(
                        function(response){
                            return response.data.tracks_paths;
                        },
                        function(errResponse){
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
        var start_x = 0.0;
        var start_y = 0.0;
        var end_x = 1.0 - start_x;
        var end_y = start_y;
        var avg_x = 0.5;
        var avg_y = 1.0;
        var delta_w = avg_x - start_x;
        var delta_h = avg_y - start_y;
        var path = [];
        var pathnames = [];
        var positions_colors = [];
        var track = '';
        var null_res_1 = 0;
        var null_res_2 = 0;

        var changeStringStyle = function(x,j) {
            var r = /\\u([\d\w]{4})/gi;
            x = x.replace(r, function (match, grp) {
                return String.fromCharCode(parseInt(grp, 16)); } );
            x = unescape(x);
            var y = x.split("/");
            var res = y[y.length-1].replace("_"," ").replace("Category:","");
            if ((res.length > 14) && (j!=0) && (j!=12) && (j!=6)){
                res = res.substr(0, 14) + '...';
            }
            return [x,res]
        };

        var setPath = function(trackname,path_dirty) {
            track = trackname;
            null_res_1 = 0;
            null_res_2 = 0;
            pathnames = [];
            path = [];
            positions_colors = [];
            var avg_resource = '';
            for (var i=0;i <path_dirty.length;i++){
                var p = path_dirty[i]
                if (p != ''){
                    var res = changeStringStyle(path_dirty[i],i);
                    if (i==6) avg_resource = res[0];
                    path.push(res[0]);
                    pathnames.push(res[1]);
                }
                else {
                    if (i < 6) null_res_1 ++;
                    else null_res_2 ++;
                }
            }
            var nodes_left = 3 - null_res_1/2;
            var nodes_right =3 - null_res_2/2;

            var step_left_x = delta_w / nodes_left;
            var step_left_y = delta_h / nodes_left;

            var step_right_x = delta_w / nodes_right;
            var step_right_y = delta_h / nodes_right;

            var pos_x = start_x;
            var pos_y = start_y;

            for (i = 0; i < path.length; i++){
                var col;

                if (i%2 == 0){
                    if (i == path.length - 1) {
                        col = '#4D84FF';
                        positions_colors.push([end_x,end_y,col]);
                    }
                    else if (i == 0) {
                        col = 'red';
                        positions_colors.push([start_x,start_y,col]);
                        pos_x += step_left_x;
                        pos_y += step_left_y;
                    }
                    else if (i == path.indexOf(avg_resource)){
                        col = '#D5A606';
                        positions_colors.push([avg_x,avg_y,col]);
                        pos_x = avg_x + step_right_x;
                        pos_y = avg_y - step_right_y;

                    }
                    else {
                        col = 'black';
                        positions_colors.push([pos_x,pos_y,col]);
                        if (i < path.indexOf(avg_resource)){
                            pos_x += step_left_x;
                            pos_y += step_left_y;
                        }
                        else {
                            pos_x += step_right_x;
                            pos_y += -step_right_y;
                        }
                    }
                }
                else positions_colors.push('');



            }
        };

        var getPath = function(){
            return [track,path,pathnames,positions_colors];
        };



        return {
            setPath: setPath,
            getPath: getPath,
            changeStringStyle: changeStringStyle,
            getTrack :function(){
                return track;
            }
        };
    });


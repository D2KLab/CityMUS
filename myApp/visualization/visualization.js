'use strict';

angular.module('myApp.visualization', ['ngRoute'])

// Route Config
    .config(['$routeProvider', function($routeProvider) {
        $routeProvider.when('/visualization', {
            templateUrl: 'visualization/visualization.html',
            controller: 'VisualizationCtrl'
        });
    }])

    // Controller
    .controller('VisualizationCtrl', ['$scope', '$location', '$log','Geolocation','watchOptions','Recommendation','shareRecommendation','$mdDialog','$window',
        function($scope,  $location, $log,Geolocation,watchOptions,Recommendation,shareRecommendation,$mdDialog,$window) {
            var data_link = shareRecommendation.getPath();
            var s = "";
            var isGraph = false;
            function drawPath(){
                if (isGraph){
                    s.graph.clear();
                    s.refresh();
                }
                isGraph = true;
                var track = data_link[0];
                var path = data_link[1];
                var pathnames = data_link[2];
                var positions_colors = data_link[3];
                var i,
                    N = 20,
                    E = 200,
                    g = {
                        nodes: [],
                        edges: []
                    };
                g.nodes.push({
                    id: 'n' + pathnames.length,
                    label: track,
                    x: 0.5,
                    y: 0.1,
                    size: 30,
                    color: '#1ECC5C'
                });
                for (i = 0; i < pathnames.length; i+=2){

                    g.nodes.push({
                        id: 'n' + i,
                        label: pathnames[i],
                        link: path[i],
                        x: positions_colors[i][0],
                        y: positions_colors[i][1],
                        size: 30,
                        color: positions_colors[i][2]
                    });
                }

                g.edges.push({
                    id: 'e' + i,
                    source: 'n' + pathnames.length,
                    target: 'n' + 0,
                    size: 0.2,
                    type: 'curve',
                    color: '#1ECC5C',
                });


                for (i = 1; i < pathnames.length; i+=2)
                    g.edges.push({
                        id: 'e' + i,
                        label: pathnames[i],
                        link: path[i],
                        source: 'n' + (i-1),
                        target: 'n' + (i+1),
                        size: 0.2,
                        type: 'line',
                        color: '#ccc'
                    });

                s = new sigma({
                    graph: g,
                    renderer: {
                        container: document.getElementById('graph-container'),
                        type: 'canvas'
                    },
                    settings: {
                        doubleClickEnabled: false,
                        minEdgeSize: 0.5,
                        maxEdgeSize: 4,
                        enableEdgeHovering: true,
                        edgeHoverColor: 'edge',
                        defaultEdgeHoverColor: '#000',
                        edgeHoverSizeRatio: 1,
                        defaultLabelColor: '#00340E',
                        labelThreshold : 0,
                        labelSize: 'proportional',
                        labelAlignment:'top',
                        sideMargin: 5
                    }
                });

// Bind the events:
                s.bind('clickNode doubleClickNode rightClickNode', function(e) {
                    window.open(e.data.node.link, '_blank', 'location=yes,height=570,width=520,scrollbars=yes,status=yes');
                    console.log(e.type, e.data.node.label, e.data.captor);
                });
                s.bind('overEdge clickEdge doubleClickEdge rightClickEdge', function(e) {
                    window.open(e.data.edge.link, '_blank', 'location=yes,height=570,width=520,scrollbars=yes,status=yes');
                    console.log(e.type, e.data.edge, e.data.captor);

                    //overEdge outEdge
                });
                // Configure the noverlap layout:
                var noverlapListener = s.configNoverlap({
                    nodeMargin: 10.0,
                    scaleNodes: 1.05
                });
// Start the layout:
                s.startNoverlap();

            }

            if (data_link[0] != ""){
                drawPath();
            }

            else {
                $mdDialog.show({
                    contentElement: '#myDialog',
                    parent: angular.element(document.body),
                    clickOutsideToClose: true
                });
            }



            $scope.songList = Recommendation.getTracks();

            $scope.$watch(Recommendation.getTracks, function() {
                $scope.songList = Recommendation.getTracks();
                var artistList = {};
                var poiList = {};
                for (var key in $scope.songList){
                    var artist = $scope.songList[key]["path"][0];
                    var artist_name = shareRecommendation.changeStringStyle(artist,0)[1];
                    var poi = $scope.songList[key]["path"][12];
                    var poi_name = shareRecommendation.changeStringStyle(poi,12)[1];
                    if (artist in artistList)artistList[artist]['uri_ref'].push(poi);
                    else {
                        artistList[artist] = {};
                        artistList[artist]['uri']=artist ;
                        artistList[artist]['name']= artist_name;
                        artistList[artist]['uri_ref'] = [poi];
                        artistList[artist]['active'] = true;
                    }
                    if (poi in poiList)poiList[poi]['uri_ref'].push(artist);
                    else {
                        poiList[poi] = {};
                        poiList[poi]['uri']=poi;
                        poiList[poi]['name']= poi_name;
                        poiList[poi]['uri_ref'] = [artist];
                        poiList[poi]['active'] = true;
                    }
                    //$scope.songList[key]
                    $scope.artistList = Object.values(artistList);
                    $scope.poiList = Object.values(poiList);
                }
            });

            $scope.changeActive = function(option){
                if (option == 1){
                    if ($scope.selectedArtist != null){
                        for (var i=0;i < $scope.poiList.length; i++){
                            if ($scope.poiList[i]['uri_ref'].indexOf($scope.selectedArtist['uri']) < 0)
                                $scope.poiList[i]['active'] = false;
                            else {
                                if (!$scope.poiList[i]['active']) $scope.poiList[i]['active'] = true;
                            }
                        }
                    }
                    else {
                        for (var i=0;i < $scope.poiList.length; i++){
                            if (!$scope.poiList[i]['active']) $scope.poiList[i]['active'] = true;
                        }
                    }
                }
                else if  (option == 2){
                    if ($scope.selectedPoi != null){
                        for (var i=0;i < $scope.artistList.length; i++){
                            if ($scope.artistList[i]['uri_ref'].indexOf($scope.selectedPoi['uri']) < 0)
                                $scope.artistList[i]['active'] = false;
                            else {
                                if (!$scope.artistList[i]['active']) $scope.artistList[i]['active'] = true;
                            }
                        }
                    }
                    else {
                        for (var i=0;i < $scope.artistList.length; i++){
                            if (!$scope.artistList[i]['active']) $scope.artistList[i]['active'] = true;
                        }
                    }
                }
            }

            $scope.showTabDialog = function(ev) {
                $mdDialog.show({
                    contentElement: '#myDialog',
                    parent: angular.element(document.body),
                    targetEvent: ev,
                    clickOutsideToClose: true
                });
            };

            $scope.showVisualization = function(){
                for (var key in $scope.songList){
                    if (($scope.songList[key]["path"][0] == $scope.selectedArtist.uri) && ($scope.songList[key]["path"][12] == $scope.selectedPoi.uri)){
                        shareRecommendation.setPath($scope.songList[key].label,$scope.songList[key].path);
                        data_link = shareRecommendation.getPath();
                        if (data_link[0] != ""){
                            drawPath();
                            break;
                        }
                        console.log(335);
                    }
                }
            }




            $scope.cancel = function() {
                $mdDialog.cancel();
            };








        }]);

(function() {
var EbookingApp = angular.module('EbookingApp', ['ui.bootstrap']);

EbookingApp.controller('EbookingCtrl',  ['$scope', '$http', '$modal', '$location', function($scope, $http, $modal, $location) {
	$scope.merchantTypes = [{type: 0, name: "旅行社"}, {type: 1, name: "独立酒店"}];

	$scope.citys = [];
	$scope.distrits = [];
	$scope.hotelMappings =[];
	$scope.merchants = []
	$scope.merchantType = $scope.merchantTypes[0];


    $http.get("/api/city")
        .success(function(resp) {
            if (resp.errcode == 0) {
                $scope.citys = resp.result.citys;
            }
        });
    $http.get("/api/district")
        .success(function(resp) {
            if (resp.errcode == 0) {
                $scope.districts = resp.result.districts;
            }
        });
	$http.get("/api/polymer/ebooking/merchant/all/")
		.success(function(resp) {
			if  (resp.errcode == 0) {
				$scope.merchants = resp.result.merchants;
			}
		})

    $scope.$watch(function() {
        return $location.url();
    },
    function() {
        var params = $location.search();
        var start = params.start != undefined ? params.start : 0;
        var limit = params.limit != undefined ? params.limit : 10;
        var city_id = params.city_id;
        var hotel_name = params.hotel_name;
        loadHotels(start, limit, city_id, hotel_name);

    });

	function loadHotels(start, limit, city_id, hotel_name) {
        var url = "/api/polymer/ebooking?start=" + start + "&limit=" + limit;
        if (city_id != undefined) {
            url += ("&city_id=" + city_id);
        }
        if (hotel_name != undefined) {
            url += ("&hotel_name=" + hotel_name);
        }

        $http.get(url)
            .success(function(data) {
                console.log(data);
                if (data.errcode == 0) {
                    var result = data.result;
                    $scope.hotelMappings = result.hotel_mappings;
                } else {
                    alert(data.errmsg);
                }
            })
            .error(function(data, status){
                if (status != 0) {
                    alert("网络错误");
                }
            });
	}


}])

})()

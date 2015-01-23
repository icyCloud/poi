(function() {
var EbookingApp = angular.module('EbookingApp', ['ui.bootstrap']);

EbookingApp.controller('EbookingCtrl',  ['$scope', '$http', '$modal', '$location', function($scope, $http, $modal, $location) {
	$scope.merchantTypes = [{type: 0, name: "旅行社"}, {type: 1, name: "独立酒店"}];

	$scope.citys = [];
	$scope.distrits = [];
	$scope.hotelMappings =[];
	$scope.merchants = []
	$scope.merchantTypeSelected = null;
	$scope.hotelName = null;

    $scope.totalItems = 0;
    $scope.currentPage = 0;
    $scope.itemsPerPage = 0;
    $scope.maxSize = 10;


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
			console.log(resp);
			if  (resp.errcode == 0) {
				$scope.merchants = resp.result.merchants;
			}
		})

	$scope.search = function() {
		var urlParams = {};
		if ($scope.merchantTypeSelected) {
			console.log($scope.merchantTypeSelected);
			urlParams.merchant_type = $scope.merchantTypeSelected.type;
		}
		if ($scope.merchantSelected) {
			console.log($scope.merchantSelected);
			urlParams.merchant_id = $scope.merchantSelected.id;
		}

		if ($scope.hotelName) {
			urlParams.hotel_name = $scope.hotelName;
		}

		if ($scope.searchCityName) {
			urlParams.city_id = getCityIdByName($scope.searchCityName);
		}

		$location.search(urlParams);

	}

	function flushData() {
        var params = $location.search();
        var start = params.start != undefined ? params.start : 0;
        var limit = params.limit != undefined ? params.limit : 10;
        var city_id = params.city_id;
        var hotel_name = params.hotel_name;
		var merchantId = params.merchant_id;
		var merchantType = params.merchant_type;
        loadHotels(start, limit, merchantType, merchantId, city_id, hotel_name);
	}

	$scope.resetSearch = function() {
		$scope.searchCityName = null;
		$scope.hotelName = null;
		$scope.merchantTypeSelected = null;
		$scope.merchantSelected = null;

		$location.search({});
	}

    $scope.pageChanged = function() {
        var params = $location.search();
        params.start = ($scope.currentPage - 1) * $scope.itemsPerPage;
        params.limit = $scope.itemsPerPage;
        $location.search(params);
    }

    $scope.$watch(function() {
        return $location.url();
    },
    function() {
		flushData();
    });

	function loadHotels(start, limit, merchantType, merchantId, city_id, hotel_name) {
        var url = "/api/polymer/ebooking?start=" + start + "&limit=" + limit;
        if (city_id != undefined) {
            url += ("&city_id=" + city_id);
        }
        if (hotel_name != undefined) {
            url += ("&hotel_name=" + hotel_name);
        }

		if (merchantType != undefined) {
			url += ("&merchant_type=" + merchantType);
		}
		if (merchantId != undefined) {
			url += ("&merchant_id=" + merchantId);
		}

		console.log(url);

        $http.get(url)
            .success(function(data) {
                console.log(data);
                if (data.errcode == 0) {
                    var result = data.result;
                    $scope.hotelMappings = result.hotel_mappings;

                    $scope.totalItems = result.total;
                    $scope.currentPage = Math.floor(result.start / result.limit) + 1;
                    $scope.itemsPerPage = result.limit;
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

    function getCityIdByName(city) {
        for (var i = 0; i < $scope.citys.length; i++) {
            if ($scope.citys[i].name == city) {
                return $scope.citys[i].id;   
            }
        }
        return -1;
    }

	$scope.setHotelOnline = function(hotel) {
		var url = '/api/polymer/hotel/online/';
		var params = {hotel_mapping_id: hotel.id, is_online: hotel.is_online == 0 ? 1 : 0}
		$http.put(url, params)
			.success(function(resp) {
				console.log(resp);
				if (resp.errcode == 0) {
					flushData();
				}
			});
	}

	$scope.setRoomOnline = function(hotel, room) {
		var url = '/api/polymer/roomtype/online/';
		var params = {hotel_mapping_id: hotel.id, roomtype_mapping_id: room.id, is_online: room.is_online == 0 ? 1 : 0}
		$http.put(url, params)
			.success(function(resp) {
				console.log(resp);
				if (resp.errcode == 0) {
					flushData();
				}
			});
	}

	$scope.getHotelOnlineStatus = function(hotel) {
		if (hotel.is_online == 1) {
			return '下线';
		} else {
			return '上线';
		}
	}
	$scope.getRoomOnlineStatus = function(room) {
		if (room.is_online == 1) {
			return '下线';
		} else {
			return '上线';
		}
	}


}])

})()

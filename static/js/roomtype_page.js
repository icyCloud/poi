(function() {

function BedType(id, name) {
	this.id = id;
	this.name = name;
}


var roomtypeapp = angular.module('roomtypeapp', ['ui.bootstrap']);

roomtypeapp.controller('roomtypeController', ['$scope', '$rootScope', '$modal', '$http', function($scope, $rootScope, $modal, $http) {
    $scope.roomtypes = undefined;
    $scope.hotel = undefined;

	$scope.baseBedTypes = [
		new BedType(0, "单床"),
		new BedType(1, "大床"),
		new BedType(2, "双床"),
		new BedType(3, "三床"),
		new BedType(4, "三床-1大2单"),
		new BedType(5, "榻榻米"),
		new BedType(6, "拼床"),
		new BedType(7, "水床"),
		new BedType(8, "榻榻米双床"),
		new BedType(9, "榻榻米单床"),
		new BedType(10, "圆床"),
		new BedType(11, "上下铺"),
		new BedType(12, "大床或双床"),
		new BedType(-1, "未知")
	];

    $scope.getBedNameByType = getBedNameByType;

	$scope.showValidStatus = function(roomtype) {
		if (roomtype.is_valid) {
			return "VALID";
		} else {
			return "INVALID";
		}
	}

    $scope.openRoomTypeModal = function(roomtype) {
		roomtype = roomtype || {};
		var modalInstance = $modal.open({
			templateUrl: 'modal-new-roomtype.html',
			controller: 'roomtypeModalCtrl',
			size: 'lg',
			resolve: {
				roomtype: function() {
					var _room = {};
					copy_roomtype(roomtype, _room);
					return _room;
				},
				baseBedTypes: function() {
					return $scope.baseBedTypes;
				}

			}
		});
		modalInstance.result.then(function(_roomtype) {

			console.log(_roomtype);
			for (var i = 0; i < $scope.roomtypes.length; i++) {
				if ($scope.roomtypes[i].id == _roomtype.id) {
					copy_roomtype(_roomtype, $scope.roomtypes[i]);
					break;
				} else if (i == $scope.roomtypes.length - 1) {
					$scope.roomtypes.push(_roomtype);
				}
			}
		}, function() {
			//modal close
		});
    }

    function fetch_hotel(hotel_id) {
        var url = "/api/hotel/" + hotel_id + "/roomtype/?need_valid=0";
        $http.get(url)
            .success(function(data) {
                console.log(data);
                if (data.errcode == 0) {
                    $scope.roomtypes = data.result.roomtypes;
                    $scope.hotel = data.result.hotel;
                } else {
                    alert(data.errmsg);
                }
            })
            .error(function() {
                alert('network error');
            });
    }
    fetch_hotel(hotel_id);

	function copy_roomtype(from, to) {
		to.name = from.name;
		to.area = from.area;
		to.bed_type = from.bed_type;
		to.broadnet_access = from.broadnet_access;
		to.broadnet_fee = from.broadnet_fee;
		to.capacity = from.capacity;
		to.comments = from.comments;
		to.description = from.description;
		to.facility = from.facility;
		to.floor = from.floor;
		to.hotel_id = from.hotel_id;
		to.id = from.id;
		to.is_valid = from.is_valid;
		to.is_online = from.is_online;
	}

}]);

roomtypeapp.controller('roomtypeModalCtrl', ['$scope', '$http', '$modalInstance', 'roomtype', 'baseBedTypes', function($scope, $http, $modalInstance, roomtype, baseBedTypes) {
	// init
	$scope.roomtype = roomtype;
	$scope.baseBedTypes = baseBedTypes;

	$scope.roomtype._broadnet_access = roomtype.broadnet_access == 1 ? true : false;
	$scope.roomtype._broadnet_fee = roomtype.broadnet_fee == 1 ? true : false;
	$scope.roomtype._bedtype = getBaseBedTypeById(roomtype.bed_type);


	$scope.closeRoomTypeModal = function() {
		$modalInstance.dismiss('cancel');
	}

	$scope.saveRoomTypeModal = function() {
		console.log($scope.roomtype);
		if (!validRoomType($scope.roomtype)) {
			alert("wrong argument");
			return;
		}
		console.log($scope.roomtype);
		$scope.roomtype.bed_type = $scope.roomtype._bedtype.id;
		$scope.roomtype.broadnet_access = $scope.roomtype._broadnet_access ? 1 : 0;
		$scope.roomtype.broadnet_fee = $scope.roomtype._broadnet_fee ? 1 : 0;
		delete $scope.roomtype._bedtype;
		delete $scope.roomtype._broadnet_access;
		delete $scope.roomtype._broadnet_fee;

		if ($scope.roomtype.id == undefined || $scope.roomtype.id == 0) {
			postNewRoomType($scope.roomtype);
		} else {
			putRoomType($scope.roomtype);
		}
	}


	function validRoomType(roomtype) {
		return roomtype.name && (roomtype.area || roomtype.area == 0)
			&& roomtype._bedtype && (roomtype.capacity || roomtype.capacity == 0);
	}

	function postNewRoomType(roomtype) {
		var url = "/api/hotel/" + hotel_id + "/roomtype/";
		$http.post(url, roomtype)
			.success(function(data) {
				if (data.errcode == 0) {
					$modalInstance.close(data.result.roomtype);
				} else {
					alert(data.errmsg);
				}
			})
		.error(function() {
			alert('network error');
		});
	}

	function putRoomType(roomtype) {
		var url = "/api/hotel/" + hotel_id + "/roomtype/";
		$http.put(url, roomtype)
			.success(function(data) {
				if (data.errcode == 0) {
					$modalInstance.close(data.result.roomtype);
				} else {
					alert(data.errmsg);
				}
			})
		.error(function() {
			alert('network error');
		});
	}
	function getBaseBedTypeById(id) {
		for (var i = 0; i < baseBedTypes.length; i++) {
			if (baseBedTypes[i].id == id) {
				return baseBedTypes[i];
			}
		}
	}

}]);

})()

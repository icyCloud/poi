/**
 * Created by lijh on 2015/10/19 0019.
 */
(function () {
    var validapp = angular.module('validapp', ['ui.bootstrap', 'cgBusy']);

    validapp.controller('validController',
        ['$scope', '$http', '$location',
            function ($scope, $http, $location) {

                $scope.ifloading = true;
                $scope.totalItems = 0;
                $scope.currentPage = 0;
                $scope.itemsPerPage = 0;
                $scope.maxSize = 10;

                $scope.hotelMappings = [];
                $scope.hotel_room_mappings = [];
                $scope.providers = [];
                $scope.dialogMainRoomType = {};
                $scope.dialogProviderRoomType = {};
                $scope.changeDialogRoomType = {};
                $scope.providerDialogRoomType = {};
                $scope.changeDialogRoomTypes = [];
                $scope.dialogHotel = {};
                $scope.changeHotel = {};
                $scope.citys = [];
                $scope.searchHotels = [];
                $scope.districts_by_city = [];
                $scope.selectedHotel = undefined;

                $scope.hotelTotalItems = 0;
                $scope.hotelCurrentPage = 1;
                $scope.hotelItemsPerPage = 10;
                $scope.hotelMaxSize = 10;
                $scope.hotelLoadingPromise = null;
                $scope.hotelModalLoadingPromise = null;

                $scope.searchProvider = undefined;
                $scope.searchHotelName = undefined;
                $scope.searchCityName = undefined;
                $scope.statusId = -1;

                var roomtypes = [];
                var currentEditRoomMapping = {};
                var currentEditHotelMapping = {};
                var districts = [];


                $http.get("/api/provider/")
                    .success(function (resp) {
                        if (resp.errcode == 0) {
                            $scope.providers = resp.result.providers;
                        } else {
                            alert(resp.errmsg);
                        }
                    })
                    .error(function () {
                    });

                $http.get("/api/city")
                    .success(function (resp) {
                        if (resp.errcode == 0) {
                            $scope.citys = resp.result.citys;
                        }
                    });
                $http.get("/api/district")
                    .success(function (resp) {
                        if (resp.errcode == 0) {
                            districts = resp.result.districts;
                        }
                    });

                function loadHotelMappings(start, limit, provider_id, city_id, hotel_name, statusId, match_status) {
                    var url = "/api/firstvalid?start=" + start + "&limit=" + limit;
                    if (provider_id != undefined) {
                        url += ("&provider_id=" + provider_id);
                    }
                    if (city_id != undefined) {
                        url += ("&city_id=" + city_id);
                    }
                    if (hotel_name != undefined) {
                        url += ("&hotel_name=" + hotel_name);
                    }
                    if (statusId && statusId != -1) {
                        url += ("&statusId=" + statusId);
                    }
                    if (match_status || match_status == 0){
                        url += ("&match_status=" + match_status)
                    }
                    $scope.ifloading = true;
                    $http.get(url)
                        .success(function (data) {
                            console.log(data);
                            if (data.errcode == 0) {
                                var result = data.result;
                                if(result.hasOwnProperty('hotel_mappings')){
                                    $scope.hotel_room_mappings = [];
                                    $scope.hotelMappings = result.hotel_mappings;
                                }else{
                                    $scope.hotelMappings = [];
                                    $scope.hotel_room_mappings = result.hotel_room_mappings;
                                }
                                roomtypes = result.roomtypes;
                                $scope.totalItems = result.total;
                                $scope.currentPage = Math.floor(result.start / result.limit) + 1;
                                $scope.itemsPerPage = result.limit;
                            } else {
                                alert(data.errmsg);
                            }
                            $scope.ifloading = false;
                        })
                        .error(function (data, status) {
                            $scope.ifloading = false;
                            if (status != 0) {
                                alert("网络错误");
                            }
                        });
                }


                $scope.getModifyBaseRoomTypeUrl = function (roomtypes) {
                    if (roomtypes.length > 0) {
                        return "/hotel/" + roomtypes[0].hotel_id + "/roomtype/";
                    } else {
                        return "javascript: void(0)"
                    }

                };

                $scope.showRoomType = function (mapping) {

                    cloneRoomType(mapping.main_roomtype, $scope.dialogMainRoomType);
                    cloneRoomType(mapping.provider_roomtype, $scope.dialogProviderRoomType);
                    console.log('1111111');

                    $('#modal-roomtype').modal({
                        keyboard: true
                    });
                    $('#modal-roomtype').modal('show');
                };


                $scope.getDistrict = function (district_id) {
                    for (var i = 0; i < districts.length; i++) {
                        if (districts[i].id == district_id) {
                            return districts[i].name;
                        }
                    }
                    return '';
                };
                $scope.getDistrictId = function (name) {
                    for (var i = 0; i < districts.length; i++) {
                        if (districts[i].name == name) {
                            return districts[i].id;
                        }
                    }
                    return -1;
                };
                $scope.getCity = function (city_id) {
                    for (var i = 0; i < $scope.citys.length; i++) {
                        if ($scope.citys[i].id == city_id) {
                            return $scope.citys[i].name;
                        }
                    }
                    return '';
                };

                $scope.getCityId = function (city) {
                    for (var i = 0; i < $scope.citys.length; i++) {
                        if ($scope.citys[i].name == city) {
                            return $scope.citys[i].id;
                        }
                    }
                    return -1;
                };

                $scope.getProvider = function (id) {
                    for (var i = 0; i < $scope.providers.length; i++) {
                        var p = $scope.providers[i];
                        if (id == p.chain_id) {
                            return p;
                        }
                    }
                };

                function getProviderId(provider_name) {
                    for (var i = 0; i < $scope.providers.length; i++) {
                        var provider = $scope.providers[i];
                        if (provider.name == provider_name) {
                            return provider.chain_id;
                        }
                    }

                    return null;
                }

                $scope.setValid = function (mapping) {
                    //if(!confirm('Pass?')) {
                    // return;
                    //}
                    $http.put("/api/firstvalid/hotel/" + mapping.id + "/valid/")
                        .success(function (resp) {
                            if (resp.errcode == 0) {
                                // alert('success');
                                mapping.status = resp.result.status;
                            } else {
                                alert(resp.errmsg);
                            }

                        })
                        .error(function () {
                            alert("network error");
                        });
                };

                $scope.changeRoomType = function (roomMapping) {
                    currentEditRoomMapping = roomMapping;
                    $scope.changeDialogRoomTypes = getRoomTypesByHotelId(roomMapping.main_hotel_id);
                    cloneRoomType(roomMapping.main_roomtype, $scope.changeDialogRoomType);
                    cloneRoomType(roomMapping.provider_roomtype, $scope.providerDialogRoomType);
                    $("#modal-change-roomtype").modal("show");
                };

                $scope.reloadChangeDialogRoomTypes = function () {
                    var url = '/api/hotel/' + currentEditRoomMapping.main_hotel_id + '/roomtype/';
                    $http.get(url)
                        .success(function (resp) {
                            if (resp.errcode == 0) {
                                console.log(resp);
                                mergeRoomTypes(resp.result.roomtypes);
                                $scope.changeDialogRoomTypes = getRoomTypesByHotelId(currentEditRoomMapping.main_hotel_id);
                            } else {
                                alert(resp.errmsg);
                            }

                        })
                        .error(function () {
                            alert('读取失败');
                        });
                };

                $scope.saveChangeRoomType = function () {
                    if ($scope.changeDialogRoomType.name == undefined) {
                        return;
                    }

                    var req = {'id': currentEditRoomMapping.id, 'main_roomtype_id': $scope.changeDialogRoomType.id};

                    $http.put('/api/room_type/mapping/', req)
                        .success(function (resp) {
                            if (resp.errcode == 0) {
                                currentEditRoomMapping.main_roomtype = {};
                                cloneRoomType($scope.changeDialogRoomType, currentEditRoomMapping.main_roomtype);
                                currentEditRoomMapping.main_roomtype_id = currentEditRoomMapping.main_roomtype.id;
                                $("#modal-change-roomtype").modal("hide");
                            } else {
                                alert(resp.errmsg);
                            }
                        })
                        .error(function () {
                            alert('network error');
                        });
                };

                $scope.changeShowRoomType = function (roomType) {
                    $scope.changeDialogRoomType.id = roomType.id;
                    $scope.changeDialogRoomType.name = roomType.name;
                    $scope.changeDialogRoomType.area = roomType.area;
                    $scope.changeDialogRoomType.bed_type = roomType.bed_type;
                    $scope.changeDialogRoomType.comments = roomType.comments;
                    $scope.changeDialogRoomType.description = roomType.description;
                    $scope.changeDialogRoomType.floor = roomType.floor;
                    $scope.changeDialogRoomType.capacity = roomType.capacity;
                };


                function getRoomTypesByHotelId(hotel_id) {
                    var r = [];
                    for (var i = 0; i < roomtypes.length; i++) {
                        var roomtype = roomtypes[i];
                        if (roomtype.hotel_id == hotel_id) {
                            r.push(roomtype);
                        }
                    }

                    return r;
                }

                $scope.validRoomMapping = function (room_mapping) {
                    if (room_mapping.main_roomtype == undefined || room_mapping.main_roomtype.bed_type != room_mapping.provider_roomtype.bed_type) {
                        alert('床型不同');
                        return;
                    }

                    if (room_mapping.provider_id == 10 || room_mapping.provider_id == 17 || room_mapping.provider_id == 19) {
                        if (room_mapping.provider_roomtype_name != room_mapping.main_roomtype.name) {
                            alert('七天房型不同');
                            return;
                        }
                    }


                    //if (!confirm("Pass?")) {
                    // return;
                    //}

                    $http.put('/api/firstvalid/roomtype/' + room_mapping.id + '/valid/')
                        .success(function (resp) {
                            console.log(resp);
                            if (resp.errcode == 0) {
                                room_mapping.status = resp.result.roomtype_mapping.status;
                            } else {
                                alert(resp.errmsg);
                            }
                        })
                        .error(function () {
                            alert('network error');
                        });
                };


                // change hotel
                $scope.showHotelInfo = function (hotelMapping) {
                    var hotel = hotelMapping.main_hotel;
                    currentEditHotelMapping = hotelMapping;

                    $.extend($scope.dialogHotel, hotel);
                    $scope.dialogHotel.status = hotelMapping.status;

                    console.log(hotel);


                    $('#modal-hotel').modal('show');
                };

                $scope.$watch('changeHotel.cityName', function () {
                    city_id = $scope.getCityId($scope.changeHotel.cityName);
                    $scope.districts_by_city = [];

                    for (var i = 0; i < districts.length; i++) {
                        if (districts[i].city_id == city_id) {
                            $scope.districts_by_city.push(districts[i]);
                        }
                    }

                });

                $scope.selectHotel = function (hotel) {
                    $scope.selectedHotel = hotel;
                };

                $scope.hotelPageChanged = function () {
                    $scope.queryHotel();
                };

                $scope.searchHotel = function () {
                    $scope.hotelCurrentPage = 1;
                    $scope.hotelItemsPerPage = 10;
                    $scope.queryHotel();
                };

                $scope.queryHotel = function () {
                    var url = '/api/hotel/search?';
                    var start = ($scope.hotelCurrentPage - 1) * $scope.hotelItemsPerPage
                    var limit = $scope.hotelItemsPerPage;

                    url += ('start=' + start + '&limit=' + limit + '&');

                    var city_id = $scope.getCityId($scope.changeHotel.cityName);
                    var district_id = $scope.getDistrictId($scope.changeHotel.districtName);
                    var name = $scope.changeHotel.name;
                    var star = $scope.changeHotel.star;


                    if (city_id != -1) {
                        url += 'city_id=' + city_id + '&';
                    }
                    if (district_id != -1) {
                        url += 'district_id=' + district_id + '&';
                    }
                    if (name != undefined) {
                        url += 'name=' + name + '&';
                    }
                    if (star != undefined && star != 'any') {
                        url += 'star=' + star;
                    }
                    $scope.hotelLoadingPromise = $http.get(url)
                        .success(function (resp) {
                            if (resp.errcode == 0) {
                                $scope.searchHotels = resp.result.hotels;
                                $scope.hotelTotalItems = resp.result.total;
                                $scope.hotelItemsPerPage = resp.result.limit;
                                $scope.hotelCurrentPage = Math.floor(resp.result.start / resp.result.limit) + 1;
                                $scope.selectedHotel = undefined;
                            } else {
                                alert(resp.errmsg);
                            }
                        })
                        .error(function () {
                            alert('network erroe');
                        })

                };

                $scope.showChangeHotelDialog = function () {
                    $scope.changeHotel = {};
                    $scope.searchHotels = [];
                    $scope.hotelTotalItems = 0;
                    $scope.hotelCurrentPage = 1;
                    $scope.hotelItemsPerPage = 10;
                    $('#modal-hotel').modal('hide');
                    $("#modal-change-hotel").modal('show');
                };


                $scope.saveChangeHotel = function () {
                    var hotel = $scope.selectedHotel;
                    console.log(hotel);
                    if (hotel == undefined) {
                        return;
                    }
                    req = {'hotel_mapping_id': currentEditHotelMapping.id, 'main_hotel_id': hotel.id}
                    $scope.hotelModalLoadingPromise = $http.put("/api/hotel/mapping", req)
                        .success(function (resp) {
                            console.log(resp);
                            if (resp.errcode == 0) {
                                $("#modal-change-hotel").modal('hide');
                                currentEditHotelMapping.main_hotel_id = hotel.id;
                                currentEditHotelMapping.main_hotel = hotel;
                                mergeRoomTypes(resp.result.room_types);
                                for (var i = 0; i < currentEditHotelMapping.roomtype_mappings.length; i++) {
                                    var room_type_mapping = currentEditHotelMapping.roomtype_mappings[i];
                                    room_type_mapping.main_hotel_id = hotel.id;
                                    room_type_mapping.main_roomtype_id = 0;
                                    room_type_mapping.status = 0;
                                    room_type_mapping.main_roomtype = undefined;
                                }
                            } else {
                                alert(resp.errmsg);
                            }

                        })
                        .error(function () {
                            alert('network error');
                        });
                };

                function mergeRoomTypes(new_types) {
                    var len = roomtypes.length;
                    for (var i = 0; i < new_types.length; i++) {
                        for (var j = 0; j < len; j++) {
                            if (roomtypes[j].id == new_types[i].id) {
                                angular.copy(new_types[i], roomtypes[j]);
                                break;
                            }
                            if (j == len - 1) {
                                roomtypes.push(new_types[i]);
                            }
                        }
                    }
                }

                $scope.pageChanged = function () {
                    var params = $location.search();
                    var skipPage = $("#page_text").val();
                    if (skipPage) {
                        params.start = (skipPage - 1) * $scope.itemsPerPage;
                    } else {
                        params.start = ($scope.currentPage - 1) * $scope.itemsPerPage;
                    }
                    <!--params.start = ($scope.currentPage - 1) * $scope.itemsPerPage;-->
                    params.limit = $scope.itemsPerPage;
                    $location.search(params);
                };


                $scope.$watch(function () {
                        return $location.url();
                    },
                    function () {
                        var params = $location.search();
                        var start = params.start != undefined ? params.start : 0;
                        var limit = params.limit != undefined ? params.limit : 10;
                        var provider_id = params.provider_id;
                        var city_id = params.city_id;
                        var hotel_name = params.hotel_name;
                        var statusId = params.statusId;
                        var match_status = params.match_status;
                        loadHotelMappings(start, limit, provider_id, city_id, hotel_name, statusId, match_status);

                    });

                $scope.search = function (serchMatch) {
                    console.log($scope.searchProvider);
                    console.log($scope.searchHotelName);
                    console.log($scope.searchCityName);

                    var provider_id;
                    if ($scope.searchProvider != 'any' || $scope.searchProvider != undefined) {
                        provider_id = getProviderId($scope.searchProvider);
                    } else {
                        provider_id = null;
                    }

                    var city_id = $scope.getCityId($scope.searchCityName);

                    var urlParams = {};

                    if (provider_id != null) {
                        urlParams.provider_id = provider_id;
                    }
                    if (city_id != -1) {
                        urlParams.city_id = city_id;
                    }
                    if ($scope.searchHotelName != undefined) {
                        urlParams.hotel_name = $scope.searchHotelName;
                    }
                    if ($scope.status != undefined && $scope.status != -1) {
                        urlParams.statusId = $scope.status;
                    }
                    if(serchMatch){
                        urlParams.match_status = '0';
                    }
                    console.log(urlParams);
                    $location.search(urlParams);
                };

                $scope.resetSearch = function () {
                    $scope.searchProvider = 'any';
                    $scope.searchHotelName = undefined;
                    $scope.searchCityName = undefined;

                    $location.search({});
                };

                function cloneRoomType(from, to) {
                    if (from == undefined) {
                        to.area = undefined;
                        to.bed_type = undefined;
                        to.capacity = undefined;
                        to.comments = undefined;
                        to.description = undefined;
                        to.floor = undefined;
                        to.id = undefined;
                        to.is_online = undefined;
                        to.is_valid = undefined;
                        to.name = undefined;
                    }
                    $.extend(to, from);
                }

                $scope.getBedNameByType = getBedNameByType;
                $scope.getProviderBedNameByType = getProviderBedNameByType;

                $scope.showMainHotelName = function (hotel_mapping) {
                    if (hotel_mapping.main_hotel == undefined) {
                        return 'None';
                    } else {
                        return hotel_mapping.main_hotel.name;
                    }
                };

                $scope.showRoomTypeName = function (roomtype) {
                    if (roomtype.is_valid) {
                        return roomtype.name + "    " + roomtype.id;
                    } else {
                        return "INVALID " + roomtype.name + "    " + roomtype.id;
                    }
                }
            }]);
}());
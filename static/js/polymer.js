/**
 * Created by lijh on 2015/10/14 0014.
 */
(function () {

    var validapp = angular.module('validapp', ['ui.bootstrap', 'toggle-switch']);


    validapp.controller('validController',
        ['$scope', '$http', '$location',
            function ($scope, $http, $location) {

                $scope.ifloading = true;
                $scope.multi_line_msg = false;
                $scope.totalItems = 0;
                $scope.currentPage = 0;
                $scope.itemsPerPage = 0;
                $scope.maxSize = 10;

                $scope.hotelMappings = [];
                $scope.providers = [];
                $scope.dialogMainRoomType = {};
                $scope.dialogProviderRoomType = {};
                $scope.dialogHotel = {};
                $scope.changeHotel = {};
                $scope.provinces = [];
                $scope.citys = [];
                $scope.districts = [];

                $scope.searchProvider = undefined;
                $scope.searchHotelName = undefined;
                $scope.searchCityName = undefined;
                $scope.searchProvinceName = '';

                $scope.showOnlineType = 0;

                var roomtypes = [];

                $('#liveStarTime').datepicker({

                    format: "yyyy-mm-dd",
                    language: "zh-CN",
                    orientation: "top auto",
                    autoclose: true,
                    enableOnReadonly: true,
                    showOnFocus: true


                });
                $('#liveEndTime').datepicker({

                    format: "yyyy-mm-dd",
                    language: "zh-CN",
                    orientation: "top auto",
                    autoclose: true,
                    enableOnReadonly: true,
                    showOnFocus: true


                });

                $http.get("/api/provider/")
                    .success(function (resp) {
                        if (resp.errcode == 0) {
                            $scope.providers = resp.result.providers;
                        } else {
                        }
                    })
                    .error(function () {
                    });
                $http.get("/api/province")
                    .success(function (resp) {
                        if (resp.errcode == 0) {
                            $scope.provinces = resp.result.provinces;
                        }
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
                            $scope.districts = resp.result.districts;
                        }
                    });

                function loadHotelMappings(start, limit, provider_id, city_id, hotel_name, show_online_type) {
                    var url = "/api/polymer?start=" + start + "&limit=" + limit;
                    if (provider_id != undefined) {
                        url += ("&provider_id=" + provider_id);
                    }
                    if (city_id != undefined) {
                        url += ("&city_id=" + city_id);
                    }
                    if (hotel_name != undefined) {
                        url += ("&hotel_name=" + hotel_name);
                    }
                    if (show_online_type != undefined) {
                        url += ("&show_online_type=" + show_online_type);
                    }
                     $scope.ifloading = true;
                    $http.get(url)
                        .success(function (data) {
                            console.log(data);
                            if (data.errcode == 0) {
                                var result = data.result;
                                $scope.hotelMappings = result.hotel_mappings;
                                checkHotelMappingOnline($scope.hotelMappings);
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

                function checkHotelMappingOnline(hotelMappings) {
                    for (var i = 0; i < hotelMappings.length; i++) {
                        var hotelMapping = hotelMappings[i];
                        hotelMapping.toggle = hotelMapping.is_online == 1;

                        for (var j = 0; j < hotelMapping.roomtype_mappings.length; j++) {
                            var roomtype_mapping = hotelMapping.roomtype_mappings[j];
                            roomtype_mapping.toggle = roomtype_mapping.is_online == 1;
                        }
                    }
                }

                function toggleHotelMappingOnline(hotelMapping) {
                    hotelMapping.toggle = hotelMapping.is_online == 1;

                    for (var j = 0; j < hotelMapping.roomtype_mappings.length; j++) {
                        var roomtype_mapping = hotelMapping.roomtype_mappings[j];
                        if (hotelMapping.is_online == 0) {
                            roomtype_mapping.is_online = 0;
                        }
                        roomtype_mapping.toggle = roomtype_mapping.is_online == 1;
                    }
                }

                $scope.showRoomType = function (mapping) {
                    $.extend($scope.dialogMainRoomType, mapping.main_roomtype);
                    $.extend($scope.dialogProviderRoomType, mapping.provider_roomtype);
                    $('#modal-roomtype').modal('show');
                };


                $scope.getDistrict = function (district_id) {
                    for (var i = 0; i < $scope.districts.length; i++) {
                        if ($scope.districts[i].id == district_id) {
                            return $scope.districts[i].name;
                        }
                    }
                    return '';
                };
                $scope.getDistrictId = function (name) {
                    for (var i = 0; i < $scope.districts.length; i++) {
                        if ($scope.districts[i].name == name) {
                            return $scope.districts[i].id;
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
                $scope.getProvince = function (province_id) {
                    for (var i = 0; i < $scope.provinces.length; i++) {
                        if ($scope.provinces[i].id == province_id) {
                            return $scope.provinces[i].name;
                        }
                    }
                    return '';
                };
                $scope.getProvinceId = function (province) {
                    for (var i = 0; i < $scope.provinces.length; i++) {
                        if ($scope.provinces[i].name == province) {
                            return $scope.provinces[i].id;
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

                $scope.rejectRoomMapping = function (room_mapping) {
                    if (!confirm("Reject ?")) {
                        return;
                    }

                    $http.delete('/api/polymer/roomtype/' + room_mapping.id + '/reject/')
                        .success(function (resp) {
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


                $scope.showHotelInfo = function (hotelMapping) {
                    var hotel = hotelMapping.main_hotel;
                    currentEditHotelMapping = hotelMapping;

                    $scope.dialogHotel.name = hotel.name;
                    $scope.dialogHotel.address = hotel.address;
                    $scope.dialogHotel.city_id = hotel.city_id;
                    $scope.dialogHotel.district_id = hotel.district_id;
                    $scope.dialogHotel.star = hotel.star;
                    $scope.dialogHotel.status = hotelMapping.status;

                    console.log(hotel);


                    $('#modal-hotel').modal('show');
                };

                $scope.pageChanged = function () {
                    var params = $location.search();
                    var skipPage = $("#page_text").val()
                    if (skipPage) {
                        params.start = (skipPage - 1) * $scope.itemsPerPage;
                    } else {
                        params.start = ($scope.currentPage - 1) * $scope.itemsPerPage;
                    }

                    params.limit = $scope.itemsPerPage;
                    $location.search(params);
                };


                $scope.$watch(function () {
                        return $location.url();
                    },doSearch);

                function doSearch(){
                    var params = $location.search();
                        var start = params.start != undefined ? params.start : 0;
                        var limit = params.limit != undefined ? params.limit : 10;
                        var provider_id = params.provider_id;
                        var city_id = params.city_id;
                        var hotel_name = params.hotel_name;
                        var is_show_online = params.is_show_online;
                        var is_show_offline = params.is_show_offline;
                        var show_online_type = params.show_online_type;
                        loadHotelMappings(start, limit, provider_id, city_id, hotel_name, show_online_type);
                }

                $scope.search = function () {
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
                    if ($scope.showOnlineType != undefined) {
                        urlParams.show_online_type = $scope.showOnlineType;
                    }

                    console.log(urlParams);
                    $location.search(urlParams);
                    doSearch();
                };

                $scope.resetSearch = function () {
                    $scope.searchProvider = 'any';
                    $scope.searchHotelName = undefined;
                    $scope.searchCityName = undefined;
                    $scope.showOnlineType = 0;

                    $location.search({});
                };

                $scope.rejectHotel = function (hotelMapping) {
                    if (!confirm("Reject ?")) {
                        return;
                    }

                    $http.delete('/api/polymer/hotel/' + hotelMapping.id + '/reject/')
                        .success(function (resp) {
                            if (resp.errcode == 0) {
                                hotelMapping.status = resp.result.hotel_mapping.status;
                            } else {
                                alert(resp.errmsg);
                            }
                        })
                        .error(function () {
                            alert("network error");
                        });
                };

                $scope.hotelOnline = function (hotelMapping) {
                    //if (!confirm("Change ?")) {
                    //hotelMapping.toggle = hotelMapping.is_online == 1;
                    //return;
                    // }

                    var isOnline = hotelMapping.is_online == 1 ? 0 : 1;
                    var params = {'hotel_mapping_id': hotelMapping.id, 'is_online': isOnline};

                    $http.put('/api/polymer/hotel/online/', params)
                        .success(function (resp) {
                            if (resp.errcode == 0) {
                                hotelMapping.is_online = resp.result.hotel_mapping.is_online;
                                alert("success");
                            } else {
                                alert(resp.errmsg);
                            }
                            toggleHotelMappingOnline(hotelMapping);
                        })
                        .error(function () {
                            checkHotelMappingOnline([hotelMapping]);
                            alert("network error");
                        });
                };

                $scope.show = function () {
                    $('#modal-onlineall').modal({
                        keyboard: true
                    });
                    $('.m :checkbox').prop('checked', false);
                    $('#liveStarTime').val('');
                    $('#liveEndTime').val('');
                    $('#providers .m').empty();
                    $('#providers .m').append($('<label for="provider_-100"></label>').append('<input id="provider_-100" type="checkbox" value="-100" />').append('<span>全部</span>'));
                    for (var i = 0; i < $scope.providers.length; i++) {
                        var provider = $scope.providers[i];
                        var provider_id = provider['chain_id'];
                        var input = $('<input type="checkbox" />');
                        input.attr('id', provider_id);
                        input.val(provider['chain_id']);
                        var span = $('<span></span>');
                        span.html(provider['name']);
                        $("#providers .m").append($('<label></label>').attr('for', provider_id).append(input).append(span));
                    }
                    $('#providers .m :input').each(function(){
                        $(this).change(function(){
                            $scope.changeCheckbox($(this));
                        });
                    });
                    $('#modal-onlineall').modal('show');
                };

                $scope.$watch('searchProvinceName.selected', function(newValue, oldValue){
                    if(newValue == oldValue){
                        return;
                    }
                    $('#citys .supply-section').css('height', '240px');
                    var prov_id = $scope.getProvinceId(newValue);
                    $('#citys .m').empty();
                    if(prov_id && prov_id != -1){
                        $('#citys .m').append($('<label for="city_-100" style="width: 16%"></label>').append('<input id="city_-100" type="checkbox" value="-100" />').append('<span>全部</span>'));
                        for (var i = 0; i < $scope.citys.length; i++) {
                            var city = $scope.citys[i];
                            if(city['prov_id'] == prov_id){
                                var city_id = 'city_' + city['id'];
                                var input = $('<input type="checkbox" />');
                                input.attr('id', city_id);
                                input.val(city['id']);
                                var span = $('<span></span>');
                                span.html(city['name']);
                                $("#citys .m").append($('<label style="width: 16%"></label>').attr('for', city_id).append(input).append(span));
                            }
                        }
                        $('#citys .m :input').each(function(){
                            $(this).change(function(){
                                $scope.changeCheckbox($(this));
                            });
                        });
                    }
                });

                $scope.changeCheckbox = function changeCheckbox(obj){
                    var parent = obj.parents('.m');
                    var val = obj.val();
                    var checked = obj.is(':checked');
                    var check_length = parent.find(':checkbox:gt(0):checked').size();
                    var all_length = parent.find(':checkbox:gt(0)').size();
                    if (val == -100){
                        if(checked){
                            parent.find(':checkbox:gt(0)').prop('checked', true);
                        } else {
                            parent.find(':checkbox:gt(0)').prop('checked', false);
                        }
                    }else{
                        if (check_length == all_length){
                            parent.find(':checkbox:eq(0)').prop('checked', true);
                        } else {
                            parent.find(':checkbox:eq(0)').prop('checked', false);
                        }
                    }
                };

                $scope.getLineParams = function(){
                    $scope.multi_line_msg = '';
                    var params = {};

                    var chainCheckeds = [];
                    var chks = $("#providers input:checked");
                    if (!chks || chks.length < 1) {
                        $scope.multi_line_msg = '请选择供应商！';
                        return params;
                    }
                    for (var i = 0; i < chks.length; i++) {
                        chainCheckeds.push($(chks[i]).val());
                    }
                    var startTime = $('#liveStarTime').val();
                    var endTime = $('#liveEndTime').val();
                    if (!startTime || !endTime) {
                        $scope.multi_line_msg = '请输入开始和结束日期！';
                        return params;
                    }

                    var provinceId = $scope.getProvinceId($scope.searchProvinceName.selected);
                    if(provinceId && provinceId != -1){
                        var cityCheckeds = [];
                        chks = $('#citys input:checked');
                        if(!chks || chks.length < 1 || (chks.length == 1 && $(chks.get(0)).val() == -100)) {
                            chks = $('#citys input:gt(0)');
                        }
                        var same = getSameCity();
                        if(same){
                            for(var i = 0; i < chks.length; i++){
                                cityCheckeds.push($(chks.get(i)).val());
                            }
                            params = {'chainIds': chainCheckeds.join(','), 'cityIds': cityCheckeds.join(','), 'startTime': startTime, 'endTime': endTime};
                            console.log(params);
                        }
                    }else{
                        if(confirm('确认不选择省份城市批量操作酒店？')){
                            params = {'chainIds': chainCheckeds.join(','), 'startTime': startTime, 'endTime': endTime};
                        }
                    }
                    return params;
                };

                function getSameCity(){
                    var check_city = $('#citys input:checked');
                    if(!check_city || check_city.length < 1 || (check_city.length == 1 && $(check_city.get(0)).val() == -100)) {
                        return true;
                    }
                    var all_city = $('#citys input');
                    var uncheck_city = $('#citys :input:not(:checked)');
                    var sames = [];
                    for(var i = 0; i < check_city.size(); i++){
                        var checked = $(check_city.get(i));
                        var cityName = checked.next('span').html().replace(/[市县乡]/g, '');
                        for(var j = 0; j < uncheck_city.size(); j++){
                            var unchecked = $(uncheck_city.get(j));
                            var uncityName = unchecked.next('span').html();
                            if(uncityName.indexOf(cityName) > -1){
                                sames.push(uncityName);
                            }
                        }
                    }
                    if(sames.length > 0){
                        if(confirm('未选城市中类似还有：' + sames.join(',') + '\n是否跳过这些城市继续批量操作？')){
                            return true;
                        }
                    }else{
                        return true;
                    }
                    return false;
                }

                $scope.multiOffline = function () {
                    var params = $scope.getLineParams();
                    if($.isEmptyObject(params)){
                        return;
                    }
                    params.line = 0;
                    $scope.multiLine(params);
                };

                $scope.multiOnline = function () {
                    var params = $scope.getLineParams();
                    if($.isEmptyObject(params)){
                        return;
                    }
                    params.line = 1;
                    $scope.multiLine(params);
                };

                $scope.multiLine = function(params){
                    $http.put('/api/polymer/hotel/line', params)
                        .success(function (resp) {
                            if (resp.errcode == 0) {
                                alert("success");
                            } else {
                                if(params.line == 1){
                                    alert('上线失败');
                                }else{
                                    alert('下线失败');
                                }
                            }
                        })
                        .error(function () {
                            alert("network error");
                        });
                };

                $scope.roomOnline = function (hotelMapping, roomMapping) {
                    if (hotelMapping.is_online == 0) {
                        return;
                    }

                    if (roomMapping.is_online == 0) {
                        if (roomMapping.main_roomtype == undefined || roomMapping.main_roomtype.bed_type != roomMapping.provider_roomtype.bed_type) {
                            alert('床型不同');
                            return;
                        }
                        if (roomMapping.provider_id == 10 || roomMapping.provider_id == 17 || roomMapping.provider_id == 19) {
                            if (roomMapping.provider_roomtype_name != roomMapping.main_roomtype.name) {
                                alert('七天房型不同');
                                return;
                            }
                        }
                    }

                    // if (!confirm("Change ?")) {
                    // roomMapping.toggle = roomMapping.is_online == 1;
                    // return;
                    // }

                    var isOnline = roomMapping.is_online == 1 ? 0 : 1;
                    var params = {
                        'roomtype_mapping_id': roomMapping.id,
                        'is_online': isOnline,
                        'hotel_mapping_id': hotelMapping.id
                    };

                    $http.put('/api/polymer/roomtype/online/', params)
                        .success(function (resp) {
                            if (resp.errcode == 0) {
                                roomMapping.is_online = resp.result.roomtype_mapping.is_online;
                                roomMapping.toggle = roomMapping.is_online == 1;
                                alert("success");
                            } else {
                                alert(resp.errmsg);
                            }
                            toggleHotelMappingOnline(hotelMapping);
                        })
                        .error(function () {
                            alert("network error");
                            toggleHotelMappingOnline(hotelMapping);
                        });
                };

                $scope.getBedNameByType = getBedNameByType;
                $scope.getProviderBedNameByType = getProviderBedNameByType;
            }]);

})();
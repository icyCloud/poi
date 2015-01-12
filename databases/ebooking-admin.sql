/*
 Navicat Premium Data Transfer

 Source Server         : 192.168.10.15
 Source Server Type    : MySQL
 Source Server Version : 50538
 Source Host           : 192.168.10.15
 Source Database       : ebooking-admin

 Target Server Type    : MySQL
 Target Server Version : 50538
 File Encoding         : utf-8

 Date: 11/06/2014 16:52:30 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `brand`
-- ----------------------------
DROP TABLE IF EXISTS `brand`;
CREATE TABLE `brand` (
  `id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '品牌id',
  `groupId` int(10) unsigned DEFAULT '0' COMMENT '集团id',
  `shortName` varchar(15) DEFAULT '' COMMENT '缩写名',
  `name` varchar(50) CHARACTER SET ucs2 DEFAULT '' COMMENT '全名',
  `letters` varchar(50) CHARACTER SET ucs2 DEFAULT '' COMMENT '英文标识',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='品牌';

-- ----------------------------
--  Table structure for `businessZone`
-- ----------------------------
DROP TABLE IF EXISTS `businessZone`;
CREATE TABLE `businessZone` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `elongId` varchar(50) CHARACTER SET ucs2 DEFAULT '0' COMMENT '艺龙id',
  `cityId` int(11) DEFAULT '0' COMMENT '城市id',
  `name` varchar(50) DEFAULT NULL COMMENT '名字',
  `type` tinyint(3) unsigned DEFAULT '0' COMMENT '0商业性的，1地理性的',
  PRIMARY KEY (`id`),
  KEY `Index 2` (`elongId`),
  KEY `Index 3` (`cityId`)
) ENGINE=InnoDB AUTO_INCREMENT=11840 DEFAULT CHARSET=utf8 COMMENT='商圈';

-- ----------------------------
--  Table structure for `city`
-- ----------------------------
DROP TABLE IF EXISTS `city`;
CREATE TABLE `city` (
  `id` int(11) NOT NULL,
  `name` varchar(45) NOT NULL,
  `qunarId` varchar(50) NOT NULL DEFAULT '',
  `elongId` varchar(50) NOT NULL DEFAULT '0',
  `ctripId` int(11) NOT NULL DEFAULT '0',
  `provId` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `QunarId` (`qunarId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='城市信息表';

-- ----------------------------
--  Table structure for `district`
-- ----------------------------
DROP TABLE IF EXISTS `district`;
CREATE TABLE `district` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cityId` int(11) NOT NULL DEFAULT '0',
  `name` varchar(50) NOT NULL DEFAULT '',
  `qunarId` varchar(50) NOT NULL DEFAULT '',
  `elongId` varchar(50) NOT NULL DEFAULT '',
  `ctripId` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_city` (`cityId`)
) ENGINE=InnoDB AUTO_INCREMENT=15663 DEFAULT CHARSET=utf8 COMMENT='城市下区域';

-- ----------------------------
--  Table structure for `facility`
-- ----------------------------
DROP TABLE IF EXISTS `facility`;
CREATE TABLE `facility` (
  `id` int(10) unsigned NOT NULL COMMENT '设施id',
  `name` varchar(50) DEFAULT NULL COMMENT '设施名字',
  `type` tinyint(3) unsigned DEFAULT NULL COMMENT '设施类型，0酒店，1房间',
  `hotelFacilityType` tinyint(3) unsigned DEFAULT '0' COMMENT '酒店设施类型，1服务设施，2娱乐设施，3基础设施，0通用设施',
  KEY `Index 1` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='设施';

-- ----------------------------
--  Table structure for `hotel`
-- ----------------------------
DROP TABLE IF EXISTS `hotel`;
CREATE TABLE `hotel` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `elongId` varchar(50) NOT NULL DEFAULT '' COMMENT '艺龙id',
  `name` varchar(50) NOT NULL DEFAULT '' COMMENT '名字',
  `address` varchar(100) DEFAULT '' COMMENT '地址',
  `zipCode` varchar(10) DEFAULT '0' COMMENT '邮编',
  `star` tinyint(3) unsigned DEFAULT '0' COMMENT '星级0-255',
  `phone` varchar(100) DEFAULT '' COMMENT '联系电话',
  `fax` varchar(100) DEFAULT '' COMMENT '传真',
  `establishmentDate` varchar(15) DEFAULT '' COMMENT '成立日期 yyyy-MM',
  `renovationDate` varchar(15) DEFAULT '' COMMENT '翻修日期 yyyy-MM',
  `isEconomic` bit(1) NOT NULL DEFAULT b'0' COMMENT '是否是经济酒店：0不是，1是',
  `isApartment` bit(1) NOT NULL DEFAULT b'0' COMMENT '是否是公寓式酒店：0不是，1是',
  `gLog` double NOT NULL DEFAULT '0' COMMENT '谷歌经度',
  `gLat` double NOT NULL DEFAULT '0' COMMENT '谷歌纬度',
  `bLog` double NOT NULL DEFAULT '0' COMMENT '百度经度',
  `bLat` double NOT NULL DEFAULT '0' COMMENT '百度纬度',
  `cityId` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '百达屋城市id',
  `businessZone` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '商圈id',
  `districtId` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '百达屋区域id',
  `creditCards` varchar(200) DEFAULT '' COMMENT '支持的信用卡',
  `intro` text COMMENT '介绍',
  `description` text COMMENT '描述',
  `generalAmenities` text COMMENT '基础设施描述',
  `generalAmenityIds` varchar(200) DEFAULT '' COMMENT '基础设施id,用|分割，对应type=0, hotelFacilityType=3',
  `roomAmenities` text COMMENT '房间设施描述',
  `recreationAmenities` text COMMENT '娱乐设施描述',
  `recreationAmenityIds` varchar(200) DEFAULT '' COMMENT '娱乐设施id,用|分割，对应type=0, hotelFacilityType=2',
  `conferenceAmenities` text COMMENT '服务设施描述',
  `conferenceAmenityIds` varchar(200) DEFAULT '' COMMENT '服务设施id,用|分割，对应type=0, hotelFacilityType=1',
  `diningAmenities` text COMMENT '餐厅设施描述',
  `traffic` text COMMENT '交通信息',
  `surroundings` text COMMENT '四周标志性建筑',
  `brandId` int(11) NOT NULL DEFAULT '0' COMMENT '百达屋品牌id',
  `facilities` varchar(200) NOT NULL DEFAULT '' COMMENT '通用设施id，用|分割，对应type=0, hotelFacilityType=0',
  `score` float NOT NULL DEFAULT '0' COMMENT '评分',
  `isValid` bit(1) NOT NULL DEFAULT b'1' COMMENT '是否生效',
  `isOnline` bit(1) NOT NULL DEFAULT b'1' COMMENT '是否上线',
  PRIMARY KEY (`id`),
  KEY `city` (`cityId`),
  KEY `district` (`districtId`),
  KEY `elongId` (`elongId`)
) ENGINE=InnoDB AUTO_INCREMENT=188212 DEFAULT CHARSET=utf8 COMMENT='酒店';

-- ----------------------------
--  Table structure for `hotelMapping`
-- ----------------------------
DROP TABLE IF EXISTS `hotelMapping`;
CREATE TABLE `hotelMapping` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `providerId` int(10) unsigned NOT NULL DEFAULT '0',
  `providerHotelId` int(10) unsigned NOT NULL DEFAULT '0',
  `mainHotelId` int(10) unsigned NOT NULL DEFAULT '0',
  `isFirstValid` bit(1) NOT NULL DEFAULT b'0',
  `isSecondValid` bit(1) NOT NULL DEFAULT b'0',
  `isOnline` bit(1) NOT NULL DEFAULT b'0',
  `tsUpdate` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `isDelete` bit(1) NOT NULL DEFAULT b'0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `image`
-- ----------------------------
DROP TABLE IF EXISTS `image`;
CREATE TABLE `image` (
  `id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '酒店或房型id',
  `url` varchar(300) DEFAULT '' COMMENT '图片url',
  `type` tinyint(4) NOT NULL DEFAULT '0' COMMENT '1 - 餐厅 2 - 休闲 3 - 会议室 5 - 外观 6 - 大堂/接待台 8 - 客房 10 - 其他 11 - 公共区域 12 - 周边景点',
  `size` tinyint(4) NOT NULL DEFAULT '0' COMMENT '自然数，数字越大图片越清晰',
  KEY `id-type` (`id`,`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='图片';

-- ----------------------------
--  Table structure for `pricingRule`
-- ----------------------------
DROP TABLE IF EXISTS `pricingRule`;
CREATE TABLE `pricingRule` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `providerId` int(10) unsigned NOT NULL,
  `otaId` int(20) NOT NULL,
  `hotelId` int(10) unsigned NOT NULL,
  `roomtTypeId` int(10) unsigned NOT NULL,
  `ratePlanId` int(10) unsigned NOT NULL DEFAULT '0',
  `type` int(10) unsigned NOT NULL,
  `value` double NOT NULL,
  `hotelName` varchar(20) CHARACTER SET latin1 NOT NULL,
  `roomTypeName` varchar(20) CHARACTER SET latin1 NOT NULL,
  `ratePlanName` varchar(20) CHARACTER SET latin1 NOT NULL,
  `startDate` datetime NOT NULL,
  `endDate` datetime NOT NULL,
  `tsUpdate` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `isDelete` bit(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `provider`
-- ----------------------------
DROP TABLE IF EXISTS `provider`;
CREATE TABLE `provider` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) CHARACTER SET latin1 NOT NULL,
  `contact` varchar(20) CHARACTER SET latin1 NOT NULL,
  `phone` varchar(50) CHARACTER SET latin1 NOT NULL,
  `email` varchar(200) CHARACTER SET latin1 DEFAULT NULL,
  `isDelete` bit(1) NOT NULL,
  `isOnline` bit(1) NOT NULL,
  `tsUpdate` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `type` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `province`
-- ----------------------------
DROP TABLE IF EXISTS `province`;
CREATE TABLE `province` (
  `id` int(11) unsigned NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `roomType`
-- ----------------------------
DROP TABLE IF EXISTS `roomType`;
CREATE TABLE `roomType` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `elongId` varchar(50) NOT NULL DEFAULT '0',
  `hotelId` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '百达屋酒店id',
  `name` varchar(50) NOT NULL DEFAULT '' COMMENT '房间名称',
  `area` float NOT NULL DEFAULT '0' COMMENT '房间大小',
  `floor` varchar(50) DEFAULT '' COMMENT '占据楼层',
  `broadnetAccess` bit(1) NOT NULL DEFAULT b'0' COMMENT '是否有网络',
  `broadnetFee` bit(1) NOT NULL DEFAULT b'0' COMMENT '网络是否收费',
  `comments` varchar(300) DEFAULT '' COMMENT '评价，须知',
  `description` varchar(300) DEFAULT '' COMMENT '介绍',
  `bedType` int(11) NOT NULL DEFAULT '-1' COMMENT '0单床 1大床 2双床 3三床 4三床-1大2单 5榻榻米 6拼床 7水床 8榻榻米双床 9榻榻米单床 10圆床 11上下铺 12 大床或双床 -1未知，需编辑',
  `capacity` tinyint(4) NOT NULL DEFAULT '0' COMMENT '可居住人数',
  `facility` varchar(200) DEFAULT '' COMMENT '设备id列表，用|分隔，对应type=1',
  `isValid` bit(1) DEFAULT b'0' COMMENT '是否有效',
  `isOnline` bit(1) DEFAULT b'0' COMMENT '是否上线',
  PRIMARY KEY (`id`),
  KEY `hotel` (`hotelId`),
  KEY `elongId` (`elongId`)
) ENGINE=InnoDB AUTO_INCREMENT=823264 DEFAULT CHARSET=utf8 COMMENT='房型';

-- ----------------------------
--  Table structure for `roomTypeMapping`
-- ----------------------------
DROP TABLE IF EXISTS `roomTypeMapping`;
CREATE TABLE `roomTypeMapping` (
  `Id` int(10) unsigned NOT NULL,
  `providerId` int(10) unsigned NOT NULL,
  `providerHotelId` int(10) unsigned NOT NULL,
  `providerRoomTypeId` int(10) unsigned NOT NULL,
  `mainHotelId` int(10) unsigned NOT NULL,
  `mainRoomTypeId` int(10) unsigned NOT NULL,
  `isFirstValid` bit(1) NOT NULL,
  `isSecondValid` bit(1) NOT NULL,
  `isOnline` bit(1) NOT NULL,
  `tsUpdate` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `isDelete` bit(1) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(20) CHARACTER SET latin1 NOT NULL,
  `password` varchar(50) CHARACTER SET latin1 NOT NULL,
  `nickname` varchar(20) CHARACTER SET latin1 NOT NULL,
  `lastLogin` datetime NOT NULL,
  `permission` int(10) unsigned NOT NULL,
  `department` varchar(20) DEFAULT NULL,
  `isDelete` bit(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;

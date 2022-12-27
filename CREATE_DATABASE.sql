/*
 Navicat Premium Data Transfer

 Source Server         : 云服务器
 Source Server Type    : MySQL
 Source Server Version : 50724 (5.7.24)
 Source Host           : 1.12.76.245:3306
 Source Schema         : covid

 Target Server Type    : MySQL
 Target Server Version : 50724 (5.7.24)
 File Encoding         : 65001

 Date: 27/12/2022 18:10:02
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for details_data
-- ----------------------------
DROP TABLE IF EXISTS `details_data`;
CREATE TABLE `details_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `update_date` datetime NOT NULL,
  `province` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `confirm` int(11) DEFAULT NULL,
  `confirm_add` int(11) DEFAULT NULL,
  `heal` int(11) DEFAULT NULL,
  `dead` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=113816 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for history_data
-- ----------------------------
DROP TABLE IF EXISTS `history_data`;
CREATE TABLE `history_data` (
  `update_date` date NOT NULL,
  `confirm` int(11) DEFAULT NULL,
  `confirm_add` int(11) DEFAULT NULL,
  `heal` int(11) DEFAULT NULL,
  `heal_add` int(11) DEFAULT NULL,
  `dead` int(11) DEFAULT NULL,
  `dead_add` int(11) DEFAULT NULL,
  PRIMARY KEY (`update_date`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for mainland_data
-- ----------------------------
DROP TABLE IF EXISTS `mainland_data`;
CREATE TABLE `mainland_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `update_date` datetime NOT NULL,
  `mainland_confirm_now` int(11) DEFAULT NULL,
  `mainland_confirm_add` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=213 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for province_confirm_now_data
-- ----------------------------
DROP TABLE IF EXISTS `province_confirm_now_data`;
CREATE TABLE `province_confirm_now_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `update_date` datetime NOT NULL,
  `province` varchar(50) DEFAULT NULL,
  `confirm_now` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=112864 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for risk_area_data
-- ----------------------------
DROP TABLE IF EXISTS `risk_area_data`;
CREATE TABLE `risk_area_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `update_date` datetime DEFAULT NULL,
  `province` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `county` varchar(255) DEFAULT NULL,
  `community` varchar(1024) DEFAULT NULL,
  `grade` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1954919 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;

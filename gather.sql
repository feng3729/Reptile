/*
Navicat MySQL Data Transfer

Source Server         : 90news
Source Server Version : 50556
Source Host           : 139.199.36.39:3306
Source Database       : gather

Target Server Type    : MYSQL
Target Server Version : 50556
File Encoding         : 65001

Date: 2018-05-25 09:42:59
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for cj_qishu_dushi
-- ----------------------------
DROP TABLE IF EXISTS `cj_qishu_dushi`;
CREATE TABLE `cj_qishu_dushi` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL DEFAULT '',
  `author` varchar(50) NOT NULL DEFAULT '',
  `desc` varchar(200) NOT NULL DEFAULT '',
  `downUrl` varchar(100) NOT NULL DEFAULT '',
  `thumb` varchar(100) NOT NULL DEFAULT '',
  `size` varchar(10) NOT NULL DEFAULT '0',
  `updatetime` varchar(20) NOT NULL DEFAULT '0',
  `createtime` varchar(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `tit_size_type` (`title`,`size`)
) ENGINE=InnoDB AUTO_INCREMENT=298 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for cj_qishu_junshi
-- ----------------------------
DROP TABLE IF EXISTS `cj_qishu_junshi`;
CREATE TABLE `cj_qishu_junshi` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL DEFAULT '',
  `author` varchar(50) NOT NULL DEFAULT '',
  `desc` varchar(200) NOT NULL DEFAULT '',
  `downUrl` varchar(100) NOT NULL DEFAULT '',
  `thumb` varchar(100) NOT NULL DEFAULT '',
  `size` varchar(10) NOT NULL DEFAULT '0',
  `updatetime` varchar(20) NOT NULL DEFAULT '0',
  `createtime` varchar(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `tit_size_type` (`title`,`size`)
) ENGINE=InnoDB AUTO_INCREMENT=126 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for cj_qishu_wuxia
-- ----------------------------
DROP TABLE IF EXISTS `cj_qishu_wuxia`;
CREATE TABLE `cj_qishu_wuxia` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL DEFAULT '',
  `author` varchar(50) NOT NULL DEFAULT '',
  `desc` varchar(200) NOT NULL DEFAULT '',
  `downUrl` varchar(100) NOT NULL DEFAULT '',
  `thumb` varchar(100) NOT NULL DEFAULT '',
  `size` varchar(10) NOT NULL DEFAULT '0',
  `updatetime` varchar(20) NOT NULL DEFAULT '0',
  `updatecon` varchar(100) NOT NULL DEFAULT '',
  `createtime` varchar(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `tit_size_type` (`title`,`size`)
) ENGINE=InnoDB AUTO_INCREMENT=136 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for cj_qishu_xuanhuan
-- ----------------------------
DROP TABLE IF EXISTS `cj_qishu_xuanhuan`;
CREATE TABLE `cj_qishu_xuanhuan` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL DEFAULT '',
  `author` varchar(50) NOT NULL DEFAULT '',
  `desc` varchar(200) NOT NULL DEFAULT '',
  `downUrl` varchar(100) NOT NULL DEFAULT '',
  `thumb` varchar(100) NOT NULL DEFAULT '',
  `updatecon` varchar(100) NOT NULL DEFAULT '',
  `size` varchar(10) NOT NULL DEFAULT '0',
  `updatetime` varchar(20) NOT NULL DEFAULT '0',
  `createtime` varchar(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `tit_size_type` (`title`,`size`)
) ENGINE=InnoDB AUTO_INCREMENT=265 DEFAULT CHARSET=utf8;

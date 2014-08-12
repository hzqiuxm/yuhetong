/*
Navicat MySQL Data Transfer

Source Server         : lvxun
Source Server Version : 50615
Source Host           : 218.244.135.22:3306
Source Database       : lvxunDev

Target Server Type    : MYSQL
Target Server Version : 50615
File Encoding         : 65001

Date: 2014-08-10 16:18:49
*/

-- ----------------------------
-- Table structure for `lxuser`
-- ----------------------------
DROP TABLE IF EXISTS `lxuser`;
CREATE TABLE `lxuser` (
  `id` int(16) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id主键',
  `type` tinyint NOT NULL COMMENT '用户类型 先设置1',
  `userName` varchar(80) COLLATE utf8_bin NOT NULL COMMENT '用户名',
  `realName` varchar(80) COLLATE utf8_bin COMMENT '真实姓名',
  `passwd` varchar(50) COLLATE utf8_bin NOT NULL COMMENT '用户密码',
  `email` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '用户邮箱',
  `phone` varchar(20) COLLATE utf8_bin DEFAULT NULL COMMENT '用户联系电话',
  `parentUserId` int(16)  default 0 COMMENT '主账户id,
  子账户具有的属性，有该属性表示是子账户',
  `companyId` int(16)  default 0 COMMENT '对应的公司id',
  `createTime` TIMESTAMP NOT NULL DEFAULT 0 COMMENT '用户创建时间',
  `modifyTime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最近修改时间',
  `signId` int(16) DEFAULT NULL COMMENT '用户签名Id',
  `status` tinyint  DEFAULT NULL COMMENT '用户状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='用户表';

-- ----------------------------
-- Table structure for `lxcompany`
-- ----------------------------
DROP TABLE IF EXISTS `lxcompany`;
CREATE TABLE `lxcompany` (
  `id` int(16) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id主键',
  `type` tinyint   COMMENT '公司类型 先设置1',
  `name` varchar(80) COLLATE utf8_bin COMMENT '公司名称',
  `field1` varchar(80) COLLATE utf8_bin COMMENT '公司认证信息字段',
  `field2` varchar(80) COLLATE utf8_bin COMMENT '公司证信息字段',
  `field3` varchar(80) COLLATE utf8_bin COMMENT '公司证信息字段',
  `createTime` TIMESTAMP NOT NULL DEFAULT 0 COMMENT '创建时间',
  `modifyTime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最近修改时间',
  `status` tinyint  DEFAULT NULL COMMENT '文件状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='公司表';

-- ----------------------------
-- Table structure for `lxcontract`
-- ----------------------------
DROP TABLE IF EXISTS `lxcontract`;
CREATE TABLE `lxcontract` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id主键',
  `type` tinyint  NOT NULL COMMENT '合同类型',
  `name` varchar(80) COLLATE utf8_bin NOT NULL COMMENT '合同名称',
  `readPermUsers` varchar(1024) COLLATE utf8_bin NOT NULL COMMENT
    '具有读权限的用户列表，json格式',
  `writePermUsers` varchar(1024) COLLATE utf8_bin NOT NULL COMMENT
    '具有写权限的用户列表，json格式',
  `signPermUsers` varchar(1024) COLLATE utf8_bin NOT NULL COMMENT '用户邮箱',
  `ownerId` varchar(10) COLLATE utf8_bin NOT NULL COMMENT '所有者 user id',
  `nowFid` varchar(10) COLLATE utf8_bin NOT NULL COMMENT '目前合同文件对应的fid',
  `draftFid` varchar(10) COLLATE utf8_bin NOT NULL COMMENT '合同草稿对应的fid',
  `issuedFid` varchar(10) COLLATE utf8_bin NOT NULL COMMENT '合同正式稿版本1 对应的fid',
  `issuedFid2` varchar(10) COLLATE utf8_bin NOT NULL COMMENT '合同正式稿版本2 对应的fid',
  `issuedFid3` varchar(10) COLLATE utf8_bin NOT NULL COMMENT '合同正式稿版本3 对应的fid',
  `issuedFid4` varchar(10) COLLATE utf8_bin NOT NULL COMMENT '合同正式稿版本4 对应的fid',
  `issuedFid5` varchar(10) COLLATE utf8_bin NOT NULL COMMENT '合同正式稿版本5 对应的fid',
  `fixedFid` varchar(10) COLLATE utf8_bin NOT NULL COMMENT '合同确定稿版本对应的fid',
  `createTime` TIMESTAMP NOT NULL DEFAULT 0 COMMENT '创建时间',
  `modifyTime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最近修改时间',
  `status` tinyint  DEFAULT NULL COMMENT '合同状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='合同表';

-- ----------------------------
-- Table structure for `lxfile`
-- ----------------------------
DROP TABLE IF EXISTS `lxfile`;
CREATE TABLE `lxfile` (
  `id` int(16) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id主键',
  `fuuid` varchar(32)  NOT NULL  COMMENT 'file uuid.hex',
  `type` tinyint NOT NULL COMMENT '文件类型',
  `name` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '文件名称',
  `createTime` TIMESTAMP NOT NULL DEFAULT 0 COMMENT '创建时间',
  `modifyTime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最近修改时间',
  `status` tinyint DEFAULT NULL COMMENT '文件状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='文件表';


INSERT INTO wenwu_test.lxuser ( type, userName, realName, passwd, email, phone, parentUserId, companyId, createTime, modifyTime, signId, status) VALUES ( '1', 'sampleUser', 'test', '1', 'account@yunhetong.com', '1234567', '', '', '2014-08-12 15:19:48.0', '2014-08-12 15:19:52.0', '', '1');
INSERT INTO wenwu_test.lxcompany ( type, name, field1, field2, field3, createTime, modifyTime, status) VALUES ('1', 'test', '11', '22', '33', '2014-08-12 15:24:40.0', '2014-08-12 15:24:43.0', '1');
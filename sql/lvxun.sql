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
  `username` varchar(80) COLLATE utf8_bin NOT NULL UNIQUE COMMENT '用户名',
  `real_name` varchar(80) COLLATE utf8_bin COMMENT '真实姓名',
  `passwd` varchar(50) COLLATE utf8_bin NOT NULL COMMENT '用户密码',
  `email` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '用户邮箱',
  `phone` varchar(20) COLLATE utf8_bin DEFAULT NULL COMMENT '用户联系电话',
  `parent_user_id` int(16)  default 0 COMMENT '主账户id,
  子账户具有的属性，有该属性表示是子账户',
  `company_id` int(16)  default 0 COMMENT '对应的公司id',
  `gmt_create` TIMESTAMP NOT NULL DEFAULT 0 COMMENT '用户创建时间',
  `gmt_modify` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最近修改时间',
  `sign_id` int(16) DEFAULT NULL COMMENT '用户签名Id',
  `status` tinyint  DEFAULT 1 COMMENT '用户状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='用户表';

-- ----------------------------
-- Table structure for `lxcompany`
-- ----------------------------
DROP TABLE IF EXISTS `lxcompany`;
CREATE TABLE `lxcompany` (
  `id` int(16) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id主键',
  `type` tinyint   COMMENT '公司类型 先设置1',
  `name` varchar(128) COLLATE utf8_bin COMMENT '公司名称',
  `field1` varchar(80) COLLATE utf8_bin COMMENT '公司认证信息字段',
  `field2` varchar(80) COLLATE utf8_bin COMMENT '公司证信息字段',
  `field3` varchar(80) COLLATE utf8_bin COMMENT '公司证信息字段',
  `gmt_create` TIMESTAMP NOT NULL DEFAULT 0 COMMENT '创建时间',
  `gmt_modify` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最近修改时间',
  `status` tinyint  DEFAULT 1 COMMENT '文件状态',
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
  `read_perm_users` varchar(1024) COLLATE utf8_bin NOT NULL COMMENT
    '具有读权限的用户列表，json格式',
  `write_perm_users` varchar(1024) COLLATE utf8_bin NOT NULL COMMENT
    '具有写权限的用户列表，json格式',
  `sign_perm_users` varchar(1024) COLLATE utf8_bin NOT NULL COMMENT '用户邮箱',
  `owner_id` varchar(10) COLLATE utf8_bin NOT NULL COMMENT '所有者 user id',
  `now_fid` varchar(10) COLLATE utf8_bin NOT NULL COMMENT '目前合同文件对应的fid',
  `draft_fid` varchar(10) COLLATE utf8_bin NOT NULL COMMENT '合同草稿对应的fid',
  `issued_fid` varchar(10) COLLATE utf8_bin NOT NULL COMMENT '合同正式稿版本1 对应的fid',
  `issued_fid2` varchar(10) COLLATE utf8_bin NOT NULL COMMENT '合同正式稿版本2 对应的fid',
  `issued_fid3` varchar(10) COLLATE utf8_bin NOT NULL COMMENT '合同正式稿版本3 对应的fid',
  `issued_fid4` varchar(10) COLLATE utf8_bin NOT NULL COMMENT '合同正式稿版本4 对应的fid',
  `issued_fid5` varchar(10) COLLATE utf8_bin NOT NULL COMMENT '合同正式稿版本5 对应的fid',
  `fixed_fid` varchar(10) COLLATE utf8_bin NOT NULL COMMENT '合同确定稿版本对应的fid',
  `gmt_create` TIMESTAMP NOT NULL DEFAULT 0 COMMENT '创建时间',
  `gmt_modify` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最近修改时间',
  `status` tinyint  DEFAULT 1 COMMENT '合同状态',
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
  `extension` varchar(8) COLLATE utf8_bin NOT NULL COMMENT '文件扩展名',
  `fpath` varchar(256) COLLATE utf8_bin NOT NULL COMMENT '文件路径',
  `gmt_create` TIMESTAMP NOT NULL DEFAULT 0 COMMENT '创建时间',
  `gmt_modify` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最近修改时间',
  `status` tinyint DEFAULT 1 COMMENT '文件状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='文件表';

-- ----------------------------
-- Table structure for `lxtemptype`
-- ----------------------------
DROP TABLE IF EXISTS `lxtemptype`;
CREATE TABLE `lxtemptype` (
  `id` int(16) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id主键',
  `name` varchar(64)  NOT NULL  COMMENT '模版名称',
  `level` tinyint NOT NULL COMMENT '模版类型层级（0，1，2）三级',
  `parent_id` int(16) COMMENT '父模版类型',
  `gmt_create` TIMESTAMP NOT NULL DEFAULT 0 COMMENT '创建时间',
  `gmt_modify` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最近修改时间',
  `status` tinyint DEFAULT 1 COMMENT '文件状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='模版类型表';

-- ----------------------------
-- Table structure for `lxtemplate`
-- ----------------------------
DROP TABLE IF EXISTS `lxtemplate`;
CREATE TABLE `lxtemplate` (
  `id` int(16) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id主键',
  `name` varchar(64)  NOT NULL  COMMENT '模版名称',
  `type_id` tinyint NOT NULL COMMENT '模板类型',
  `owner_id` int(16)   COMMENT '模版所有者',
  `content` text  COMMENT '模版内容',
  `gmt_create` TIMESTAMP NOT NULL DEFAULT 0 COMMENT '创建时间',
  `gmt_modify` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最近修改时间',
  `status` tinyint DEFAULT 1 COMMENT '模版状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='文件表';


INSERT INTO wenwu_test.lxuser ( type, username, real_name, passwd, email, phone, parent_user_id, company_id, gmt_create, gmt_modify, sign_id, status) VALUES ( '1', 'sampleUser', 'test', '1', 'account@yunhetong.com', '1234567', 1, 1, '2014-08-12 15:19:48.0', '2014-08-12 15:19:52.0', 1, 1);
INSERT INTO wenwu_test.lxcompany ( type, name, field1, field2, field3, gmt_create, gmt_modify, status) VALUES ('1', 'test', '11', '22', '33', '2014-08-12 15:24:40.0', '2014-08-12 15:24:43.0', '1');


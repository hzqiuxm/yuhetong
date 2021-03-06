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
-- Table structure for 'lxuser'
-- ----------------------------
DROP TABLE IF EXISTS 'lxuser';
CREATE TABLE 'lxuser' (
  'id' int(16) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id主键',
  'type' tinyint NOT NULL COMMENT '用户类型 先设置1',
  'username' varchar(80) COLLATE utf8_bin NOT NULL UNIQUE COMMENT '用户名',
  'real_name' varchar(80) COLLATE utf8_bin COMMENT '真实姓名',
  'passwd' varchar(128) COLLATE utf8_bin NOT NULL COMMENT '用户密码',
  'email' varchar(64) COLLATE utf8_bin NOT NULL COMMENT '用户邮箱',
  'phone' varchar(20) COLLATE utf8_bin DEFAULT NULL COMMENT '用户联系电话',
  'idCardNo'  varchar(20) COLLATE utf8_bin COMMENT '用户的身份证号码',
  'idCardimg1' varchar(100)  COLLATE utf8_bin COMMENT '用户身份证正面照片地址' ,
  'idCardimg2' varchar(100) COLLATE utf8_bin COMMENT '用户身份证正面照片地址',
  'shouhanimg' varchar(100) COLLATE utf8_bin COMMENT '企业受涵文件地址',
  'parent_user_id' int(16)  default 0 COMMENT '主账户id,
  子账户具有的属性，有该属性表示是子账户',
  'company_id' int(16)  default 0 COMMENT '对应的公司id',
  'create_time' TIMESTAMP NOT NULL DEFAULT 0 COMMENT '用户创建时间',
  'modify_time' TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最近修改时间',
  'address' varchar(100) COMMENT '通讯地址',
  'sign_id' int(16) DEFAULT NULL COMMENT '用户签名Id',
  'status' tinyint  DEFAULT NULL COMMENT '用户状态',
  PRIMARY KEY ('id')
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='用户表';

-- ----------------------------
-- Table structure for 'lxcompany'
-- ----------------------------
DROP TABLE IF EXISTS 'lxcompany';
CREATE TABLE 'lxcompany' (
  'id' int(16) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id主键',
  'name' varchar(128)  COMMENT '公司名称',
  'orzNo' varchar(20) COMMENT '组织机构代码',
  'orzimg' varchar(100) COMMENT '组织机构代码证扫描件',
  'yyzyNo' varchar(20) COMMENT '营业执照号码',
  'yyzyimg' varchar(100) COMMENT '营业执照扫描件',
  'type' tinyint   COMMENT '公司类型 先设置1',
  'legal_person' varchar(80) COLLATE utf8_bin COMMENT '法人代表',
  'address' varchar(80) COLLATE utf8_bin COMMENT '公司地址',
  'create_time' TIMESTAMP NOT NULL DEFAULT 0 COMMENT '创建时间',
  'modify_time' TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最近修改时间',
  'status' tinyint  DEFAULT NULL COMMENT '文件状态',
  PRIMARY KEY ('id')
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='公司表';

-- ----------------------------
-- Table structure for 'lxcontract'
-- ----------------------------
DROP TABLE IF EXISTS 'lxcontract';
CREATE TABLE 'lxcontract' (
  'id' int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id主键',
  'type' tinyint  NOT NULL COMMENT '合同类型',
  'name' varchar(80) COLLATE utf8_bin NOT NULL COMMENT '合同名称',
  'read_perm_users' varchar(1024) COLLATE utf8_bin NOT NULL COMMENT
    '具有读权限的用户列表，json格式',
  'write_perm_users' varchar(1024) COLLATE utf8_bin NOT NULL COMMENT
    '具有写权限的用户列表，json格式',
  'sign_perm_users' varchar(1024) COLLATE utf8_bin NOT NULL COMMENT '用户邮箱',
  'owner_id' varchar(10) COLLATE utf8_bin NOT NULL COMMENT '所有者 user id',
  'now_fid' varchar(10) COLLATE utf8_bin NOT NULL COMMENT '目前合同文件对应的fid',
  'draft_fid' varchar(10) COLLATE utf8_bin NOT NULL COMMENT '合同草稿对应的fid',
  'issued_fid' varchar(10) COLLATE utf8_bin NOT NULL COMMENT '合同正式稿版本1 对应的fid',
  'issued_fid2' varchar(10) COLLATE utf8_bin NOT NULL COMMENT '合同正式稿版本2 对应的fid',
  'issued_fid3' varchar(10) COLLATE utf8_bin NOT NULL COMMENT '合同正式稿版本3 对应的fid',
  'issued_fid4' varchar(10) COLLATE utf8_bin NOT NULL COMMENT '合同正式稿版本4 对应的fid',
  'issued_fid5' varchar(10) COLLATE utf8_bin NOT NULL COMMENT '合同正式稿版本5 对应的fid',
  'fixed_fid' varchar(10) COLLATE utf8_bin NOT NULL COMMENT '合同确定稿版本对应的fid',
  'create_time' TIMESTAMP NOT NULL DEFAULT 0 COMMENT '创建时间',
  'modify_time' TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最近修改时间',
  'status' tinyint  DEFAULT NULL COMMENT '合同状态',
  PRIMARY KEY ('id')
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='合同表';

-- ----------------------------
-- Table structure for 'lxfile'
-- ----------------------------
DROP TABLE IF EXISTS 'lxfile';
CREATE TABLE 'lxfile' (
  'id' int(16) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id主键',
  'fuuid' varchar(32)  NOT NULL  COMMENT 'file uuid.hex',
  'type' tinyint NOT NULL COMMENT '文件类型',
  'name' varchar(64) COLLATE utf8_bin NOT NULL COMMENT '文件名称',
  'extension' varchar(8) COLLATE utf8_bin NOT NULL COMMENT '文件扩展名',
  'fpath' varchar(256) COLLATE utf8_bin NOT NULL COMMENT '文件路径',
  'create_time' TIMESTAMP NOT NULL DEFAULT 0 COMMENT '创建时间',
  'modify_time' TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最近修改时间',
  'status' tinyint DEFAULT NULL COMMENT '文件状态',
  PRIMARY KEY ('id')
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='文件表';

-- ----------------------------
-- Table structure for 'lxtemptype'
-- ----------------------------
DROP TABLE IF EXISTS 'lxtemptype';
CREATE TABLE 'lxtemptype' (
  'id' int(16) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id主键',
  'name' varchar(64)  NOT NULL  COMMENT '模版名称',
  'level' tinyint NOT NULL COMMENT '模版类型层级（0，1，2）三级',
  'parent' int(16) NOT NULL COMMENT '父模版类型',
  'create_time' TIMESTAMP NOT NULL DEFAULT 0 COMMENT '创建时间',
  'modify_time' TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最近修改时间',
  'status' tinyint DEFAULT NULL COMMENT '文件状态',
  PRIMARY KEY ('id')
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='模版类型表';

-- ----------------------------
-- Table structure for 'lxtemplate'
-- ----------------------------
DROP TABLE IF EXISTS 'lxtemplate';
CREATE TABLE 'lxtemplate' (
  'id' int(16) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id主键',
  'name' varchar(64)  NOT NULL  COMMENT '模版名称',
  'type_id' tinyint NOT NULL COMMENT '模板类型',
  'owner_id' int(16)  NOT NULL default 0 COMMENT '模版所有者',
  'content' text  COMMENT '模版内容',
  'create_time' TIMESTAMP NOT NULL DEFAULT 0 COMMENT '创建时间',
  'modify_time' TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最近修改时间',
  'status' tinyint DEFAULT NULL COMMENT '模版状态',
  PRIMARY KEY ('id')
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='文件表';

-- ----------------------------
-- Table structure for 'lxemail'
-- ----------------------------
DROP TABLE IF EXISTS 'lxemail';
CREATE TABLE 'lxemail' (
  'id' int(11) NOT NULL,
  'eFrom' varchar(50) COLLATE utf8_bin NOT NULL DEFAULT '发件人',
  'eTo' varchar(50) COLLATE utf8_bin NOT NULL COMMENT '收件人',
  'eSubject' varchar(100) COLLATE utf8_bin NOT NULL COMMENT '邮件主题',
  'eContent' varchar(1000) COLLATE utf8_bin NOT NULL COMMENT '邮件内容',
  'eSentTime' datetime NOT NULL COMMENT '邮件发送时间',
  PRIMARY KEY ('id')
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Table structure for 'lxcontract'
-- ----------------------------
DROP TABLE IF EXISTS 'lxcontract';
CREATE TABLE 'lxcontract' (
  'id' int(11) NOT NULL,
  'stage' int(11) COMMENT '合同签订阶段',
  'name' varchar (128) COMMENT '合同名称',

  'participants' varchar (256) COMMENT '合同参与方 user id list',
  'write_perm_users' varchar (256) COMMENT '拥有写权限的用户列表',
  'read_perm_users' varchar (256) COMMENT '拥有读权限的用户列表',
  'sign_perm_users' varchar (256) COMMENT '拥有签权限的用户列表',

  'owner_id' int(16)  COMMENT '合同所有者',
  'draft' int(16)  COMMENT '合同草稿',
  'file_id_v1' int(16)  COMMENT '合同文件v1',
  'file_id_v2' int(16)  COMMENT '合同文件v2',
  'file_id_v3' int(16)  COMMENT '合同文件v3',
  'file_id_v4' int(16)  COMMENT '合同文件v4',
  'file_id_v5' int(16)  COMMENT '合同文件v5',
  PRIMARY KEY ('id')
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


INSERT INTO wenwu_test.lxuser ( type, username, real_name, passwd, email, phone, parent_user_id, company_id, create_time, modify_time, sign_id, status) VALUES ( '1', 'sampleUser', 'test', '1', 'account@yunhetong.com', '1234567', 1, 1, '2014-08-12 15:19:48.0', '2014-08-12 15:19:52.0', 1, 1);
INSERT INTO wenwu_test.lxcompany ( type, name, field1, field2, field3, create_time, modify_time, status) VALUES ('1', 'test', '11', '22', '33', '2014-08-12 15:24:40.0', '2014-08-12 15:24:43.0', '1');


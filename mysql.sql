-- MySQL dump 10.14  Distrib 5.5.37-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: seanwuTest
-- ------------------------------------------------------
-- Server version	5.5.37-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `lxcompany`
--

DROP TABLE IF EXISTS `lxcompany`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lxcompany` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` int(11) NOT NULL,
  `gmt_modify` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `gmt_create` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `type` int(11) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `organizationNo` varchar(50) DEFAULT NULL,
  `organization_img` varchar(100) DEFAULT NULL,
  `business_license_No` varchar(50) DEFAULT NULL,
  `business_license_img` varchar(100) DEFAULT NULL,
  `legal_person` varchar(10) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lxcompany`
--

LOCK TABLES `lxcompany` WRITE;
/*!40000 ALTER TABLE `lxcompany` DISABLE KEYS */;
/*!40000 ALTER TABLE `lxcompany` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lxcontract`
--

DROP TABLE IF EXISTS `lxcontract`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lxcontract` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` int(11) NOT NULL,
  `gmt_modify` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `gmt_create` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `stage` int(11) NOT NULL,
  `name` varchar(64) NOT NULL,
  `appendix` varchar(256) NOT NULL,
  `take_passwd` varchar(256) DEFAULT NULL,
  `part_num` int(11) NOT NULL,
  `version` int(11) NOT NULL,
  `gmt_expire` timestamp NULL DEFAULT NULL,
  `draft_fid` int(11) DEFAULT NULL,
  `contract_v1_fid` int(11) DEFAULT NULL,
  `contract_v2_fid` int(11) DEFAULT NULL,
  `contract_v3_fid` int(11) DEFAULT NULL,
  `contract_v4_fid` int(11) DEFAULT NULL,
  `contract_v5_fid` int(11) DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `draft_fid` (`draft_fid`),
  KEY `contract_v1_fid` (`contract_v1_fid`),
  KEY `contract_v2_fid` (`contract_v2_fid`),
  KEY `contract_v3_fid` (`contract_v3_fid`),
  KEY `contract_v4_fid` (`contract_v4_fid`),
  KEY `contract_v5_fid` (`contract_v5_fid`),
  KEY `owner_id` (`owner_id`),
  CONSTRAINT `lxcontract_ibfk_1` FOREIGN KEY (`draft_fid`) REFERENCES `lxfile` (`id`),
  CONSTRAINT `lxcontract_ibfk_2` FOREIGN KEY (`contract_v1_fid`) REFERENCES `lxfile` (`id`),
  CONSTRAINT `lxcontract_ibfk_3` FOREIGN KEY (`contract_v2_fid`) REFERENCES `lxfile` (`id`),
  CONSTRAINT `lxcontract_ibfk_4` FOREIGN KEY (`contract_v3_fid`) REFERENCES `lxfile` (`id`),
  CONSTRAINT `lxcontract_ibfk_5` FOREIGN KEY (`contract_v4_fid`) REFERENCES `lxfile` (`id`),
  CONSTRAINT `lxcontract_ibfk_6` FOREIGN KEY (`contract_v5_fid`) REFERENCES `lxfile` (`id`),
  CONSTRAINT `lxcontract_ibfk_7` FOREIGN KEY (`owner_id`) REFERENCES `lxuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lxcontract`
--

LOCK TABLES `lxcontract` WRITE;
/*!40000 ALTER TABLE `lxcontract` DISABLE KEYS */;
/*!40000 ALTER TABLE `lxcontract` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lxcontractauthorization`
--

DROP TABLE IF EXISTS `lxcontractauthorization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lxcontractauthorization` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` int(11) NOT NULL,
  `gmt_modify` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `gmt_create` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `read_perm` int(11) NOT NULL,
  `write_perm` int(11) NOT NULL,
  `sign_perm` int(11) NOT NULL,
  `auth_passwd` varchar(256) DEFAULT NULL,
  `gmt_expire` timestamp NULL DEFAULT NULL,
  `contract_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `auth_own_user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `contract_id` (`contract_id`),
  KEY `user_id` (`user_id`),
  KEY `auth_own_user_id` (`auth_own_user_id`),
  CONSTRAINT `lxcontractauthorization_ibfk_1` FOREIGN KEY (`contract_id`) REFERENCES `lxcontract` (`id`),
  CONSTRAINT `lxcontractauthorization_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `lxuser` (`id`),
  CONSTRAINT `lxcontractauthorization_ibfk_3` FOREIGN KEY (`auth_own_user_id`) REFERENCES `lxuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lxcontractauthorization`
--

LOCK TABLES `lxcontractauthorization` WRITE;
/*!40000 ALTER TABLE `lxcontractauthorization` DISABLE KEYS */;
/*!40000 ALTER TABLE `lxcontractauthorization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lxcontractparticipation`
--

DROP TABLE IF EXISTS `lxcontractparticipation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lxcontractparticipation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` int(11) NOT NULL,
  `gmt_modify` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `gmt_create` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `stage` int(11) NOT NULL,
  `is_owner` int(11) NOT NULL,
  `contract_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `contract_id` (`contract_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `lxcontractparticipation_ibfk_1` FOREIGN KEY (`contract_id`) REFERENCES `lxcontract` (`id`),
  CONSTRAINT `lxcontractparticipation_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `lxuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lxcontractparticipation`
--

LOCK TABLES `lxcontractparticipation` WRITE;
/*!40000 ALTER TABLE `lxcontractparticipation` DISABLE KEYS */;
/*!40000 ALTER TABLE `lxcontractparticipation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lxemail`
--

DROP TABLE IF EXISTS `lxemail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lxemail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` int(11) NOT NULL,
  `gmt_modify` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `gmt_create` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `eTo` varchar(50) NOT NULL,
  `eFrom` varchar(50) NOT NULL,
  `eSubject` varchar(100) NOT NULL,
  `eContent` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lxemail`
--

LOCK TABLES `lxemail` WRITE;
/*!40000 ALTER TABLE `lxemail` DISABLE KEYS */;
/*!40000 ALTER TABLE `lxemail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lxfile`
--

DROP TABLE IF EXISTS `lxfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lxfile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` int(11) NOT NULL,
  `gmt_modify` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `gmt_create` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `type` int(11) DEFAULT NULL,
  `fuuid` varchar(64) NOT NULL,
  `name` varchar(64) NOT NULL,
  `extension` varchar(8) DEFAULT NULL,
  `fpath` varchar(256) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `fuuid` (`fuuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lxfile`
--

LOCK TABLES `lxfile` WRITE;
/*!40000 ALTER TABLE `lxfile` DISABLE KEYS */;
/*!40000 ALTER TABLE `lxfile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lxsign`
--

DROP TABLE IF EXISTS `lxsign`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lxsign` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` int(11) NOT NULL,
  `gmt_modify` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `gmt_create` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `owner_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `owner_id` (`owner_id`),
  CONSTRAINT `lxsign_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `lxuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lxsign`
--

LOCK TABLES `lxsign` WRITE;
/*!40000 ALTER TABLE `lxsign` DISABLE KEYS */;
/*!40000 ALTER TABLE `lxsign` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lxtemplate`
--

DROP TABLE IF EXISTS `lxtemplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lxtemplate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` int(11) NOT NULL,
  `gmt_modify` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `gmt_create` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `name` varchar(64) NOT NULL,
  `content` text,
  `owner_id` int(11) DEFAULT NULL,
  `type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `owner_id` (`owner_id`),
  KEY `type_id` (`type_id`),
  CONSTRAINT `lxtemplate_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `lxuser` (`id`),
  CONSTRAINT `lxtemplate_ibfk_2` FOREIGN KEY (`type_id`) REFERENCES `lxtemptype` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lxtemplate`
--

LOCK TABLES `lxtemplate` WRITE;
/*!40000 ALTER TABLE `lxtemplate` DISABLE KEYS */;
/*!40000 ALTER TABLE `lxtemplate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lxtemptype`
--

DROP TABLE IF EXISTS `lxtemptype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lxtemptype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` int(11) NOT NULL,
  `gmt_modify` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `gmt_create` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `level` int(11) DEFAULT NULL,
  `name` varchar(64) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `parent_id` (`parent_id`),
  CONSTRAINT `lxtemptype_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `lxtemptype` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lxtemptype`
--

LOCK TABLES `lxtemptype` WRITE;
/*!40000 ALTER TABLE `lxtemptype` DISABLE KEYS */;
/*!40000 ALTER TABLE `lxtemptype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lxuser`
--

DROP TABLE IF EXISTS `lxuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lxuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` int(11) NOT NULL,
  `gmt_modify` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `gmt_create` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `type` int(11) DEFAULT NULL,
  `username` varchar(128) NOT NULL,
  `real_name` varchar(128) DEFAULT NULL,
  `passwd` varchar(128) NOT NULL,
  `email` varchar(64) NOT NULL,
  `phone` varchar(32) DEFAULT NULL,
  `idCardNo` varchar(50) DEFAULT NULL,
  `idCardimg1` varchar(100) DEFAULT NULL,
  `idCardimg2` varchar(100) DEFAULT NULL,
  `authorization_img` varchar(100) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `parent_id` (`parent_id`),
  KEY `company_id` (`company_id`),
  CONSTRAINT `lxuser_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `lxuser` (`id`),
  CONSTRAINT `lxuser_ibfk_2` FOREIGN KEY (`company_id`) REFERENCES `lxcompany` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lxuser`
--

LOCK TABLES `lxuser` WRITE;
/*!40000 ALTER TABLE `lxuser` DISABLE KEYS */;
/*!40000 ALTER TABLE `lxuser` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-10-13  2:46:00

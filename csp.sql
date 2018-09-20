-- MySQL dump 10.13  Distrib 5.6.41, for Win64 (x86_64)
--
-- Host: localhost    Database: csp
-- ------------------------------------------------------
-- Server version	5.6.41

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
-- Table structure for table `guanliban`
--

DROP TABLE IF EXISTS `guanliban`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `guanliban` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `specialities` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '专业',
  `grade` varchar(255) CHARACTER SET utf8 NOT NULL,
  `class` varchar(255) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guanliban`
--

LOCK TABLES `guanliban` WRITE;
/*!40000 ALTER TABLE `guanliban` DISABLE KEYS */;
INSERT INTO `guanliban` VALUES (6,'信息安全','2015级','3班'),(7,'信息安全','2014级','2班'),(8,'网络工程','2015级','1班'),(9,'网络工程','2016级','1班');
/*!40000 ALTER TABLE `guanliban` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jihuaxijie`
--

DROP TABLE IF EXISTS `jihuaxijie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jihuaxijie` (
  `coursename` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `coursetime` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `courseplan` varchar(255) CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jihuaxijie`
--

LOCK TABLES `jihuaxijie` WRITE;
/*!40000 ALTER TABLE `jihuaxijie` DISABLE KEYS */;
INSERT INTO `jihuaxijie` VALUES ('网络安全','张三','闭卷'),('操作系统','李四','开卷');
/*!40000 ALTER TABLE `jihuaxijie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paike_js`
--

DROP TABLE IF EXISTS `paike_js`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `paike_js` (
  `course_name` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '课程时间',
  `course_class` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `course_plan` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '课程计划'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paike_js`
--

LOCK TABLES `paike_js` WRITE;
/*!40000 ALTER TABLE `paike_js` DISABLE KEYS */;
INSERT INTO `paike_js` VALUES ('操作系统','教三B201','5、6节'),('网络安全','教一C502','7、8节');
/*!40000 ALTER TABLE `paike_js` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `username` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('admin','admin');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_status`
--

DROP TABLE IF EXISTS `user_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_status` (
  `id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_status`
--

LOCK TABLES `user_status` WRITE;
/*!40000 ALTER TABLE `user_status` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `xueshengchengji`
--

DROP TABLE IF EXISTS `xueshengchengji`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xueshengchengji` (
  `course_name` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `student_name` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `student_class` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `student_score` varchar(255) CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `xueshengchengji`
--

LOCK TABLES `xueshengchengji` WRITE;
/*!40000 ALTER TABLE `xueshengchengji` DISABLE KEYS */;
INSERT INTO `xueshengchengji` VALUES ('12','王三','操作系统','78'),('33','刘四','网络安全','88'),('23','李四','操作系统','88'),('23','李四','网络安全','98');
/*!40000 ALTER TABLE `xueshengchengji` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `xueshengleibie`
--

DROP TABLE IF EXISTS `xueshengleibie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xueshengleibie` (
  `name` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `number` varchar(255) DEFAULT NULL,
  `specialities` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `class` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `xueshengleibie`
--

LOCK TABLES `xueshengleibie` WRITE;
/*!40000 ALTER TABLE `xueshengleibie` DISABLE KEYS */;
INSERT INTO `xueshengleibie` VALUES ('王三','12','信息安全','15-1','12'),('李四','23','信息安全','15-2','23');
/*!40000 ALTER TABLE `xueshengleibie` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-09-20 13:40:55

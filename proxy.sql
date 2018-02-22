-- MySQL dump 10.13  Distrib 5.7.21, for macos10.13 (x86_64)
--
-- Host: localhost    Database: proxy
-- ------------------------------------------------------
-- Server version	5.7.21

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
-- Table structure for table `proxylist`
--

DROP TABLE IF EXISTS `proxylist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `proxylist` (
  `ip` varchar(30) NOT NULL,
  `type` varchar(10) DEFAULT NULL,
  `model` varchar(10) NOT NULL,
  `verifytime` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proxylist`
--

LOCK TABLES `proxylist` WRITE;
/*!40000 ALTER TABLE `proxylist` DISABLE KEYS */;
INSERT INTO `proxylist` VALUES ('110.73.54.216:8123','http','高匿','2018-02-19 16:59:14'),('110.189.222.125:808','http','高匿','2018-02-19 16:59:09'),('61.188.24.184:808','http','高匿','2018-02-19 16:59:04'),('175.155.247.204:808','http','高匿','2018-02-19 16:58:59'),('112.194.43.226:808','http','高匿','2018-02-19 16:58:54'),('119.7.75.246:808','http','高匿','2018-02-19 16:58:48'),('175.155.223.99:808','http','高匿','2018-02-19 16:58:43'),('175.155.245.199:808','http','高匿','2018-02-19 16:58:38'),('113.58.233.5:808','http','高匿','2018-02-19 16:58:33'),('113.58.232.116:808','http','高匿','2018-02-19 16:58:28'),('36.1.155.140:9797','http','高匿','2018-02-19 16:58:23'),('113.58.232.237:808','http','高匿','2018-02-19 16:58:18'),('113.58.233.40:808','http','高匿','2018-02-19 16:58:13'),('27.46.37.124:9797','http','高匿','2018-02-19 16:58:08'),('113.221.214.75:9000','http','高匿','2018-02-19 16:58:03'),('121.62.184.97:808','http','高匿','2018-02-19 16:57:58'),('119.99.19.183:808','http','高匿','2018-02-19 16:57:53'),('123.55.95.225:808','http','高匿','2018-02-19 16:57:48'),('123.55.95.114:808','http','高匿','2018-02-19 16:57:43'),('123.55.159.183:808','http','高匿','2018-02-19 16:57:38'),('175.155.153.38:808','http','高匿','2018-02-19 17:04:40'),('218.63.216.74:8998','http','高匿','2018-02-19 17:04:35'),('106.56.87.34:8998','http','高匿','2018-02-19 17:04:30'),('36.55.231.53:3128','http','高匿','2018-02-19 17:04:25'),('110.73.34.60:8123','http','高匿','2018-02-19 17:04:20');
/*!40000 ALTER TABLE `proxylist` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-02-22 21:36:21

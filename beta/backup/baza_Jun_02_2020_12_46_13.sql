-- MySQL dump 10.17  Distrib 10.3.22-MariaDB, for debian-linux-gnueabihf (armv8l)
--
-- Host: localhost    Database: proba
-- ------------------------------------------------------
-- Server version	10.3.22-MariaDB-0+deb10u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `proizvodi`
--

DROP TABLE IF EXISTS `proizvodi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `proizvodi` (
  `ID` int(6) unsigned NOT NULL AUTO_INCREMENT,
  `nazivProizvoda` varchar(30) NOT NULL,
  `precnikAmbalaze` float NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proizvodi`
--

LOCK TABLES `proizvodi` WRITE;
/*!40000 ALTER TABLE `proizvodi` DISABLE KEYS */;
INSERT INTO `proizvodi` VALUES (1,'Coca Cola 1L',9.2),(12,'Limenka',5.8);
/*!40000 ALTER TABLE `proizvodi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rasporedProizvoda`
--

DROP TABLE IF EXISTS `rasporedProizvoda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rasporedProizvoda` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `red` int(5) NOT NULL,
  `kolona` int(5) NOT NULL,
  `idProizvod` int(5) NOT NULL,
  `kolikoStajeURaf` int(4) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rasporedProizvoda`
--

LOCK TABLES `rasporedProizvoda` WRITE;
/*!40000 ALTER TABLE `rasporedProizvoda` DISABLE KEYS */;
INSERT INTO `rasporedProizvoda` VALUES (1,1,1,12,11),(2,1,2,1,7);
/*!40000 ALTER TABLE `rasporedProizvoda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test`
--

DROP TABLE IF EXISTS `test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `test` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `vreme` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `idSenzora` int(5) DEFAULT NULL,
  `idRaf` int(3) NOT NULL,
  `idRed` int(3) NOT NULL,
  `idKolona` int(3) NOT NULL,
  `idProizvod` int(5) NOT NULL,
  `trenutnoStanje` int(5) NOT NULL,
  `dodatoURaf` int(4) NOT NULL,
  `uzetoIzRafa` int(4) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test`
--

LOCK TABLES `test` WRITE;
/*!40000 ALTER TABLE `test` DISABLE KEYS */;
INSERT INTO `test` VALUES (1,'2020-06-01 14:51:09',1,1,1,1,1,0,0,0),(2,'2020-06-01 14:51:11',2,1,1,2,1,0,0,0),(3,'2020-06-01 14:51:13',3,1,1,3,1,0,0,0),(4,'2020-06-01 14:51:15',4,1,1,4,1,0,0,0),(5,'2020-06-01 14:51:17',5,1,1,5,1,0,0,0),(6,'2020-06-01 14:51:33',1,1,1,1,12,7,7,0),(7,'2020-06-01 14:51:33',2,1,1,2,1,3,3,0),(8,'2020-06-01 14:52:59',1,1,1,1,12,6,0,1),(9,'2020-06-01 14:54:04',1,1,1,1,12,5,0,1),(10,'2020-06-01 15:02:24',1,1,1,1,12,3,0,2),(11,'2020-06-01 15:07:38',2,1,1,2,1,2,0,1),(12,'2020-06-01 15:07:40',2,1,1,2,1,3,1,0),(13,'2020-06-01 18:43:22',1,1,1,1,12,4,1,0),(14,'2020-06-01 18:43:33',1,1,1,1,12,3,0,1),(15,'2020-06-01 20:05:52',2,1,1,2,1,2,0,1),(16,'2020-06-01 20:06:02',2,1,1,2,1,3,1,0),(17,'2020-06-01 23:10:39',2,1,1,2,1,2,0,1),(18,'2020-06-01 23:10:49',2,1,1,2,1,3,1,0),(19,'2020-06-02 09:49:01',1,1,1,1,12,2,0,1),(20,'2020-06-02 09:49:22',1,1,1,1,12,4,2,0),(21,'2020-06-02 09:49:44',1,1,1,1,12,6,2,0),(22,'2020-06-02 09:50:15',2,1,1,2,1,4,1,0),(23,'2020-06-02 09:52:14',2,1,1,2,1,3,0,1),(24,'2020-06-02 09:52:57',1,1,1,1,12,5,0,1),(25,'2020-06-02 09:53:40',1,1,1,1,12,4,0,1);
/*!40000 ALTER TABLE `test` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-06-02 12:46:13

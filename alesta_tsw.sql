-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: alesta_tsw
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE cp1251_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE cp1251_bin NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE cp1251_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add Парковка',7,'add_parking'),(26,'Can change Парковка',7,'change_parking'),(27,'Can delete Парковка',7,'delete_parking'),(28,'Can view Парковка',7,'view_parking'),(29,'Can add Место складирования',8,'add_place'),(30,'Can change Место складирования',8,'change_place'),(31,'Can delete Место складирования',8,'delete_place'),(32,'Can view Место складирования',8,'view_place'),(33,'Can add Заказ услуги',9,'add_serviceorder'),(34,'Can change Заказ услуги',9,'change_serviceorder'),(35,'Can delete Заказ услуги',9,'delete_serviceorder'),(36,'Can view Заказ услуги',9,'view_serviceorder'),(37,'Can add Поставщик',10,'add_supplier'),(38,'Can change Поставщик',10,'change_supplier'),(39,'Can delete Поставщик',10,'delete_supplier'),(40,'Can view Поставщик',10,'view_supplier'),(41,'Can add Транспорт',11,'add_transport'),(42,'Can change Транспорт',11,'change_transport'),(43,'Can delete Транспорт',11,'delete_transport'),(44,'Can view Транспорт',11,'view_transport'),(45,'Can add Склад временного хранения',12,'add_tsw'),(46,'Can change Склад временного хранения',12,'change_tsw'),(47,'Can delete Склад временного хранения',12,'delete_tsw'),(48,'Can view Склад временного хранения',12,'view_tsw'),(49,'Can add Тип места',13,'add_typeplace'),(50,'Can change Тип места',13,'change_typeplace'),(51,'Can delete Тип места',13,'delete_typeplace'),(52,'Can view Тип места',13,'view_typeplace'),(53,'Can add Лог действия',14,'add_actionlog'),(54,'Can change Лог действия',14,'change_actionlog'),(55,'Can delete Лог действия',14,'delete_actionlog'),(56,'Can view Лог действия',14,'view_actionlog'),(57,'Can add Журнал въезда/выезда',15,'add_logbook'),(58,'Can change Журнал въезда/выезда',15,'change_logbook'),(59,'Can delete Журнал въезда/выезда',15,'delete_logbook'),(60,'Can view Журнал въезда/выезда',15,'view_logbook'),(61,'Can add Уведомление',16,'add_notice'),(62,'Can change Уведомление',16,'change_notice'),(63,'Can delete Уведомление',16,'delete_notice'),(64,'Can view Уведомление',16,'view_notice'),(65,'Can add Документ',17,'add_doc'),(66,'Can change Документ',17,'change_doc'),(67,'Can delete Документ',17,'delete_doc'),(68,'Can view Документ',17,'view_doc'),(69,'Can add Заказ',18,'add_order'),(70,'Can change Заказ',18,'change_order'),(71,'Can delete Заказ',18,'delete_order'),(72,'Can view Заказ',18,'view_order'),(73,'Can add Парковочное место',19,'add_placepark'),(74,'Can change Парковочное место',19,'change_placepark'),(75,'Can delete Парковочное место',19,'delete_placepark'),(76,'Can view Парковочное место',19,'view_placepark'),(77,'Can add Товар',20,'add_product'),(78,'Can change Товар',20,'change_product'),(79,'Can delete Товар',20,'delete_product'),(80,'Can view Товар',20,'view_product'),(81,'Can add Лог перемещения товара',21,'add_logplace'),(82,'Can change Лог перемещения товара',21,'change_logplace'),(83,'Can delete Лог перемещения товара',21,'delete_logplace'),(84,'Can view Лог перемещения товара',21,'view_logplace'),(85,'Can add Получатель',22,'add_recipient'),(86,'Can change Получатель',22,'change_recipient'),(87,'Can delete Получатель',22,'delete_recipient'),(88,'Can view Получатель',22,'view_recipient'),(89,'Can add Передача груза',23,'add_transfer'),(90,'Can change Передача груза',23,'change_transfer'),(91,'Can delete Передача груза',23,'delete_transfer'),(92,'Can view Передача груза',23,'view_transfer'),(93,'Can add Транспорт-Уведомление',24,'add_transportnotice'),(94,'Can change Транспорт-Уведомление',24,'change_transportnotice'),(95,'Can delete Транспорт-Уведомление',24,'delete_transportnotice'),(96,'Can view Транспорт-Уведомление',24,'view_transportnotice'),(97,'Can add Склад',25,'add_warehouse'),(98,'Can change Склад',25,'change_warehouse'),(99,'Can delete Склад',25,'delete_warehouse'),(100,'Can view Склад',25,'view_warehouse'),(101,'Can add Рампа',26,'add_ramp'),(102,'Can change Рампа',26,'change_ramp'),(103,'Can delete Рампа',26,'delete_ramp'),(104,'Can view Рампа',26,'view_ramp');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE cp1251_bin NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE cp1251_bin NOT NULL,
  `first_name` varchar(150) COLLATE cp1251_bin NOT NULL,
  `last_name` varchar(150) COLLATE cp1251_bin NOT NULL,
  `email` varchar(254) COLLATE cp1251_bin NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$870000$ADoNNifSK9oQZ3aCqymHba$esgFFuWgM8IDn5YMhD/v1xkTEZtHCqLXizuCF3tXHdk=','2024-12-16 12:03:58.798106',1,'admin','','','',1,1,'2024-12-16 12:00:50.249031');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_actionlog`
--

DROP TABLE IF EXISTS `core_actionlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_actionlog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `object_id` int unsigned NOT NULL,
  `action` varchar(100) COLLATE cp1251_bin NOT NULL,
  `before_state` json DEFAULT NULL,
  `after_state` json DEFAULT NULL,
  `datetime` datetime(6) NOT NULL,
  `content_type_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_actionlog_content_type_id_a5ee1884_fk_django_co` (`content_type_id`),
  KEY `core_actionlog_user_id_686d25e2_fk_auth_user_id` (`user_id`),
  CONSTRAINT `core_actionlog_content_type_id_a5ee1884_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `core_actionlog_user_id_686d25e2_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `core_actionlog_chk_1` CHECK ((`object_id` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_actionlog`
--

LOCK TABLES `core_actionlog` WRITE;
/*!40000 ALTER TABLE `core_actionlog` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_actionlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_doc`
--

DROP TABLE IF EXISTS `core_doc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_doc` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `doc_code` varchar(5) COLLATE cp1251_bin NOT NULL,
  `doc_number` varchar(30) COLLATE cp1251_bin NOT NULL,
  `doc_date` date NOT NULL,
  `notice_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_doc_notice_id_075e3404_fk_core_notice_id` (`notice_id`),
  CONSTRAINT `core_doc_notice_id_075e3404_fk_core_notice_id` FOREIGN KEY (`notice_id`) REFERENCES `core_notice` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_doc`
--

LOCK TABLES `core_doc` WRITE;
/*!40000 ALTER TABLE `core_doc` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_doc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_logbook`
--

DROP TABLE IF EXISTS `core_logbook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_logbook` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(10) COLLATE cp1251_bin DEFAULT NULL,
  `carrier_info` varchar(100) COLLATE cp1251_bin NOT NULL,
  `phone` varchar(100) COLLATE cp1251_bin NOT NULL,
  `vehicle_number` varchar(100) COLLATE cp1251_bin NOT NULL,
  `trailer_number` varchar(100) COLLATE cp1251_bin NOT NULL,
  `seal` tinyint(1) NOT NULL,
  `seal_quantity` varchar(100) COLLATE cp1251_bin DEFAULT NULL,
  `seal_number` varchar(100) COLLATE cp1251_bin DEFAULT NULL,
  `removed_control` varchar(10) COLLATE cp1251_bin NOT NULL,
  `datetime_in` datetime(6) NOT NULL,
  `datetime_out` datetime(6) DEFAULT NULL,
  `note_in` longtext COLLATE cp1251_bin,
  `note_out` longtext COLLATE cp1251_bin,
  `note` longtext COLLATE cp1251_bin,
  `user_in_id` int NOT NULL,
  `user_out_id` int DEFAULT NULL,
  `place_park_id` bigint NOT NULL,
  `warehouse_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_logbook_place_park_id_e15d4193_fk_core_placepark_id` (`place_park_id`),
  KEY `core_logbook_user_in_id_784599b9_fk_auth_user_id` (`user_in_id`),
  KEY `core_logbook_user_out_id_e3dbbf8b_fk_auth_user_id` (`user_out_id`),
  KEY `core_logbook_warehouse_id_bd37a3b7_fk_core_warehouse_id` (`warehouse_id`),
  CONSTRAINT `core_logbook_place_park_id_e15d4193_fk_core_placepark_id` FOREIGN KEY (`place_park_id`) REFERENCES `core_placepark` (`id`),
  CONSTRAINT `core_logbook_user_in_id_784599b9_fk_auth_user_id` FOREIGN KEY (`user_in_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `core_logbook_user_out_id_e3dbbf8b_fk_auth_user_id` FOREIGN KEY (`user_out_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `core_logbook_warehouse_id_bd37a3b7_fk_core_warehouse_id` FOREIGN KEY (`warehouse_id`) REFERENCES `core_warehouse` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_logbook`
--

LOCK TABLES `core_logbook` WRITE;
/*!40000 ALTER TABLE `core_logbook` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_logbook` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_logplace`
--

DROP TABLE IF EXISTS `core_logplace`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_logplace` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int unsigned NOT NULL,
  `datetime` datetime(6) NOT NULL,
  `note` longtext COLLATE cp1251_bin,
  `user_id` int NOT NULL,
  `place_from_id` bigint DEFAULT NULL,
  `place_to_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_logplace_user_id_641ede25_fk_auth_user_id` (`user_id`),
  KEY `core_logplace_place_from_id_945fdc94_fk_core_place_id` (`place_from_id`),
  KEY `core_logplace_place_to_id_ea8a08f1_fk_core_place_id` (`place_to_id`),
  KEY `core_logplace_product_id_070032ce_fk_core_product_id` (`product_id`),
  CONSTRAINT `core_logplace_place_from_id_945fdc94_fk_core_place_id` FOREIGN KEY (`place_from_id`) REFERENCES `core_place` (`id`),
  CONSTRAINT `core_logplace_place_to_id_ea8a08f1_fk_core_place_id` FOREIGN KEY (`place_to_id`) REFERENCES `core_place` (`id`),
  CONSTRAINT `core_logplace_product_id_070032ce_fk_core_product_id` FOREIGN KEY (`product_id`) REFERENCES `core_product` (`id`),
  CONSTRAINT `core_logplace_user_id_641ede25_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `core_logplace_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_logplace`
--

LOCK TABLES `core_logplace` WRITE;
/*!40000 ALTER TABLE `core_logplace` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_logplace` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_notice`
--

DROP TABLE IF EXISTS `core_notice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_notice` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `doc_creation_date` datetime(6) NOT NULL,
  `date_in` date NOT NULL,
  `time_in` time(6) NOT NULL,
  `gross_weight` double NOT NULL,
  `goods_presence` tinyint(1) NOT NULL,
  `purpose_placement` varchar(2) COLLATE cp1251_bin NOT NULL,
  `guid` varchar(36) COLLATE cp1251_bin NOT NULL,
  `number_out` varchar(15) COLLATE cp1251_bin DEFAULT NULL,
  `notification` varchar(25) COLLATE cp1251_bin DEFAULT NULL,
  `number_notification` varchar(50) COLLATE cp1251_bin DEFAULT NULL,
  `zhurnal` varchar(12) COLLATE cp1251_bin DEFAULT NULL,
  `stz` varchar(1) COLLATE cp1251_bin DEFAULT NULL,
  `year` varchar(12) COLLATE cp1251_bin DEFAULT NULL,
  `fio` varchar(100) COLLATE cp1251_bin DEFAULT NULL,
  `user_id` int NOT NULL,
  `order_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `guid` (`guid`),
  KEY `core_notice_order_id_61fb9c4b_fk_core_order_id` (`order_id`),
  KEY `core_notice_user_id_2b488d98_fk_auth_user_id` (`user_id`),
  CONSTRAINT `core_notice_order_id_61fb9c4b_fk_core_order_id` FOREIGN KEY (`order_id`) REFERENCES `core_order` (`id`),
  CONSTRAINT `core_notice_user_id_2b488d98_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_notice`
--

LOCK TABLES `core_notice` WRITE;
/*!40000 ALTER TABLE `core_notice` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_notice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_order`
--

DROP TABLE IF EXISTS `core_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `transport_type` varchar(1) COLLATE cp1251_bin NOT NULL,
  `carrier_name` varchar(100) COLLATE cp1251_bin NOT NULL,
  `phone` varchar(20) COLLATE cp1251_bin NOT NULL,
  `vehicle_number` varchar(20) COLLATE cp1251_bin NOT NULL,
  `customer` varchar(100) COLLATE cp1251_bin DEFAULT NULL,
  `status_order` varchar(2) COLLATE cp1251_bin NOT NULL,
  `datetime` datetime(6) NOT NULL,
  `quantity` int unsigned NOT NULL,
  `damage` varchar(10) COLLATE cp1251_bin NOT NULL,
  `damage_description` longtext COLLATE cp1251_bin,
  `note` longtext COLLATE cp1251_bin,
  `logbook_id` bigint DEFAULT NULL,
  `user_id` int NOT NULL,
  `supplier_id` bigint NOT NULL,
  `warehouse_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_order_warehouse_id_5d76be52_fk_core_warehouse_id` (`warehouse_id`),
  KEY `core_order_logbook_id_1895ff4d_fk_core_logbook_id` (`logbook_id`),
  KEY `core_order_user_id_b03bbffd_fk_auth_user_id` (`user_id`),
  KEY `core_order_supplier_id_96b3bf14_fk_core_supplier_id` (`supplier_id`),
  CONSTRAINT `core_order_logbook_id_1895ff4d_fk_core_logbook_id` FOREIGN KEY (`logbook_id`) REFERENCES `core_logbook` (`id`),
  CONSTRAINT `core_order_supplier_id_96b3bf14_fk_core_supplier_id` FOREIGN KEY (`supplier_id`) REFERENCES `core_supplier` (`id`),
  CONSTRAINT `core_order_user_id_b03bbffd_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `core_order_warehouse_id_5d76be52_fk_core_warehouse_id` FOREIGN KEY (`warehouse_id`) REFERENCES `core_warehouse` (`id`),
  CONSTRAINT `core_order_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_order`
--

LOCK TABLES `core_order` WRITE;
/*!40000 ALTER TABLE `core_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_parking`
--

DROP TABLE IF EXISTS `core_parking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_parking` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `description` longtext COLLATE cp1251_bin,
  `note` longtext COLLATE cp1251_bin,
  `warehouse_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_parking_warehouse_id_e93d2926_fk_core_warehouse_id` (`warehouse_id`),
  CONSTRAINT `core_parking_warehouse_id_e93d2926_fk_core_warehouse_id` FOREIGN KEY (`warehouse_id`) REFERENCES `core_warehouse` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_parking`
--

LOCK TABLES `core_parking` WRITE;
/*!40000 ALTER TABLE `core_parking` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_parking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_place`
--

DROP TABLE IF EXISTS `core_place`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_place` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status_place` varchar(50) COLLATE cp1251_bin NOT NULL,
  `type` varchar(100) COLLATE cp1251_bin NOT NULL,
  `characteristic` varchar(100) COLLATE cp1251_bin NOT NULL,
  `description` longtext COLLATE cp1251_bin,
  `note` longtext COLLATE cp1251_bin,
  `type_place_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_place_type_place_id_3e4e1103_fk_core_typeplace_id` (`type_place_id`),
  CONSTRAINT `core_place_type_place_id_3e4e1103_fk_core_typeplace_id` FOREIGN KEY (`type_place_id`) REFERENCES `core_typeplace` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_place`
--

LOCK TABLES `core_place` WRITE;
/*!40000 ALTER TABLE `core_place` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_place` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_placepark`
--

DROP TABLE IF EXISTS `core_placepark`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_placepark` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `spot_number` varchar(50) COLLATE cp1251_bin NOT NULL,
  `size` varchar(50) COLLATE cp1251_bin DEFAULT NULL,
  `is_available` tinyint(1) NOT NULL,
  `parking_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_placepark_parking_id_cb6f3df3_fk_core_parking_id` (`parking_id`),
  CONSTRAINT `core_placepark_parking_id_cb6f3df3_fk_core_parking_id` FOREIGN KEY (`parking_id`) REFERENCES `core_parking` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_placepark`
--

LOCK TABLES `core_placepark` WRITE;
/*!40000 ALTER TABLE `core_placepark` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_placepark` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_product`
--

DROP TABLE IF EXISTS `core_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_product` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sku` varchar(100) COLLATE cp1251_bin NOT NULL,
  `type_product` varchar(100) COLLATE cp1251_bin NOT NULL,
  `description` longtext COLLATE cp1251_bin,
  `net_weight` decimal(10,2) NOT NULL,
  `gross_weight` decimal(10,2) NOT NULL,
  `quantity` int NOT NULL,
  `barcode` varchar(100) COLLATE cp1251_bin NOT NULL,
  `quantity_pack` int NOT NULL,
  `datetime_in` datetime(6) NOT NULL,
  `datetime_out` datetime(6) DEFAULT NULL,
  `size` varchar(100) COLLATE cp1251_bin DEFAULT NULL,
  `note` longtext COLLATE cp1251_bin,
  `place_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_product_place_id_8ec44d35_fk_core_place_id` (`place_id`),
  CONSTRAINT `core_product_place_id_8ec44d35_fk_core_place_id` FOREIGN KEY (`place_id`) REFERENCES `core_place` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_product`
--

LOCK TABLES `core_product` WRITE;
/*!40000 ALTER TABLE `core_product` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_ramp`
--

DROP TABLE IF EXISTS `core_ramp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_ramp` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `description` varchar(100) COLLATE cp1251_bin NOT NULL,
  `note` longtext COLLATE cp1251_bin,
  `status_ramp` varchar(20) COLLATE cp1251_bin NOT NULL,
  `warehouse_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_ramp_warehouse_id_54dd7f69_fk_core_warehouse_id` (`warehouse_id`),
  CONSTRAINT `core_ramp_warehouse_id_54dd7f69_fk_core_warehouse_id` FOREIGN KEY (`warehouse_id`) REFERENCES `core_warehouse` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_ramp`
--

LOCK TABLES `core_ramp` WRITE;
/*!40000 ALTER TABLE `core_ramp` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_ramp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_recipient`
--

DROP TABLE IF EXISTS `core_recipient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_recipient` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE cp1251_bin NOT NULL,
  `country` varchar(2) COLLATE cp1251_bin NOT NULL,
  `notice_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_recipient_notice_id_e12bf012_fk_core_notice_id` (`notice_id`),
  CONSTRAINT `core_recipient_notice_id_e12bf012_fk_core_notice_id` FOREIGN KEY (`notice_id`) REFERENCES `core_notice` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_recipient`
--

LOCK TABLES `core_recipient` WRITE;
/*!40000 ALTER TABLE `core_recipient` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_recipient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_serviceorder`
--

DROP TABLE IF EXISTS `core_serviceorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_serviceorder` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `price` decimal(10,2) NOT NULL,
  `price_nds` decimal(10,2) NOT NULL,
  `price_invoice` decimal(10,2) NOT NULL,
  `description_service` longtext COLLATE cp1251_bin NOT NULL,
  `note` longtext COLLATE cp1251_bin,
  `currency` varchar(3) COLLATE cp1251_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_serviceorder`
--

LOCK TABLES `core_serviceorder` WRITE;
/*!40000 ALTER TABLE `core_serviceorder` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_serviceorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_supplier`
--

DROP TABLE IF EXISTS `core_supplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_supplier` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE cp1251_bin NOT NULL,
  `address` longtext COLLATE cp1251_bin,
  `postal_code` varchar(20) COLLATE cp1251_bin NOT NULL,
  `phone` varchar(20) COLLATE cp1251_bin NOT NULL,
  `city` varchar(100) COLLATE cp1251_bin NOT NULL,
  `tax_number` varchar(20) COLLATE cp1251_bin NOT NULL,
  `note` longtext COLLATE cp1251_bin,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_supplier`
--

LOCK TABLES `core_supplier` WRITE;
/*!40000 ALTER TABLE `core_supplier` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_supplier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_transfer`
--

DROP TABLE IF EXISTS `core_transfer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_transfer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `price` decimal(10,2) NOT NULL,
  `quantity` int unsigned NOT NULL,
  `note` longtext COLLATE cp1251_bin,
  `type_transfer` varchar(100) COLLATE cp1251_bin NOT NULL,
  `is_fully_transferred` tinyint(1) NOT NULL,
  `order_in_id` bigint NOT NULL,
  `order_out_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_transfer_order_in_id_267af0ca_fk_core_order_id` (`order_in_id`),
  KEY `core_transfer_order_out_id_b875cf64_fk_core_order_id` (`order_out_id`),
  KEY `core_transfer_product_id_58ee4513_fk_core_product_id` (`product_id`),
  KEY `core_transfer_user_id_b03294c2_fk_auth_user_id` (`user_id`),
  CONSTRAINT `core_transfer_order_in_id_267af0ca_fk_core_order_id` FOREIGN KEY (`order_in_id`) REFERENCES `core_order` (`id`),
  CONSTRAINT `core_transfer_order_out_id_b875cf64_fk_core_order_id` FOREIGN KEY (`order_out_id`) REFERENCES `core_order` (`id`),
  CONSTRAINT `core_transfer_product_id_58ee4513_fk_core_product_id` FOREIGN KEY (`product_id`) REFERENCES `core_product` (`id`),
  CONSTRAINT `core_transfer_user_id_b03294c2_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `core_transfer_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_transfer`
--

LOCK TABLES `core_transfer` WRITE;
/*!40000 ALTER TABLE `core_transfer` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_transfer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_transport`
--

DROP TABLE IF EXISTS `core_transport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_transport` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ts` varchar(20) COLLATE cp1251_bin NOT NULL,
  `type_ts` varchar(3) COLLATE cp1251_bin NOT NULL,
  `country` varchar(2) COLLATE cp1251_bin NOT NULL,
  `carrier_name` varchar(100) COLLATE cp1251_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ts` (`ts`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_transport`
--

LOCK TABLES `core_transport` WRITE;
/*!40000 ALTER TABLE `core_transport` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_transport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_transportnotice`
--

DROP TABLE IF EXISTS `core_transportnotice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_transportnotice` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `number` varchar(100) COLLATE cp1251_bin NOT NULL,
  `type` varchar(100) COLLATE cp1251_bin NOT NULL,
  `country` varchar(2) COLLATE cp1251_bin NOT NULL,
  `notice_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_transportnotice_notice_id_9859b56c_fk_core_notice_id` (`notice_id`),
  CONSTRAINT `core_transportnotice_notice_id_9859b56c_fk_core_notice_id` FOREIGN KEY (`notice_id`) REFERENCES `core_notice` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_transportnotice`
--

LOCK TABLES `core_transportnotice` WRITE;
/*!40000 ALTER TABLE `core_transportnotice` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_transportnotice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_tsw`
--

DROP TABLE IF EXISTS `core_tsw`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_tsw` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE cp1251_bin NOT NULL,
  `base_notification_number` varchar(50) COLLATE cp1251_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `base_notification_number` (`base_notification_number`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_tsw`
--

LOCK TABLES `core_tsw` WRITE;
/*!40000 ALTER TABLE `core_tsw` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_tsw` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_typeplace`
--

DROP TABLE IF EXISTS `core_typeplace`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_typeplace` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `description` longtext COLLATE cp1251_bin NOT NULL,
  `max_weight` decimal(10,2) NOT NULL,
  `max_size` varchar(100) COLLATE cp1251_bin NOT NULL,
  `type_product` varchar(100) COLLATE cp1251_bin NOT NULL,
  `type_place` varchar(100) COLLATE cp1251_bin NOT NULL,
  `note` longtext COLLATE cp1251_bin,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_typeplace`
--

LOCK TABLES `core_typeplace` WRITE;
/*!40000 ALTER TABLE `core_typeplace` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_typeplace` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_warehouse`
--

DROP TABLE IF EXISTS `core_warehouse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_warehouse` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE cp1251_bin NOT NULL,
  `svh_number` varchar(50) COLLATE cp1251_bin DEFAULT NULL,
  `address` varchar(100) COLLATE cp1251_bin NOT NULL,
  `note` longtext COLLATE cp1251_bin,
  `customs_post` varchar(100) COLLATE cp1251_bin DEFAULT NULL,
  `name_post` varchar(100) COLLATE cp1251_bin DEFAULT NULL,
  `TSW_id` bigint NOT NULL,
  `place_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_warehouse_TSW_id_aefcb428_fk_core_tsw_id` (`TSW_id`),
  KEY `core_warehouse_place_id_1d3172e6_fk_core_place_id` (`place_id`),
  CONSTRAINT `core_warehouse_place_id_1d3172e6_fk_core_place_id` FOREIGN KEY (`place_id`) REFERENCES `core_place` (`id`),
  CONSTRAINT `core_warehouse_TSW_id_aefcb428_fk_core_tsw_id` FOREIGN KEY (`TSW_id`) REFERENCES `core_tsw` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_warehouse`
--

LOCK TABLES `core_warehouse` WRITE;
/*!40000 ALTER TABLE `core_warehouse` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_warehouse` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE cp1251_bin,
  `object_repr` varchar(200) COLLATE cp1251_bin NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE cp1251_bin NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE cp1251_bin NOT NULL,
  `model` varchar(100) COLLATE cp1251_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(14,'core','actionlog'),(17,'core','doc'),(15,'core','logbook'),(21,'core','logplace'),(16,'core','notice'),(18,'core','order'),(7,'core','parking'),(8,'core','place'),(19,'core','placepark'),(20,'core','product'),(26,'core','ramp'),(22,'core','recipient'),(9,'core','serviceorder'),(10,'core','supplier'),(23,'core','transfer'),(11,'core','transport'),(24,'core','transportnotice'),(12,'core','tsw'),(13,'core','typeplace'),(25,'core','warehouse'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE cp1251_bin NOT NULL,
  `name` varchar(255) COLLATE cp1251_bin NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-12-16 12:00:28.136343'),(2,'auth','0001_initial','2024-12-16 12:00:28.711805'),(3,'admin','0001_initial','2024-12-16 12:00:28.819543'),(4,'admin','0002_logentry_remove_auto_add','2024-12-16 12:00:28.827529'),(5,'admin','0003_logentry_add_action_flag_choices','2024-12-16 12:00:28.834509'),(6,'contenttypes','0002_remove_content_type_name','2024-12-16 12:00:28.903291'),(7,'auth','0002_alter_permission_name_max_length','2024-12-16 12:00:28.920245'),(8,'auth','0003_alter_user_email_max_length','2024-12-16 12:00:28.943232'),(9,'auth','0004_alter_user_username_opts','2024-12-16 12:00:28.950165'),(10,'auth','0005_alter_user_last_login_null','2024-12-16 12:00:29.002026'),(11,'auth','0006_require_contenttypes_0002','2024-12-16 12:00:29.005020'),(12,'auth','0007_alter_validators_add_error_messages','2024-12-16 12:00:29.012037'),(13,'auth','0008_alter_user_username_max_length','2024-12-16 12:00:29.033941'),(14,'auth','0009_alter_user_last_name_max_length','2024-12-16 12:00:29.053887'),(15,'auth','0010_alter_group_name_max_length','2024-12-16 12:00:29.073837'),(16,'auth','0011_update_proxy_permissions','2024-12-16 12:00:29.083842'),(17,'auth','0012_alter_user_first_name_max_length','2024-12-16 12:00:29.104788'),(18,'core','0001_initial','2024-12-16 12:00:30.995692'),(19,'sessions','0001_initial','2024-12-16 12:00:31.027609'),(20,'core','0002_alter_logbook_warehouse','2024-12-16 12:25:18.698332');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE cp1251_bin NOT NULL,
  `session_data` longtext COLLATE cp1251_bin NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('qopx70s8xknihsw1h3vhunvcdv1ktbr7','.eJxVjMsOwiAQRf-FtSEyPAZcuu83kAEGqZo2Ke3K-O_apAvd3nPOfYlI29ri1nmJYxEXocTpd0uUHzztoNxpus0yz9O6jEnuijxol8Nc-Hk93L-DRr19a-3B2YqoKuecEdGAUeBtSGCqA8MGyzlYIs3OI3tQlSiwhqS9qamI9wfFPTeJ:1tN9pO:FQXj4GGoVfqbBzZE0VxsTJB_cwp6AZNiApUxQfdPETc','2024-12-30 12:03:58.801101');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-18 10:05:00

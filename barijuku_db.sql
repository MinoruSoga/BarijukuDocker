-- -------------------------------------------------------------
-- TablePlus 5.6.0(514)
--
-- https://tableplus.com/
--
-- Database: barijuku_db
-- Generation Time: 2023-11-03 04:00:38.2930
-- -------------------------------------------------------------


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


DROP TABLE IF EXISTS `app_calendar`;
CREATE TABLE `app_calendar` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `is_student` int NOT NULL,
  `content` varchar(50) DEFAULT NULL,
  `place_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_calendar_place_id_4fdaee34_fk_app_place_id` (`place_id`),
  KEY `app_calendar_user_id_f03e0d06_fk_user_customuser_id` (`user_id`),
  CONSTRAINT `app_calendar_place_id_4fdaee34_fk_app_place_id` FOREIGN KEY (`place_id`) REFERENCES `app_place` (`id`),
  CONSTRAINT `app_calendar_user_id_f03e0d06_fk_user_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `user_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `app_chatgptlog`;
CREATE TABLE `app_chatgptlog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `request_content` longtext,
  `response_content` longtext,
  `created_at` datetime(6) NOT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_chatgptlog_student_id_096bf7a1_fk_student_student_id` (`student_id`),
  CONSTRAINT `app_chatgptlog_student_id_096bf7a1_fk_student_student_id` FOREIGN KEY (`student_id`) REFERENCES `student_student` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `app_city`;
CREATE TABLE `app_city` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `city` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `prefecture_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_city_prefecture_id_3b6e05c0_fk_app_prefecture_id` (`prefecture_id`),
  CONSTRAINT `app_city_prefecture_id_3b6e05c0_fk_app_prefecture_id` FOREIGN KEY (`prefecture_id`) REFERENCES `app_prefecture` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=385070 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `app_coupon`;
CREATE TABLE `app_coupon` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `price` int NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `app_couponstudent`;
CREATE TABLE `app_couponstudent` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(20) NOT NULL,
  `is_used` tinyint(1) NOT NULL,
  `expiration_date` date DEFAULT NULL,
  `used_date` datetime(6) DEFAULT NULL,
  `coupon_id` bigint NOT NULL,
  `shop_id` bigint DEFAULT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `app_couponstudent_coupon_id_68139827_fk_app_coupon_id` (`coupon_id`),
  KEY `app_couponstudent_shop_id_f0729f96_fk_shop_shop_id` (`shop_id`),
  KEY `app_couponstudent_student_id_f3bcac11_fk_student_student_id` (`student_id`),
  CONSTRAINT `app_couponstudent_coupon_id_68139827_fk_app_coupon_id` FOREIGN KEY (`coupon_id`) REFERENCES `app_coupon` (`id`),
  CONSTRAINT `app_couponstudent_shop_id_f0729f96_fk_shop_shop_id` FOREIGN KEY (`shop_id`) REFERENCES `shop_shop` (`id`),
  CONSTRAINT `app_couponstudent_student_id_f3bcac11_fk_student_student_id` FOREIGN KEY (`student_id`) REFERENCES `student_student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `app_meeting`;
CREATE TABLE `app_meeting` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content` varchar(50) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `meeting_schedule_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_meeting_meeting_schedule_id_1ad5a20e_fk_app_meeti` (`meeting_schedule_id`),
  CONSTRAINT `app_meeting_meeting_schedule_id_1ad5a20e_fk_app_meeti` FOREIGN KEY (`meeting_schedule_id`) REFERENCES `app_meetingschedule` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `app_meetingschedule`;
CREATE TABLE `app_meetingschedule` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `content` varchar(50) DEFAULT NULL,
  `place_id` bigint NOT NULL,
  `student_id` bigint NOT NULL,
  `trainer_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_meetingschedule_place_id_027aa99b_fk_app_place_id` (`place_id`),
  KEY `app_meetingschedule_student_id_95d8026f_fk_student_student_id` (`student_id`),
  KEY `app_meetingschedule_trainer_id_dc2f9d8b_fk_trainer_trainer_id` (`trainer_id`),
  CONSTRAINT `app_meetingschedule_place_id_027aa99b_fk_app_place_id` FOREIGN KEY (`place_id`) REFERENCES `app_place` (`id`),
  CONSTRAINT `app_meetingschedule_student_id_95d8026f_fk_student_student_id` FOREIGN KEY (`student_id`) REFERENCES `student_student` (`id`),
  CONSTRAINT `app_meetingschedule_trainer_id_dc2f9d8b_fk_trainer_trainer_id` FOREIGN KEY (`trainer_id`) REFERENCES `trainer_trainer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `app_place`;
CREATE TABLE `app_place` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `place_name` varchar(50) DEFAULT NULL,
  `postal_code` varchar(50) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `entry_date` date DEFAULT NULL,
  `city_id` bigint DEFAULT NULL,
  `prefecture_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `app_place_city_id_603007f7_fk_app_city_id` (`city_id`),
  KEY `app_place_prefecture_id_79465316_fk_app_prefecture_id` (`prefecture_id`),
  CONSTRAINT `app_place_city_id_603007f7_fk_app_city_id` FOREIGN KEY (`city_id`) REFERENCES `app_city` (`id`),
  CONSTRAINT `app_place_prefecture_id_79465316_fk_app_prefecture_id` FOREIGN KEY (`prefecture_id`) REFERENCES `app_prefecture` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `app_prefecture`;
CREATE TABLE `app_prefecture` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `prefecture` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_user_customuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_user_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `user_customuser` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `shop_shop`;
CREATE TABLE `shop_shop` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `shop_name` varchar(100) NOT NULL,
  `email` varchar(50) DEFAULT NULL,
  `bank_name` varchar(100) NOT NULL,
  `branch_name` varchar(100) NOT NULL,
  `account_number` varchar(20) NOT NULL,
  `account_holder_name` varchar(100) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `shop_shop_user_id_2ca99439_fk_user_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `user_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `student_atamaplus`;
CREATE TABLE `student_atamaplus` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `login_id` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `site_url` varchar(100) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `student_atamaplus_user_id_d0ae6d63_fk_user_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `user_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `student_averagetestresult`;
CREATE TABLE `student_averagetestresult` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `score` varchar(50) NOT NULL,
  `subject_id` bigint DEFAULT NULL,
  `test_category_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `student_averagetestr_subject_id_01721193_fk_student_s` (`subject_id`),
  KEY `student_averagetestr_test_category_id_44f40e1d_fk_student_t` (`test_category_id`),
  CONSTRAINT `student_averagetestr_subject_id_01721193_fk_student_s` FOREIGN KEY (`subject_id`) REFERENCES `student_subject` (`id`),
  CONSTRAINT `student_averagetestr_test_category_id_44f40e1d_fk_student_t` FOREIGN KEY (`test_category_id`) REFERENCES `student_testcategory` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `student_clubactivity`;
CREATE TABLE `student_clubactivity` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `club_activity` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `student_school`;
CREATE TABLE `student_school` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `school` varchar(50) NOT NULL,
  `school_category_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_school_school_category_id_500bb9e1_fk_student_s` (`school_category_id`),
  CONSTRAINT `student_school_school_category_id_500bb9e1_fk_student_s` FOREIGN KEY (`school_category_id`) REFERENCES `student_schoolcategory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `student_schoolcategory`;
CREATE TABLE `student_schoolcategory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `school_category` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `student_student`;
CREATE TABLE `student_student` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `last_name` varchar(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name_kana` varchar(50) NOT NULL,
  `first_name_kana` varchar(50) NOT NULL,
  `grade` varchar(50) DEFAULT NULL,
  `school_class` varchar(50) DEFAULT NULL,
  `phone_number` varchar(50) DEFAULT NULL,
  `parent_last_name` varchar(50) DEFAULT NULL,
  `parent_first_name` varchar(50) DEFAULT NULL,
  `parent_last_name_kana` varchar(50) DEFAULT NULL,
  `parent_first_name_kana` varchar(50) DEFAULT NULL,
  `parent_phone_number` varchar(50) DEFAULT NULL,
  `parent_email` varchar(50) DEFAULT NULL,
  `zipcode` varchar(50) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `entry_date` date DEFAULT NULL,
  `expiration_date` date DEFAULT NULL,
  `stripe_data` varchar(250) DEFAULT NULL,
  `introducer_last_name` varchar(50) DEFAULT NULL,
  `introducer_first_name` varchar(50) DEFAULT NULL,
  `unsubscribe_request` tinyint(1) NOT NULL,
  `city_id` bigint DEFAULT NULL,
  `club_activity_id` bigint DEFAULT NULL,
  `prefecture_id` bigint DEFAULT NULL,
  `school_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `student_student_city_id_e115c973_fk_app_city_id` (`city_id`),
  KEY `student_student_club_activity_id_dfcedeac_fk_student_c` (`club_activity_id`),
  KEY `student_student_prefecture_id_aefd9b4a_fk_app_prefecture_id` (`prefecture_id`),
  KEY `student_student_school_id_a4d5476a_fk_student_school_id` (`school_id`),
  CONSTRAINT `student_student_city_id_e115c973_fk_app_city_id` FOREIGN KEY (`city_id`) REFERENCES `app_city` (`id`),
  CONSTRAINT `student_student_club_activity_id_dfcedeac_fk_student_c` FOREIGN KEY (`club_activity_id`) REFERENCES `student_clubactivity` (`id`),
  CONSTRAINT `student_student_prefecture_id_aefd9b4a_fk_app_prefecture_id` FOREIGN KEY (`prefecture_id`) REFERENCES `app_prefecture` (`id`),
  CONSTRAINT `student_student_school_id_a4d5476a_fk_student_school_id` FOREIGN KEY (`school_id`) REFERENCES `student_school` (`id`),
  CONSTRAINT `student_student_user_id_4f4b35ef_fk_user_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `user_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `student_studenttarget`;
CREATE TABLE `student_studenttarget` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content` varchar(100) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_studenttarget_student_id_410d471c_fk_student_student_id` (`student_id`),
  CONSTRAINT `student_studenttarget_student_id_410d471c_fk_student_student_id` FOREIGN KEY (`student_id`) REFERENCES `student_student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `student_studysapuri`;
CREATE TABLE `student_studysapuri` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `login_id` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `site_url` varchar(100) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `student_studysapuri_user_id_28c05ac6_fk_user_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `user_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `student_subject`;
CREATE TABLE `student_subject` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `subject` varchar(50) NOT NULL,
  `grade` varchar(50) DEFAULT NULL,
  `school_category_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `student_subject_school_category_id_7f045e1d_fk_student_s` (`school_category_id`),
  CONSTRAINT `student_subject_school_category_id_7f045e1d_fk_student_s` FOREIGN KEY (`school_category_id`) REFERENCES `student_schoolcategory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `student_testcategory`;
CREATE TABLE `student_testcategory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `test_category` varchar(50) NOT NULL,
  `grade` varchar(50) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `school_id` bigint DEFAULT NULL,
  `school_category_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `student_testcategory_school_id_e067722d_fk_student_school_id` (`school_id`),
  KEY `student_testcategory_school_category_id_68e4e654_fk_student_s` (`school_category_id`),
  CONSTRAINT `student_testcategory_school_category_id_68e4e654_fk_student_s` FOREIGN KEY (`school_category_id`) REFERENCES `student_schoolcategory` (`id`),
  CONSTRAINT `student_testcategory_school_id_e067722d_fk_student_school_id` FOREIGN KEY (`school_id`) REFERENCES `student_school` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `student_testresult`;
CREATE TABLE `student_testresult` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `score` varchar(50) NOT NULL,
  `date` date DEFAULT NULL,
  `school_id` bigint DEFAULT NULL,
  `student_id` bigint NOT NULL,
  `subject_id` bigint NOT NULL,
  `test_category_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_testresult_school_id_c70da904_fk_student_school_id` (`school_id`),
  KEY `student_testresult_student_id_d91e7a66_fk_student_student_id` (`student_id`),
  KEY `student_testresult_subject_id_3d7a923a_fk_student_subject_id` (`subject_id`),
  KEY `student_testresult_test_category_id_51565ba1_fk_student_t` (`test_category_id`),
  CONSTRAINT `student_testresult_school_id_c70da904_fk_student_school_id` FOREIGN KEY (`school_id`) REFERENCES `student_school` (`id`),
  CONSTRAINT `student_testresult_student_id_d91e7a66_fk_student_student_id` FOREIGN KEY (`student_id`) REFERENCES `student_student` (`id`),
  CONSTRAINT `student_testresult_subject_id_3d7a923a_fk_student_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `student_subject` (`id`),
  CONSTRAINT `student_testresult_test_category_id_51565ba1_fk_student_t` FOREIGN KEY (`test_category_id`) REFERENCES `student_testcategory` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `trainer_trainer`;
CREATE TABLE `trainer_trainer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `last_name` varchar(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name_kana` varchar(50) NOT NULL,
  `first_name_kana` varchar(50) NOT NULL,
  `phone_number` decimal(12,0) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `zipcode` varchar(50) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `entry_date` date DEFAULT NULL,
  `city_id` bigint DEFAULT NULL,
  `prefecture_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `trainer_trainer_city_id_d1777fcd_fk_app_city_id` (`city_id`),
  KEY `trainer_trainer_prefecture_id_e1181036_fk_app_prefecture_id` (`prefecture_id`),
  CONSTRAINT `trainer_trainer_city_id_d1777fcd_fk_app_city_id` FOREIGN KEY (`city_id`) REFERENCES `app_city` (`id`),
  CONSTRAINT `trainer_trainer_prefecture_id_e1181036_fk_app_prefecture_id` FOREIGN KEY (`prefecture_id`) REFERENCES `app_prefecture` (`id`),
  CONSTRAINT `trainer_trainer_user_id_2aa08d32_fk_user_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `user_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `user_customuser`;
CREATE TABLE `user_customuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `user_type` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `user_customuser_groups`;
CREATE TABLE `user_customuser_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_customuser_groups_customuser_id_group_id_e0a2f621_uniq` (`customuser_id`,`group_id`),
  KEY `user_customuser_groups_group_id_bcbc9e48_fk_auth_group_id` (`group_id`),
  CONSTRAINT `user_customuser_grou_customuser_id_192632a7_fk_user_cust` FOREIGN KEY (`customuser_id`) REFERENCES `user_customuser` (`id`),
  CONSTRAINT `user_customuser_groups_group_id_bcbc9e48_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

DROP TABLE IF EXISTS `user_customuser_user_permissions`;
CREATE TABLE `user_customuser_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_customuser_user_per_customuser_id_permission_a5da865d_uniq` (`customuser_id`,`permission_id`),
  KEY `user_customuser_user_permission_id_e57e8b9a_fk_auth_perm` (`permission_id`),
  CONSTRAINT `user_customuser_user_customuser_id_4552d9cc_fk_user_cust` FOREIGN KEY (`customuser_id`) REFERENCES `user_customuser` (`id`),
  CONSTRAINT `user_customuser_user_permission_id_e57e8b9a_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;

INSERT INTO `app_chatgptlog` (`id`, `request_content`, `response_content`, `created_at`, `student_id`) VALUES
(1, '三平方の定理の概要を教えてください。', '三平方の定理は、三平方の和の定理としても知られ、数を3つの完全平方和で表すことを扱う数学の定理である。この定理は1770年にジョセフ・ルイ・ラグランジュによって初めて述べられた。\n\nこの定理は、任意の自然数や整数が4^n(8m+7)の形でない場合に限り、3つの完全平方和として表現できることを述べている。\n\nもっと簡単に言えば、4^n(8m+7)の形でない数はすべて3乗の和として書けるということである。例えば、10という数は1^2 + 1^2 + 2^2と表すことができ、25という数は3^2 + 4^2 + 0^2と表すことができる。\n\nしかし、3つの2乗の和で表せない数字もある。これらの数は4^n(8m+7)の形に属し、nとmは負でない整数である。例えば、7は3つの正方形の和では表せない。\n\n三平方の定理は、整数論、代数学、さらには暗号学など、数学の様々な分野で応用されている。この定理は、数がどのように2乗の和として表されるかについての基本的な理解を提供し、関連する数学的問題を解くのに役立つ。', '2023-09-12 02:26:06.308410', 2),
(2, '私は中学2年生です。三平方の定理を勉強', '三平方の定理を勉強しているとは素晴らしいですね！三平方の定理は、2乗の和に関するフェルマーの定理としても知られ、数学の興味深いトピックです。この定理は、奇数の素数が、4のモジュロで1と合同である場合に限り、3つの完全平方和として表すことができるというものです。\n\n三平方の定理に関する具体的な質問や、特定の概念を理解する手助けが必要な場合は、遠慮なくお尋ねください。あなたの勉強をお手伝いします。', '2023-09-12 02:27:11.789867', 2);

INSERT INTO `app_city` (`id`, `city`, `is_active`, `prefecture_id`) VALUES
(382019, '松山市', 0, 38),
(382027, '今治市', 1, 38),
(382035, '宇和島市', 0, 38),
(382043, '八幡浜市', 0, 38),
(382051, '新居浜市', 0, 38),
(382060, '西条市', 0, 38),
(382078, '大洲市', 0, 38),
(382108, '伊予市', 0, 38),
(382132, '四国中央市', 0, 38),
(382141, '西予市', 0, 38),
(382159, '東温市', 0, 38),
(383562, '上島町', 0, 38),
(383864, '久万高原町', 0, 38),
(384011, '松前町', 0, 38),
(384020, '砥部町', 0, 38),
(384224, '内子町', 0, 38),
(384429, '伊方町', 0, 38),
(384844, '松野町', 0, 38),
(384887, '鬼北町', 0, 38),
(385069, '愛南町', 0, 38);

INSERT INTO `app_place` (`id`, `place_name`, `postal_code`, `address`, `entry_date`, `city_id`, `prefecture_id`) VALUES
(1, '今治商店街', '7940015', '常磐町3丁目4-1', '2023-04-01', 382027, 38);

INSERT INTO `app_prefecture` (`id`, `prefecture`, `is_active`) VALUES
(1, '北海道', 0),
(2, '青森県', 0),
(3, '岩手県', 0),
(4, '宮城県', 0),
(5, '秋田県', 0),
(6, '山形県', 0),
(7, '福島県', 0),
(8, '茨城県', 0),
(9, '栃木県', 0),
(10, '群馬県', 0),
(11, '埼玉県', 0),
(12, '千葉県', 0),
(13, '東京都', 0),
(14, '神奈川県', 0),
(15, '新潟県', 0),
(16, '富山県', 0),
(17, '石川県', 0),
(18, '福井県', 0),
(19, '山梨県', 0),
(20, '長野県', 0),
(21, '岐阜県', 0),
(22, '静岡県', 0),
(23, '愛知県', 0),
(24, '三重県', 0),
(25, '滋賀県', 0),
(26, '京都府', 0),
(27, '大阪府', 0),
(28, '兵庫県', 0),
(29, '奈良県', 0),
(30, '和歌山県', 0),
(31, '鳥取県', 0),
(32, '島根県', 0),
(33, '岡山県', 0),
(34, '広島県', 0),
(35, '山口県', 0),
(36, '徳島県', 0),
(37, '香川県', 0),
(38, '愛媛県', 1),
(39, '高知県', 0),
(40, '福岡県', 0),
(41, '佐賀県', 0),
(42, '長崎県', 0),
(43, '熊本県', 0),
(44, '大分県', 0),
(45, '宮崎県', 0),
(46, '鹿児島県', 0),
(47, '沖縄県', 0);

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add calendar', 6, 'add_calendar'),
(22, 'Can change calendar', 6, 'change_calendar'),
(23, 'Can delete calendar', 6, 'delete_calendar'),
(24, 'Can view calendar', 6, 'view_calendar'),
(25, 'Can add chat gpt log', 7, 'add_chatgptlog'),
(26, 'Can change chat gpt log', 7, 'change_chatgptlog'),
(27, 'Can delete chat gpt log', 7, 'delete_chatgptlog'),
(28, 'Can view chat gpt log', 7, 'view_chatgptlog'),
(29, 'Can add city', 8, 'add_city'),
(30, 'Can change city', 8, 'change_city'),
(31, 'Can delete city', 8, 'delete_city'),
(32, 'Can view city', 8, 'view_city'),
(33, 'Can add coupon', 9, 'add_coupon'),
(34, 'Can change coupon', 9, 'change_coupon'),
(35, 'Can delete coupon', 9, 'delete_coupon'),
(36, 'Can view coupon', 9, 'view_coupon'),
(37, 'Can add coupon student', 10, 'add_couponstudent'),
(38, 'Can change coupon student', 10, 'change_couponstudent'),
(39, 'Can delete coupon student', 10, 'delete_couponstudent'),
(40, 'Can view coupon student', 10, 'view_couponstudent'),
(41, 'Can add meeting', 11, 'add_meeting'),
(42, 'Can change meeting', 11, 'change_meeting'),
(43, 'Can delete meeting', 11, 'delete_meeting'),
(44, 'Can view meeting', 11, 'view_meeting'),
(45, 'Can add prefecture', 12, 'add_prefecture'),
(46, 'Can change prefecture', 12, 'change_prefecture'),
(47, 'Can delete prefecture', 12, 'delete_prefecture'),
(48, 'Can view prefecture', 12, 'view_prefecture'),
(49, 'Can add place', 13, 'add_place'),
(50, 'Can change place', 13, 'change_place'),
(51, 'Can delete place', 13, 'delete_place'),
(52, 'Can view place', 13, 'view_place'),
(53, 'Can add meeting schedule', 14, 'add_meetingschedule'),
(54, 'Can change meeting schedule', 14, 'change_meetingschedule'),
(55, 'Can delete meeting schedule', 14, 'delete_meetingschedule'),
(56, 'Can view meeting schedule', 14, 'view_meetingschedule'),
(57, 'Can add atama plus', 15, 'add_atamaplus'),
(58, 'Can change atama plus', 15, 'change_atamaplus'),
(59, 'Can delete atama plus', 15, 'delete_atamaplus'),
(60, 'Can view atama plus', 15, 'view_atamaplus'),
(61, 'Can add average test result', 16, 'add_averagetestresult'),
(62, 'Can change average test result', 16, 'change_averagetestresult'),
(63, 'Can delete average test result', 16, 'delete_averagetestresult'),
(64, 'Can view average test result', 16, 'view_averagetestresult'),
(65, 'Can add club activity', 17, 'add_clubactivity'),
(66, 'Can change club activity', 17, 'change_clubactivity'),
(67, 'Can delete club activity', 17, 'delete_clubactivity'),
(68, 'Can view club activity', 17, 'view_clubactivity'),
(69, 'Can add school', 18, 'add_school'),
(70, 'Can change school', 18, 'change_school'),
(71, 'Can delete school', 18, 'delete_school'),
(72, 'Can view school', 18, 'view_school'),
(73, 'Can add school category', 19, 'add_schoolcategory'),
(74, 'Can change school category', 19, 'change_schoolcategory'),
(75, 'Can delete school category', 19, 'delete_schoolcategory'),
(76, 'Can view school category', 19, 'view_schoolcategory'),
(77, 'Can add student', 20, 'add_student'),
(78, 'Can change student', 20, 'change_student'),
(79, 'Can delete student', 20, 'delete_student'),
(80, 'Can view student', 20, 'view_student'),
(81, 'Can add student target', 21, 'add_studenttarget'),
(82, 'Can change student target', 21, 'change_studenttarget'),
(83, 'Can delete student target', 21, 'delete_studenttarget'),
(84, 'Can view student target', 21, 'view_studenttarget'),
(85, 'Can add study sapuri', 22, 'add_studysapuri'),
(86, 'Can change study sapuri', 22, 'change_studysapuri'),
(87, 'Can delete study sapuri', 22, 'delete_studysapuri'),
(88, 'Can view study sapuri', 22, 'view_studysapuri'),
(89, 'Can add subject', 23, 'add_subject'),
(90, 'Can change subject', 23, 'change_subject'),
(91, 'Can delete subject', 23, 'delete_subject'),
(92, 'Can view subject', 23, 'view_subject'),
(93, 'Can add test category', 24, 'add_testcategory'),
(94, 'Can change test category', 24, 'change_testcategory'),
(95, 'Can delete test category', 24, 'delete_testcategory'),
(96, 'Can view test category', 24, 'view_testcategory'),
(97, 'Can add test result', 25, 'add_testresult'),
(98, 'Can change test result', 25, 'change_testresult'),
(99, 'Can delete test result', 25, 'delete_testresult'),
(100, 'Can view test result', 25, 'view_testresult'),
(101, 'Can add trainer', 26, 'add_trainer'),
(102, 'Can change trainer', 26, 'change_trainer'),
(103, 'Can delete trainer', 26, 'delete_trainer'),
(104, 'Can view trainer', 26, 'view_trainer'),
(105, 'Can add user', 27, 'add_customuser'),
(106, 'Can change user', 27, 'change_customuser'),
(107, 'Can delete user', 27, 'delete_customuser'),
(108, 'Can view user', 27, 'view_customuser'),
(109, 'Can add shop', 28, 'add_shop'),
(110, 'Can change shop', 28, 'change_shop'),
(111, 'Can delete shop', 28, 'delete_shop'),
(112, 'Can view shop', 28, 'view_shop');

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session'),
(6, 'app', 'calendar'),
(7, 'app', 'chatgptlog'),
(8, 'app', 'city'),
(9, 'app', 'coupon'),
(10, 'app', 'couponstudent'),
(11, 'app', 'meeting'),
(12, 'app', 'prefecture'),
(13, 'app', 'place'),
(14, 'app', 'meetingschedule'),
(15, 'student', 'atamaplus'),
(16, 'student', 'averagetestresult'),
(17, 'student', 'clubactivity'),
(18, 'student', 'school'),
(19, 'student', 'schoolcategory'),
(20, 'student', 'student'),
(21, 'student', 'studenttarget'),
(22, 'student', 'studysapuri'),
(23, 'student', 'subject'),
(24, 'student', 'testcategory'),
(25, 'student', 'testresult'),
(26, 'trainer', 'trainer'),
(27, 'user', 'customuser'),
(28, 'shop', 'shop');

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2023-05-07 15:52:02.950820'),
(2, 'contenttypes', '0002_remove_content_type_name', '2023-05-07 15:52:02.968472'),
(3, 'auth', '0001_initial', '2023-05-07 15:52:03.035297'),
(4, 'auth', '0002_alter_permission_name_max_length', '2023-05-07 15:52:03.050849'),
(5, 'auth', '0003_alter_user_email_max_length', '2023-05-07 15:52:03.054405'),
(6, 'auth', '0004_alter_user_username_opts', '2023-05-07 15:52:03.057836'),
(7, 'auth', '0005_alter_user_last_login_null', '2023-05-07 15:52:03.061269'),
(8, 'auth', '0006_require_contenttypes_0002', '2023-05-07 15:52:03.062371'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2023-05-07 15:52:03.066622'),
(10, 'auth', '0008_alter_user_username_max_length', '2023-05-07 15:52:03.070275'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2023-05-07 15:52:03.074569'),
(12, 'auth', '0010_alter_group_name_max_length', '2023-05-07 15:52:03.082359'),
(13, 'auth', '0011_update_proxy_permissions', '2023-05-07 15:52:03.086902'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2023-05-07 15:52:03.090514'),
(15, 'user', '0001_initial', '2023-05-07 15:52:03.165650'),
(16, 'admin', '0001_initial', '2023-05-07 15:52:03.204087'),
(17, 'admin', '0002_logentry_remove_auto_add', '2023-05-07 15:52:03.209822'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2023-05-07 15:52:03.215187'),
(19, 'student', '0001_initial', '2023-05-07 15:52:03.372834'),
(20, 'app', '0001_initial', '2023-05-07 15:52:03.459111'),
(21, 'app', '0002_initial', '2023-05-07 15:52:03.479518'),
(22, 'trainer', '0001_initial', '2023-05-07 15:52:03.521570'),
(23, 'shop', '0001_initial', '2023-05-07 15:52:03.528755'),
(24, 'app', '0003_initial', '2023-05-07 15:52:03.712696'),
(25, 'app', '0004_initial', '2023-05-07 15:52:03.743766'),
(26, 'sessions', '0001_initial', '2023-05-07 15:52:03.755676'),
(27, 'shop', '0002_initial', '2023-05-07 15:52:03.786409'),
(28, 'student', '0002_initial', '2023-05-07 15:52:04.280620'),
(29, 'trainer', '0002_initial', '2023-05-07 15:52:04.318415');

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('2lpvobz3cvtvhkk36zr1z2l8ovi1rjrl', '.eJxVjMsOwiAUBf-FtSFAGx4u3fsN5F44laqBpLQr479rky50e2bmvESkbS1x61jinMVZaHH63ZjSA3UH-U711mRqdV1mlrsiD9rltWU8L4f7d1Col289ManBUUgBxmDUk1bBwyAoE5CtG8n7IVmrLDtWg1EpATmTBiyBrXh_AOnXOIw:1pvh8K:7gNt6ubBPQGTSZUL4nKDgFPt2v3pUlHdYIKh1gyV3p4', '2023-05-21 16:21:12.724042'),
('6g84xziv979qjbgel1nkso9lytpjrix2', 'eyJsb2dpbl9yZWZlcmVyIjoiLyJ9:1qybgt:NSPseDLtubeSE7_0Qpg2BkPWE6BhUQv7dpyXU2qQE2U', '2023-11-16 17:41:11.445230'),
('954c9235f8hag48kaq99cmxje3r9qtfm', '.eJxVjDsOwyAQBe9CHRGvAQMp0-cMaGHXn8QCCdtVlLvHlty4nZn3vmIuw5RD5Z4rV_EQd3ETAbd1DNvCNUy0s_bKIqYP50PQG_NQZCp5rVOURyJPu8hXIZ6fZ3s5GHEZ97VTmpLV3hNEk4CwJx8RyGiEpHRSTQSHHoxrYu-s1dBil7pOG7atQhC_P5IGPhY:1pvheG:8unEeCEaakpjfLYRVj3JizMyJPsqZZLVgsigkhSp4B0', '2023-05-21 16:54:12.521726'),
('mo2j8dv2g03v68c9yyjem1hpqquifb83', '.eJxVjDsOwjAQBe_iGlnr-E9JnzNYu16DA8iR4qRC3B0ipYD2zcx7iYTbWtPWy5ImFmehxOl3I8yP0nbAd2y3Wea5rctEclfkQbscZy7Py-H-HVTs9Vtbq1zQrBUHZLDKMjq0xrA3VIoOkWN0XhvwCkhdIWQfbAA_DMZHIBLvD7vbNoo:1qftAX:0dZmikxzeaCUnmtBYLnBnZIRQ5XwMsyw19vbwpn-g_8', '2023-09-26 02:30:25.755370');

INSERT INTO `student_atamaplus` (`id`, `login_id`, `password`, `site_url`, `user_id`) VALUES
(1, 'soga_minoru', 'minoru', '', 3);

INSERT INTO `student_clubactivity` (`id`, `club_activity`) VALUES
(1, '野球部'),
(2, 'ボート部'),
(3, '水泳部'),
(4, 'バレーボール部'),
(5, 'サッカー部'),
(6, 'バスケットボール部'),
(7, '陸上競技部'),
(8, 'バドミントン部'),
(9, '卓球部'),
(10, 'テニス部'),
(11, 'ソフトテニス部'),
(12, '柔道部'),
(13, '剣道部'),
(14, '弓道部'),
(15, 'ダンス部'),
(16, 'ハンドボール部'),
(17, '空手道部'),
(18, '理科部'),
(19, 'ワープロ部'),
(20, '文芸部'),
(21, '美術部'),
(22, '写真部'),
(23, 'クッキング部'),
(24, '電卓部'),
(25, '珠算部'),
(26, '書道部'),
(27, '茶道部'),
(28, '郷土研究部'),
(29, '吹奏楽部'),
(30, '国際交流部'),
(31, '商業研究部'),
(32, '簿記部'),
(33, 'コンピュータ部'),
(34, '放送部'),
(35, '箏部'),
(36, '華道部');

INSERT INTO `student_school` (`id`, `school`, `school_category_id`) VALUES
(1, '吹揚小学校', 1),
(2, '別宮小学校', 1),
(3, '常盤小学校', 1),
(4, '近見小学校', 1),
(5, '立花小学校', 1),
(6, '鳥生小学校', 1),
(7, '桜井小学校', 1),
(8, '国分小学校', 1),
(9, '富田小学校', 1),
(10, '清水小学校', 1),
(11, '日高小学校', 1),
(12, '乃万小学校', 1),
(13, '波止浜小学校', 1),
(14, '朝倉小学校', 1),
(15, '鴨部小学校', 1),
(16, '九和小学校', 1),
(17, '波方小学校', 1),
(18, '大西小学校', 1),
(19, '亀岡小学校', 1),
(20, '菊間小学校', 1),
(21, '吉海小学校', 1),
(22, '宮窪小学校', 1),
(23, '伯方小学校', 1),
(24, '上浦小学校', 1),
(25, '大三島小学校', 1),
(26, '岡村小学校', 1),
(27, '日吉中学校', 2),
(28, '近見中学校', 2),
(29, '立花中学校', 2),
(30, '桜井中学校', 2),
(31, '南中学校', 2),
(32, '西中学校', 2),
(33, '北郷中学校', 2),
(34, '朝倉中学校', 2),
(35, '玉川中学校', 2),
(36, '大西中学校', 2),
(37, '菊間中学校', 2),
(38, '大島中学校', 2),
(39, '伯方中学校', 2),
(40, '大三島中学校', 2),
(41, '関前中学校', 2),
(42, '愛媛県立今治北高等学校', 3),
(43, '愛媛県立今治北高等学校　大三島分校', 3),
(44, '愛媛県立今治工業高等学校', 3),
(45, '今治精華高等学校', 3),
(46, '愛媛県立今治西高等学校', 3),
(47, '愛媛県立今治西高等学校　伯方分校', 3),
(48, '愛媛県立今治南高等学校', 3),
(49, '今治明徳高等学校', 3),
(50, '今治明徳高等学校　矢田分校', 3);

INSERT INTO `student_schoolcategory` (`id`, `school_category`) VALUES
(1, '小学校'),
(2, '中学校'),
(3, '高等学校');

INSERT INTO `student_student` (`id`, `last_name`, `first_name`, `last_name_kana`, `first_name_kana`, `grade`, `school_class`, `phone_number`, `parent_last_name`, `parent_first_name`, `parent_last_name_kana`, `parent_first_name_kana`, `parent_phone_number`, `parent_email`, `zipcode`, `address`, `entry_date`, `expiration_date`, `stripe_data`, `introducer_last_name`, `introducer_first_name`, `unsubscribe_request`, `city_id`, `club_activity_id`, `prefecture_id`, `school_id`, `user_id`) VALUES
(1, '曽我', '稔', 'ソガ', 'ミノル', '1', '2', '', '曽我', '佳加', 'ソガ', 'ヨシカ', '08072777231', 'minoru.2021@gmail.com', '7940015', '常盤町3丁目4-1', NULL, NULL, NULL, NULL, NULL, 0, 382027, 2, 38, 42, 2),
(2, '曽我', '稔', 'ソガ', 'ミノル', '2', '2', '08072777231', '', '', '', '', '', '', '794-0015', '常磐町4丁目8-18 しまなみイノベーションビル401', NULL, NULL, NULL, NULL, NULL, 0, 382027, 2, 38, 42, 3);

INSERT INTO `student_subject` (`id`, `subject`, `grade`, `school_category_id`) VALUES
(1, '国語', NULL, 1),
(2, '算数', NULL, 1),
(3, '理科', NULL, 1),
(4, '社会', NULL, 1),
(5, '英語', NULL, 1),
(6, '国語', NULL, 2),
(7, '数学', NULL, 2),
(8, '理科', NULL, 2),
(9, '社会', NULL, 2),
(10, '英語', NULL, 2),
(11, '国語', NULL, 3),
(12, '数学', NULL, 3),
(13, '理科', NULL, 3),
(14, '社会', NULL, 3),
(15, '英語', NULL, 3);

INSERT INTO `user_customuser` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `user_type`) VALUES
(1, 'pbkdf2_sha256$390000$6SkLJf2YooUKciXeBZVYe0$6heJelvD7uXCyfNPIvJmrRRYDGB/7lHqfjQJjoOhNDY=', '2023-09-12 02:30:25.753322', 1, 'barijuku', '', '', 'bari.juku@gmail.com', 1, 1, '2023-05-07 15:53:06.553818', ''),
(2, 'pbkdf2_sha256$390000$T055VMWxUQeJAXcbfPOc4O$A8RhlVMeIY9JYTLcyx5DecRAZGqMUN/0KORnMYVweQ8=', '2023-05-07 16:54:12.512845', 0, '曽我', '', '', '', 0, 1, '2023-05-07 16:12:21.073007', 'STUDENT'),
(3, 'pbkdf2_sha256$390000$6SkLJf2YooUKciXeBZVYe0$6heJelvD7uXCyfNPIvJmrRRYDGB/7lHqfjQJjoOhNDY=', '2023-09-12 02:21:34.228312', 0, 'soga_minoru', '', '', '', 0, 1, '2023-09-12 02:21:33.722437', 'STUDENT');



/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
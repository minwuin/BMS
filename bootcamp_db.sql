-- --------------------------------------------------------
-- 호스트:                          127.0.0.1
-- 서버 버전:                        12.1.2-MariaDB - MariaDB Server
-- 서버 OS:                        Win64
-- HeidiSQL 버전:                  12.11.0.7065
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- bootcamp_db 데이터베이스 구조 내보내기
CREATE DATABASE IF NOT EXISTS `bootcamp_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci */;
USE `bootcamp_db`;

-- 테이블 bootcamp_db.2_toilet_reservation 구조 내보내기
CREATE TABLE IF NOT EXISTS `2_toilet_reservation` (
  `res_id` int(11) NOT NULL AUTO_INCREMENT,
  `sex` tinyblob NOT NULL,
  `toilet_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `password` int(4) NOT NULL DEFAULT 1111,
  PRIMARY KEY (`res_id`) USING BTREE,
  KEY `student_id` (`student_id`) USING BTREE,
  CONSTRAINT `1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci ROW_FORMAT=DYNAMIC;

-- 테이블 데이터 bootcamp_db.2_toilet_reservation:~1 rows (대략적) 내보내기
INSERT IGNORE INTO `2_toilet_reservation` (`res_id`, `sex`, `toilet_id`, `student_id`, `start_time`, `end_time`, `password`) VALUES
	(10, _binary 0xec97ac, 1, 23, '2026-01-30 15:00:00', '2026-01-30 18:00:00', 1234);

-- 테이블 bootcamp_db.7_toilet_reservation 구조 내보내기
CREATE TABLE IF NOT EXISTS `7_toilet_reservation` (
  `res_id` int(11) NOT NULL AUTO_INCREMENT,
  `sex` tinyblob NOT NULL,
  `toilet_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `password` int(4) NOT NULL DEFAULT 1111,
  PRIMARY KEY (`res_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `student_id` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 테이블 데이터 bootcamp_db.7_toilet_reservation:~1 rows (대략적) 내보내기
INSERT IGNORE INTO `7_toilet_reservation` (`res_id`, `sex`, `toilet_id`, `student_id`, `start_time`, `end_time`, `password`) VALUES
	(10, _binary 0xeb82a8, 1, 9, '2026-01-30 15:30:00', '2026-01-30 00:00:00', 1234);

-- 테이블 bootcamp_db.attendance 구조 내보내기
CREATE TABLE IF NOT EXISTS `attendance` (
  `attendance_id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) NOT NULL,
  `check_in_time` datetime DEFAULT NULL,
  `check_out_time` datetime DEFAULT NULL,
  `status` enum('정상','지각','조퇴','결석') NOT NULL,
  PRIMARY KEY (`attendance_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 테이블 데이터 bootcamp_db.attendance:~24 rows (대략적) 내보내기
INSERT IGNORE INTO `attendance` (`attendance_id`, `student_id`, `check_in_time`, `check_out_time`, `status`) VALUES
	(1, 12, '2026-01-29 13:23:49', NULL, '정상'),
	(2, 4, '2026-01-29 13:23:49', NULL, '정상'),
	(3, 2, '2026-01-29 13:23:49', NULL, '정상'),
	(4, 16, '2026-01-29 13:23:49', NULL, '정상'),
	(5, 18, '2026-01-29 13:23:49', NULL, '정상'),
	(6, 13, '2026-01-29 13:23:49', NULL, '정상'),
	(7, 23, '2026-01-29 13:23:49', NULL, '정상'),
	(8, 15, '2026-01-29 13:23:49', NULL, '정상'),
	(9, 10, '2026-01-29 13:23:49', NULL, '정상'),
	(10, 19, '2026-01-29 13:23:49', NULL, '정상'),
	(11, 1, '2026-01-29 13:23:49', NULL, '정상'),
	(12, 11, '2026-01-29 13:23:49', NULL, '정상'),
	(13, 22, '2026-01-29 13:23:49', NULL, '정상'),
	(14, 5, '2026-01-29 13:23:49', NULL, '정상'),
	(15, 3, '2026-01-29 13:23:49', NULL, '정상'),
	(16, 9, '2026-01-29 13:23:49', NULL, '정상'),
	(17, 8, '2026-01-29 13:23:49', NULL, '정상'),
	(18, 7, '2026-01-29 13:23:49', NULL, '정상'),
	(19, 17, '2026-01-29 13:23:49', NULL, '정상'),
	(20, 6, '2026-01-29 13:23:49', NULL, '정상'),
	(21, 14, '2026-01-29 13:23:49', NULL, '정상'),
	(22, 24, '2026-01-29 13:23:49', NULL, '정상'),
	(23, 21, '2026-01-29 13:23:49', NULL, '정상'),
	(24, 20, '2026-01-29 13:23:49', NULL, '정상');

-- 테이블 bootcamp_db.desk 구조 내보내기
CREATE TABLE IF NOT EXISTS `desk` (
  `desk_id` int(11) NOT NULL,
  `row_idx` int(11) NOT NULL,
  `col_idx` int(11) NOT NULL,
  `student_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`desk_id`),
  KEY `fk_desk_student` (`student_id`),
  CONSTRAINT `fk_desk_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 테이블 데이터 bootcamp_db.desk:~35 rows (대략적) 내보내기
INSERT IGNORE INTO `desk` (`desk_id`, `row_idx`, `col_idx`, `student_id`) VALUES
	(1, 0, 0, 1),
	(2, 0, 1, 2),
	(3, 0, 2, 3),
	(4, 0, 3, NULL),
	(5, 0, 4, NULL),
	(6, 0, 5, 4),
	(7, 0, 6, NULL),
	(8, 0, 7, NULL),
	(9, 0, 8, 5),
	(10, 0, 9, 6),
	(11, 1, 0, 7),
	(12, 1, 1, 8),
	(13, 1, 2, NULL),
	(14, 1, 3, NULL),
	(15, 1, 4, 10),
	(16, 1, 5, 11),
	(17, 1, 6, NULL),
	(18, 1, 7, 12),
	(19, 1, 8, NULL),
	(20, 1, 9, 13),
	(21, 2, 0, 14),
	(22, 2, 1, 15),
	(23, 2, 2, 16),
	(24, 2, 3, NULL),
	(25, 2, 4, 17),
	(26, 2, 5, 18),
	(27, 2, 6, NULL),
	(28, 2, 7, 19),
	(29, 2, 8, NULL),
	(30, 2, 9, 20),
	(31, 3, 0, 21),
	(32, 3, 1, 9),
	(33, 3, 2, 22),
	(34, 3, 3, 23),
	(35, 3, 4, 24);

-- 테이블 bootcamp_db.game_rentals 구조 내보내기
CREATE TABLE IF NOT EXISTS `game_rentals` (
  `rental_id` int(11) NOT NULL AUTO_INCREMENT,
  `game_device` enum('게임기 1','게임기 2') NOT NULL,
  `student_id` int(11) NOT NULL,
  `rental_start` datetime NOT NULL,
  `is_returned` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`rental_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 테이블 데이터 bootcamp_db.game_rentals:~2 rows (대략적) 내보내기
INSERT IGNORE INTO `game_rentals` (`rental_id`, `game_device`, `student_id`, `rental_start`, `is_returned`) VALUES
	(1, '게임기 1', 3, '2026-01-29 13:33:16', 0),
	(2, '게임기 2', 8, '2026-01-29 13:33:16', 0);

-- 테이블 bootcamp_db.room_reservations 구조 내보내기
CREATE TABLE IF NOT EXISTS `room_reservations` (
  `res_id` int(11) NOT NULL AUTO_INCREMENT,
  `room_number` tinyint(4) NOT NULL,
  `student_id` int(11) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `purpose` varchar(100) DEFAULT NULL,
  `password` int(4) NOT NULL,
  PRIMARY KEY (`res_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
  CONSTRAINT `chk_room` CHECK (`room_number` between 1 and 8)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 테이블 데이터 bootcamp_db.room_reservations:~6 rows (대략적) 내보내기
INSERT IGNORE INTO `room_reservations` (`res_id`, `room_number`, `student_id`, `start_time`, `end_time`, `purpose`, `password`) VALUES
	(12, 2, 15, '2026-01-30 09:00:00', '2026-01-30 18:00:00', '팀 프로젝트', 1234),
	(13, 2, 14, '2026-01-30 09:00:00', '2026-01-30 18:00:00', '팀 프로젝트', 1234),
	(14, 2, 23, '2026-01-30 09:00:00', '2026-01-30 18:00:00', '팀 프로젝트', 1234),
	(15, 2, 1, '2026-01-30 09:00:00', '2026-01-30 18:00:00', '팀 프로젝트', 1234),
	(16, 2, 6, '2026-01-30 09:00:00', '2026-01-30 18:00:00', '팀 프로젝트', 1234);

-- 테이블 bootcamp_db.snacks 구조 내보내기
CREATE TABLE IF NOT EXISTS `snacks` (
  `snack_id` int(11) NOT NULL AUTO_INCREMENT,
  `snack_name` varchar(50) NOT NULL,
  `category` varchar(20) DEFAULT NULL,
  `price` int(11) DEFAULT 0,
  `current_stock` int(11) DEFAULT 0,
  `restock_date` date DEFAULT NULL,
  PRIMARY KEY (`snack_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 테이블 데이터 bootcamp_db.snacks:~10 rows (대략적) 내보내기
INSERT IGNORE INTO `snacks` (`snack_id`, `snack_name`, `category`, `price`, `current_stock`, `restock_date`) VALUES
	(1, '쿠쿠다스 케이크', '과자', 2500, 30, '2026-01-29'),
	(2, '빅팜', '소시지', 1500, 50, '2026-01-25'),
	(3, '빅파이', '과자', 4000, 20, '2026-01-24'),
	(4, '후레쉬베리', '과자', 5000, 15, '2026-01-27'),
	(5, '킷캣', '초콜릿', 1200, 40, '2026-01-19'),
	(6, '두유', '음료', 1000, 60, '2026-01-29'),
	(7, '밀카 무', '과자', 3500, 25, '2026-01-23'),
	(8, '빈츠', '과자', 2800, 35, '2026-01-29'),
	(9, '마가렛트', '과자', 4500, 20, '2026-01-26'),
	(10, '박카스', '음료', 800, 100, '2026-01-24');

-- 테이블 bootcamp_db.snacks_apply 구조 내보내기
CREATE TABLE IF NOT EXISTS `snacks_apply` (
  `snack_id` int(11) NOT NULL AUTO_INCREMENT,
  `snack_name` varchar(50) NOT NULL,
  `count` int(11) DEFAULT 0,
  `apply_id` int(11) NOT NULL,
  PRIMARY KEY (`snack_id`) USING BTREE,
  KEY `apply_id` (`apply_id`),
  CONSTRAINT `apply_id` FOREIGN KEY (`apply_id`) REFERENCES `students` (`student_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci ROW_FORMAT=DYNAMIC;

-- 테이블 데이터 bootcamp_db.snacks_apply:~3 rows (대략적) 내보내기
INSERT IGNORE INTO `snacks_apply` (`snack_id`, `snack_name`, `count`, `apply_id`) VALUES
	(1, '킷캣(말차)', 20, 13),
	(2, '밀카 무', 5, 17),
	(3, '후레시 베리', 20, 9);

-- 테이블 bootcamp_db.sofa_reservation 구조 내보내기
CREATE TABLE IF NOT EXISTS `sofa_reservation` (
  `res_id` int(11) NOT NULL AUTO_INCREMENT,
  `sofa_number` tinyint(4) NOT NULL,
  `student_id` int(11) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `password` int(4) NOT NULL,
  PRIMARY KEY (`res_id`) USING BTREE,
  KEY `student_id` (`student_id`) USING BTREE,
  CONSTRAINT `1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci ROW_FORMAT=DYNAMIC;

-- 테이블 데이터 bootcamp_db.sofa_reservation:~1 rows (대략적) 내보내기
INSERT IGNORE INTO `sofa_reservation` (`res_id`, `sofa_number`, `student_id`, `start_time`, `end_time`, `password`) VALUES
	(15, 1, 11, '2026-01-30 09:00:00', '2026-01-30 22:00:00', 1234);

-- 테이블 bootcamp_db.students 구조 내보내기
CREATE TABLE IF NOT EXISTS `students` (
  `student_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `gender` enum('남','여') NOT NULL,
  `birth_date` date DEFAULT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(50) DEFAULT NULL,
  `is_major` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 테이블 데이터 bootcamp_db.students:~25 rows (대략적) 내보내기
INSERT IGNORE INTO `students` (`student_id`, `name`, `gender`, `birth_date`, `phone`, `email`, `is_major`) VALUES
	(1, '김세현', '남', '1996-01-13', '010-3890-5722', 'user1@example.com', 1),
	(2, '이민섭', '남', '2001-06-30', '010-1628-1960', 'user2@example.com', 1),
	(3, '장현근', '남', '2001-07-20', '010-5543-5210', 'user3@example.com', 0),
	(4, '박재민', '남', '2003-03-29', '010-1494-1520', 'user4@example.com', 0),
	(5, '김준영', '남', '1995-06-08', '010-5537-8747', 'user5@example.com', 0),
	(6, '이인우', '남', '2002-06-20', '010-8391-5690', 'user6@example.com', 1),
	(7, '김홍근', '남', '2004-02-18', '010-6979-9098', 'user7@example.com', 1),
	(8, '금경훈', '남', '1997-04-09', '010-6537-9964', 'user8@example.com', 1),
	(9, '김예진', '여', '1996-07-11', '010-6213-5728', 'user9@example.com', 1),
	(10, '진민영', '여', '1999-04-28', '010-3278-5048', 'user10@example.com', 1),
	(11, '정병채', '남', '1999-11-13', '010-4403-5281', 'user11@example.com', 0),
	(12, '안선우', '남', '2002-03-27', '010-1393-3459', 'user12@example.com', 1),
	(13, '김진섭', '남', '2002-02-27', '010-2778-4961', 'user13@example.com', 0),
	(14, '민우인', '남', '1995-02-19', '010-8648-6927', 'user14@example.com', 1),
	(15, '송승민', '남', '2000-07-08', '010-3218-2783', 'user15@example.com', 1),
	(16, '노경덕', '남', '1998-01-21', '010-1933-9538', 'user16@example.com', 1),
	(17, '최창연', '남', '2001-04-01', '010-7299-1417', 'user17@example.com', 0),
	(18, '김세훈', '남', '1997-06-03', '010-2778-4542', 'user18@example.com', 0),
	(19, '장현호', '남', '2000-12-20', '010-3538-1916', 'user19@example.com', 0),
	(20, '이순재', '남', '2001-09-30', '010-9701-8553', 'user20@example.com', 0),
	(21, '박세진', '남', '1997-07-23', '010-8912-5695', 'user21@example.com', 0),
	(22, '구효제', '여', '1996-05-05', '010-5340-3838', 'user22@example.com', 1),
	(23, '김진수', '남', '1999-06-25', '010-2997-4032', 'user23@example.com', 0),
	(24, '문지하', '남', '1998-01-15', '010-8697-7711', 'user24@example.com', 0),
	(25, '김기석', '남', '2026-01-30', '010-4328-1014', 'user25@example.com', 0);

-- 테이블 bootcamp_db.toilet_status 구조 내보내기
CREATE TABLE IF NOT EXISTS `toilet_status` (
  `toilet_id` int(11) NOT NULL AUTO_INCREMENT,
  `floor` tinyint(4) NOT NULL,
  `gender` enum('남','여') NOT NULL,
  `stall_number` tinyint(4) NOT NULL,
  `is_occupied` tinyint(1) DEFAULT 0,
  `current_user_id` int(11) DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `password` int(4) NOT NULL DEFAULT 1111,
  PRIMARY KEY (`toilet_id`),
  KEY `current_user_id` (`current_user_id`),
  CONSTRAINT `1` FOREIGN KEY (`current_user_id`) REFERENCES `students` (`student_id`),
  CONSTRAINT `chk_floor_val` CHECK (`floor` in (2,7))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 테이블 데이터 bootcamp_db.toilet_status:~0 rows (대략적) 내보내기

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;

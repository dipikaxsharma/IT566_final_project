SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
USE `dipika_ad_project`;

CREATE TABLE IF NOT EXISTS `campaign` (
  `campaign_id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `company` varchar(100) NOT NULL,
  `budget` decimal(10,2) DEFAULT NULL,
  `status` enum('active','paused','ended') DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  PRIMARY KEY (`campaign_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Store ad campaign data.';

CREATE TABLE IF NOT EXISTS `channel` (
  `channel_id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `type` enum('social','search','email','video') DEFAULT NULL,
  `status` enum('active','inactive') DEFAULT NULL,
  PRIMARY KEY (`channel_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Store distribution channel data.';

CREATE TABLE IF NOT EXISTS `campaign_channel_xref` (
  `xref_id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `campaign_id` int UNSIGNED NOT NULL,
  `channel_id` int UNSIGNED NOT NULL,
  `spend` decimal(10,2) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  PRIMARY KEY (`xref_id`),
  KEY `campaign_id_fk_constraint` (`campaign_id`),
  KEY `channel_id_fk_constraint` (`channel_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
COMMENT='Relates campaigns to the channels they run on.';

ALTER TABLE `campaign_channel_xref`
  ADD CONSTRAINT `campaign_id_fk_constraint` FOREIGN KEY (`campaign_id`)
    REFERENCES `campaign` (`campaign_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `channel_id_fk_constraint` FOREIGN KEY (`channel_id`)
    REFERENCES `channel` (`channel_id`) ON DELETE CASCADE ON UPDATE CASCADE;

COMMIT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

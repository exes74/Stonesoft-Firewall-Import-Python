--CREATION OF THE FLOW MATRIX


CREATE TABLE IF NOT EXISTS `firewall_flow_matrix` (
  `id` int(11) NOT NULL,
  `key_rule` text COLLATE utf8_general_mysql500_ci NOT NULL,
  `id_import` int(11) NOT NULL,
  `firewall_name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `type_fw` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `safe` varchar(100) COLLATE utf8_general_mysql500_ci NOT NULL,
  `new` varchar(10) COLLATE utf8_general_mysql500_ci NOT NULL,
  `source` text COLLATE utf8_general_mysql500_ci NOT NULL,
  `dest` text COLLATE utf8_general_mysql500_ci NOT NULL,
  `protocole_port` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `comment` varchar(255) COLLATE utf8_general_mysql500_ci DEFAULT NULL,
  `action` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `log_level` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `rule_number` decimal(11,1) NOT NULL,
  `dest_zone` varchar(255) COLLATE utf8_general_mysql500_ci DEFAULT NULL,
  `target_zone` varchar(255) COLLATE utf8_general_mysql500_ci DEFAULT NULL,
  `rule_status` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `obso_counter` int(11) NOT NULL,
  `ref` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=25438 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;


--CREATION OF THE NEEDS MATRIX

CREATE TABLE IF NOT EXISTS `firewall_needs` (
  `id` int(11) NOT NULL,
  `title` text COLLATE utf8_general_mysql500_ci NOT NULL,
  `requester` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `source` text COLLATE utf8_general_mysql500_ci NOT NULL,
  `destination` text COLLATE utf8_general_mysql500_ci NOT NULL,
  `protocole` text COLLATE utf8_general_mysql500_ci NOT NULL,
  `justification` text COLLATE utf8_general_mysql500_ci NOT NULL,
  `dateapplication` date NOT NULL,
  `datecreation` date NOT NULL,
  `temporaire` int(11) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;


--CREATION OF THE FLOW MATRIX HISTO


CREATE TABLE IF NOT EXISTS `firewall_flow_matrix_histo` (
  `id` int(11) NOT NULL,
  `key_rule` text COLLATE utf8_general_mysql500_ci NOT NULL,
  `id_import` int(11) NOT NULL,
  `firewall_name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `type_fw` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `safe` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `new` varchar(10) COLLATE utf8_general_mysql500_ci NOT NULL,
  `source` text COLLATE utf8_general_mysql500_ci NOT NULL,
  `dest` text COLLATE utf8_general_mysql500_ci NOT NULL,
  `protocole_port` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `comment` varchar(255) COLLATE utf8_general_mysql500_ci DEFAULT NULL,
  `action` varchar(255) COLLATE utf8_general_mysql500_ci DEFAULT NULL,
  `log_level` varchar(255) COLLATE utf8_general_mysql500_ci DEFAULT NULL,
  `rule_number` decimal(11,1) NOT NULL,
  `dest_zone` varchar(255) COLLATE utf8_general_mysql500_ci DEFAULT NULL,
  `target_zone` varchar(255) COLLATE utf8_general_mysql500_ci DEFAULT NULL,
  `rule_status` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `obso_counter` int(11) NOT NULL,
  `ref` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=22125 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

---FLOW APPROVAL
CREATE TABLE IF NOT EXISTS `flow_approval` (
  `id` int(11) NOT NULL,
  `need_ref` text COLLATE utf8_general_mysql500_ci NOT NULL,
  `compliant` varchar(50) COLLATE utf8_general_mysql500_ci NOT NULL,
  `validated` varchar(50) COLLATE utf8_general_mysql500_ci NOT NULL,
  `dateValidation` date NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

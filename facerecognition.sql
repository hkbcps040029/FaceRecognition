-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 17, 2020 at 09:41 PM
-- Server version: 5.7.28-0ubuntu0.18.04.4
-- PHP Version: 7.2.24-0ubuntu0.18.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `facerecognition`
--

-- --------------------------------------------------------

--
-- Table structure for table `Customer`
--
DROP TABLE IF EXISTS `Customer`;

# Create TABLE 'Customer'
CREATE TABLE `Customer` (
  `customer_id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `login_time` time NOT NULL,
  `login_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `Customer` WRITE;
/*!40000 ALTER TABLE `Customer` DISABLE KEYS */;
INSERT INTO `Customer` VALUES (1, "JACK", NOW(), '2021-09-01');
/*!40000 ALTER TABLE `Customer` ENABLE KEYS */;
UNLOCK TABLES;


# Create TABLE 'Account'
# Create TABLE 'Transaction'
# Create other TABLE...


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;





-- New Additions
/*

-- Setting up Tables

CREATE TABLE Customer
(
customer_id INT NOT NULL,
customer_name VARCHAR(50) NOT NULL,
face_id INT NOT NULL,
PRIMARY KEY(customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Account
(
account_id INT NOT NULL,
account_type VARCHAR(7) NOT NULL,
balance FLOAT(28,8) SIGNED NOT NULL, # Must be HKD, even if currency different
currency VARCHAR(3) NOT NULL,
customer_id INT NOT NULL,
PRIMARY KEY(account_id),
FOREIGN KEY(customer_id) REFERENCES Customer(customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Internal_Trans
(
transaction_id INT NOT NULL,
target_acc INT NOT NULL,
transaction_description VARCHAR(50),
date_n_time DATETIME NOT NULL,
amount FLOAT(28, 8) UNSIGNED NOT NULL, # Change to UNSIGNED
account_id INT NOT NULL,
PRIMARY KEY(transaction_id),
FOREIGN KEY(account_id) references Account(account_id),
FOREIGN KEY(target_acc) references Account(account_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE External_Trans
(
transaction_id INT NOT NULL,
target_acc INT NOT NULL,
transaction_description VARCHAR(50),
date_n_time DATETIME NOT NULL,
amount FLOAT(28, 8) UNSIGNED NOT NULL,
account_id INT NOT NULL,
bank VARCHAR(50) NOT NULL,
PRIMARY KEY(transaction_id),
FOREIGN KEY(account_id) references Account(account_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Login_History
(
date_time DATETIME NOT NULL,
customer_id INT NOT NULL,
PRIMARY KEY(date_time, customer_id),
FOREIGN KEY(customer_id) references Customer(customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE Internal_Trans AUTO_INCREMENT=1;


============= ADD DUMMY DATA ============

INSERT INTO Customer VALUES
(1001, 'Tamanna', 1),
(1002, 'Andy', 2);

INSERT INTO Account VALUES
(661, 'Savings', 1200.06, 'HKD', 1001),
(662, 'Current', 5000.88, 'USD', 1002),
(663, 'Savings', 400000.21, 'HKD', 1002);

INSERT INTO Login_History VALUES
('2019-10-07 21:58:52', 1001),
('2021-12-19 14:23:59', 1002);

INSERT INTO Internal_Trans VALUES
(51, 661, 'Pay for bills', '2021-12-19 14:29:59', 500, 662);

INSERT INTO External_Trans VALUES
(52, 1728, 'Subscription', '2019-10-07 22:05:59', 100, 661, 'Bank of Delta');




*/

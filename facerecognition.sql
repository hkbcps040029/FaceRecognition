-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 17, 2020 at 09:41 PM
-- Server version: 5.7.28-0ubuntu0.18.04.4
-- PHP Version: 7.2.24-0ubuntu0.18.04.1

DROP DATABASE IF EXISTS `testDB`;
CREATE DATABASE testDB;
USE testDB;


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
DROP TABLE IF EXISTS `Account`;
DROP TABLE IF EXISTS `Internal_Trans`;
DROP TABLE IF EXISTS `ExternalAccounts`;
DROP TABLE IF EXISTS `ExternalReceive`;
DROP TABLE IF EXISTS `ExternalSend`;
DROP TABLE IF EXISTS `Login_History`;
DROP TABLE IF EXISTS `Transactions`;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;





-- New Additions


-- Setting up Tables
CREATE TABLE Customer
(
customer_id INT NOT NULL,
customer_name VARCHAR(50) NOT NULL,
password VARCHAR(16) NOT NULL,
face_id INT NOT NULL,
PRIMARY KEY(customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Account
(
account_id INT NOT NULL,
account_type VARCHAR(7) NOT NULL,
balance FLOAT SIGNED NOT NULL, # Must be HKD, even if currency different
currency VARCHAR(3) NOT NULL,
customer_id INT NOT NULL,
PRIMARY KEY(account_id),
FOREIGN KEY(customer_id) REFERENCES Customer(customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Transactions
(
transaction_id INT NOT NULL AUTO_INCREMENT,
transaction_description VARCHAR(50),
date_n_time DATETIME NOT NULL,
amount FLOAT UNSIGNED NOT NULL,
PRIMARY KEY(transaction_id)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Internal_Trans
(
transaction_id INT NOT NULL,
target_acc INT NOT NULL,
account_id INT NOT NULL,
PRIMARY KEY(transaction_id),
FOREIGN KEY(transaction_id) references Transactions(transaction_id),
FOREIGN KEY(account_id) references Account(account_id),
FOREIGN KEY(target_acc) references Account(account_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE ExternalAccounts(
bank_name VARCHAR(50) NOT NULL,
account_id INT UNSIGNED NOT NULL,
PRIMARY KEY(bank_name, account_id)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE ExternalReceive(
transaction_id INT NOT NULL,
target_account_id INT NOT NULL,
sender_bank_name VARCHAR(50) NOT NULL,
sender_account_id INT UNSIGNED NOT NULL,
PRIMARY KEY(transaction_id),
FOREIGN KEY(transaction_id) references Transactions(transaction_id),
FOREIGN KEY(sender_bank_name, sender_account_id) references ExternalAccounts(bank_name, account_id),
FOREIGN KEY(target_account_id) references Account(account_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE ExternalSend(
transaction_id INT NOT NULL,
sender_account_id INT NOT NULL,
receiver_bank_name VARCHAR(50) NOT NULL,
receiver_account_id INT UNSIGNED NOT NULL,
PRIMARY KEY(transaction_id),
FOREIGN KEY(transaction_id) references Transactions(transaction_id),
FOREIGN KEY(receiver_bank_name, receiver_account_id) references ExternalAccounts(bank_name, account_id),
FOREIGN KEY(sender_account_id) references Account(account_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



CREATE TABLE Login_History
(
date_time DATETIME NOT NULL,
customer_id INT NOT NULL,
PRIMARY KEY(date_time, customer_id),
FOREIGN KEY(customer_id) references Customer(customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ============= ADD DUMMY DATA ============
INSERT INTO Customer VALUES
(1001, 'Dhruv','654321', 1),
(1002, 'Andy', 'abcdef', 2),
(1003, 'Tamanna', 'fedcba', 3),
(1004, 'Sam', '123456', 4);

INSERT INTO Account VALUES
(661, 'Savings', 1200.06, 'HKD', 1001),
(662, 'Current', 5000.88, 'USD', 1002),
(663, 'Savings', 400000.21, 'HKD', 1002),
(664, 'Current', 5000.88, 'INR', 1001),
(665, 'Savings', 30000.11, 'HKD', 1003),
(666, 'Current', 3200.11, 'HKD', 1003),
(667, 'Savings', 1000000.11, 'HKD', 1004),
(668, 'Current', 70900.11, 'USD', 1004);

INSERT INTO Transactions (transaction_description, date_n_time, amount) VALUES
('bill', '2015-12-19 14:01:59', 1200),
('Pay for bills', '2015-12-19 14:02:59', 500.25),
('bill', '2015-12-19 14:03:59', 120),
('Pay for bills', '2015-12-19 14:04:59', 500.25),
('Hi', '2016-12-19 14:05:59', 125),
('Hello!', '2016-12-19 14:06:59', 25),
('Hi', '2016-12-19 14:07:59', 156),
('Hello!', '2016-12-19 14:08:59', 25),
('Payment', '2016-12-19 14:09:59', 4500),
('Pay', '2016-12-19 14:10:59', 4000.67),
('Payment', '2016-12-19 14:11:59', 1020),
('Pay', '2016-12-19 14:12:59', 4002.67),
('bill', '2017-05-19 14:13:59', 6600.12),
('bills', '2017-05-19 14:14:59', 6000),
('bill', '2017-05-19 14:15:59', 6500.12),
('bills', '2017-05-19 14:16:59', 2000),
('Pay', '2017-06-20 14:17:59', 12500),
('Payment', '2017-06-20 14:18:59', 12500),
('Pay', '2017-06-20 14:19:59', 112500),
('Payment', '2017-06-20 15:20:59', 12500),
('Hello again', '2018-11-16 15:21:59', 100),
('Salary', '2018-11-16 15:22:59', 1250000.02),
('Hello again', '2018-11-16 15:23:59', 990),
('Salary', '2018-11-16 15:24:39', 124000.02),
('Ticket', '2018-11-16 15:25:59', 605),
('Tickets', '2018-11-16 15:26:59', 60),
('Ticket', '2018-11-16 15:27:59', 6025),
('Tickets', '2018-11-16 15:28:39', 2520),
('Car', '2019-03-16 15:29:59', 203),
('Taxi', '2019-03-16 15:30:59', 20),
('Car', '2019-03-16 15:31:59', 1203.41),
('Taxi', '2019-03-16 15:32:59', 9540),
("Thank you for your help!!! Here's 20HKD", '2020-03-16 15:33:59', 20),
("Thank you for your help!!! Here's 60USD", '2020-03-16 15:34:59', 420),
("Thank you for your help!!! Here's 5000HKD", '2020-03-16 15:35:59', 5000),
("Thank you for your help!!! Here's 50USD", '2020-03-16 15:36:59', 350),
('Pay for bills', '2021-03-16 15:37:59', 35.22),
('Pay for bills', '2021-03-16 15:38:59', 35),
('Pay for bills', '2021-03-16 15:39:59', 352.22),
('Pay for bills', '2021-03-16 15:40:59', 1235);

INSERT INTO Internal_Trans VALUES
(2, 661, 662),
(6, 661, 663),
(10, 661, 665),
(14, 661, 663),
(18, 661, 666),
(22, 661, 662),
(26, 661, 664),
(30, 661, 663),
(34, 661, 665),
(38, 661, 662),
(1, 662, 661),
(5, 663, 661),
(9, 664, 661),
(13, 662, 661),
(17, 663, 661),
(21, 666, 661),
(25, 663, 661),
(29, 662, 661),
(33, 662, 661),
(37, 665, 661);

INSERT INTO ExternalAccounts VALUES
('Bank of Delta', 55112),
('Bank of Delta', 55331),
('Bank of Sigma', 3212),
('Bank of Sigma', 3206);



INSERT INTO ExternalReceive VALUES
(4, 661, 'Bank of Delta', 55112),
(8, 661, 'Bank of Sigma', 3212),
(12, 661, 'Bank of Sigma', 3206),
(16, 661, 'Bank of Delta', 55112),
(20, 661, 'Bank of Sigma', 3212),
(24, 661, 'Bank of Delta', 55112),
(28, 661, 'Bank of Sigma', 3206),
(32, 661, 'Bank of Delta', 55331),
(36, 661, 'Bank of Sigma', 3212),
(40, 661, 'Bank of Delta', 55331);

INSERT INTO ExternalSend VALUES
(3, 661, 'Bank of Sigma', 3206),
(7, 661, 'Bank of Sigma', 3212),
(11, 661, 'Bank of Delta', 55331),
(15, 661, 'Bank of Sigma', 3206),
(19, 661, 'Bank of Delta', 55112),
(23, 661, 'Bank of Sigma', 3206),
(27, 661, 'Bank of Sigma', 3212),
(31, 661, 'Bank of Delta', 55112),
(35, 661, 'Bank of Delta', 55331),
(39, 661, 'Bank of Sigma', 3206);

INSERT INTO Login_History VALUES
('2019-10-07 21:58:52', 1001),
('2018-12-31 16:13:31', 1001),
('2017-11-20 14:42:04', 1001),
('2016-12-31 13:33:21', 1001);

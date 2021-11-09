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
DROP TABLE IF EXISTS `customer`;
DROP TABLE IF EXISTS `account`;
DROP TABLE IF EXISTS `internal_trans`;
DROP TABLE IF EXISTS `external_trans`;
DROP TABLE IF EXISTS `externalaccounts`;
DROP TABLE IF EXISTS `externalreceive`;
DROP TABLE IF EXISTS `externalsend`;
DROP TABLE IF EXISTS `login_history`;
DROP TABLE IF EXISTS `transactions`;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;





-- New Additions


-- Setting up Tables
CREATE TABLE customer
(
customer_id INT NOT NULL,
customer_name VARCHAR(50) NOT NULL,
password VARCHAR(16) NOT NULL,
face_id INT NOT NULL,
PRIMARY KEY(customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE account
(
account_id INT NOT NULL,
account_type VARCHAR(7) NOT NULL,
balance FLOAT SIGNED NOT NULL, # Must be HKD, even if currency different
currency VARCHAR(3) NOT NULL,
customer_id INT NOT NULL,
PRIMARY KEY(account_id),
FOREIGN KEY(customer_id) REFERENCES Customer(customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE transactions
(
transaction_id INT NOT NULL AUTO_INCREMENT,
PRIMARY KEY(transaction_id)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE internal_trans
(
transaction_id INT NOT NULL,
target_acc INT NOT NULL,
transaction_description VARCHAR(50),
date_n_time DATETIME NOT NULL,
amount FLOAT UNSIGNED NOT NULL, # Change to UNSIGNED
account_id INT NOT NULL,
PRIMARY KEY(transaction_id),
FOREIGN KEY(transaction_id) references transactions(transaction_id),
FOREIGN KEY(account_id) references account(account_id),
FOREIGN KEY(target_acc) references account(account_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE externalaccounts(
bank_name VARCHAR(50) NOT NULL,
account_id INT UNSIGNED NOT NULL,
PRIMARY KEY(bank_name, account_id)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE externalreceive(
transaction_id INT NOT NULL,
transaction_description VARCHAR(50),
date_n_time DATETIME NOT NULL,
amount FLOAT UNSIGNED NOT NULL,
target_account_id INT NOT NULL,
sender_bank_name VARCHAR(50) NOT NULL,
sender_account_id INT UNSIGNED NOT NULL,
PRIMARY KEY(transaction_id),
FOREIGN KEY(transaction_id) references transactions(transaction_id),
FOREIGN KEY(sender_bank_name, sender_account_id) references ExternalAccounts(bank_name, account_id),
FOREIGN KEY(target_account_id) references Account(account_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE externalsend(
transaction_id INT NOT NULL,
transaction_description VARCHAR(50),
date_n_time DATETIME NOT NULL,
amount FLOAT UNSIGNED NOT NULL,
sender_account_id INT NOT NULL,
receiver_bank_name VARCHAR(50) NOT NULL,
receiver_account_id INT UNSIGNED NOT NULL,
PRIMARY KEY(transaction_id),
FOREIGN KEY(transaction_id) references transactions(transaction_id),
FOREIGN KEY(receiver_bank_name, receiver_account_id) references ExternalAccounts(bank_name, account_id),
FOREIGN KEY(sender_account_id) references Account(account_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



CREATE TABLE login_history
(
date_time DATETIME NOT NULL,
customer_id INT NOT NULL,
PRIMARY KEY(date_time, customer_id),
FOREIGN KEY(customer_id) references Customer(customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ============= ADD DUMMY DATA ============
INSERT INTO customer VALUES
(1001, 'Tamanna','654321', 1),
(1002, 'Andy', 'abcdef', 2),
(1003, 'Dhruv', 'fedcba', 3),
(1004, 'Sam', '123456', 4);

INSERT INTO account VALUES
(661, 'Savings', 1200.06, 'HKD', 1001),
(662, 'Current', 5000.88, 'USD', 1002),
(663, 'Savings', 400000.21, 'HKD', 1002),
(664, 'Current', 5000.88, 'INR', 1001),
(665, 'Savings', 30000.11, 'HKD', 1003),
(666, 'Current', 3200.11, 'HKD', 1003),
(667, 'Savings', 1000000.11, 'HKD', 1004),
(668, 'Current', 70900.11, 'USD', 1004);

INSERT INTO transactions VALUES (),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),(),();

INSERT INTO internal_trans VALUES
(2, 661, 'Pay for bills', '2015-12-19 14:29:59', 500.25, 662),
(6, 661, 'Hello!', '2016-12-19 14:29:59', 25, 663),
(10, 661, 'Pay', '2016-12-19 14:39:59', 4000.67, 665),
(14, 661, 'bills', '2017-05-19 14:29:59', 6000, 663),
(18, 661, 'Payment', '2017-06-20 14:29:59', 12500, 666),
(22, 661, 'Salary', '2018-11-16 15:29:59', 1250000.02, 662),
(26, 661, 'Tickets', '2018-11-16 15:29:59', 60, 664),
(30, 661, 'Taxi', '2019-03-16 15:29:59', 20, 663),
(34, 661, "Thank you for your help!!! Here's 60USD", '2020-03-16 15:29:59', 420, 665),
(38, 661, 'Pay for bills', '2021-03-16 15:29:59', 35, 662),
(1, 662, 'bill', '2015-12-19 14:24:59', 1200, 661),
(5, 663, 'Hi', '2016-12-19 14:24:59', 125, 661),
(9, 664, 'Payment', '2016-12-19 14:25:59', 4500, 661),
(13, 662, 'bill', '2017-05-19 14:24:59', 6600.12, 661),
(17, 663, 'Pay', '2017-06-20 14:24:59', 12500, 661),
(21, 666, 'Hello again', '2018-11-16 15:24:59', 100, 661),
(25, 663, 'Ticket', '2018-11-16 15:24:59', 605, 661),
(29, 662, 'Car', '2019-03-16 15:24:59', 203, 661),
(33, 662, "Thank you for your help!!! Here's 20HKD", '2020-03-16 15:24:59', 20, 661),
(37, 665, 'Pay for bills', '2021-03-16 15:24:59', 35.22, 661);

INSERT INTO externalaccounts VALUES
('Bank of Delta', 55112),
('Bank of Delta', 55331),
('Bank of Sigma', 3212),
('Bank of Sigma', 3206);



INSERT INTO externalreceive VALUES
(4, 'Pay for bills', '2015-12-19 14:39:59', 500.25, 661, 'Bank of Delta', 55112),
(8, 'Hello!', '2016-12-19 14:29:59', 25, 661, 'Bank of Sigma', 3212),
(12, 'Pay', '2016-12-19 14:39:59', 4002.67, 661, 'Bank of Sigma', 3206),
(16, 'bills', '2017-05-19 14:39:59', 2000, 661, 'Bank of Delta', 55112),
(20, 'Payment', '2017-06-20 14:39:59', 12500, 661, 'Bank of Sigma', 3212),
(24, 'Salary', '2018-11-16 15:39:39', 124000.02, 661, 'Bank of Delta', 55112),
(28, 'Tickets', '2018-11-16 15:39:39', 2520, 661, 'Bank of Sigma', 3206),
(32, 'Taxi', '2019-03-16 15:39:59', 9540, 661, 'Bank of Delta', 55331),
(36, "Thank you for your help!!! Here's 50USD", '2020-03-16 15:39:59', 350, 661, 'Bank of Sigma', 3212),
(40, 'Pay for bills', '2021-03-16 15:39:59', 1235, 661, 'Bank of Delta', 55331);

INSERT INTO externalsend VALUES
(3, 'bill', '2015-12-19 14:25:59', 120, 661, 'Bank of Sigma', 3206),
(7, 'Hi', '2016-12-19 14:24:59', 156, 661, 'Bank of Sigma', 3212),
(11, 'Payment', '2016-12-19 14:25:59', 1020, 661, 'Bank of Delta', 55331),
(15, 'bill', '2017-05-19 14:25:59', 6500.12, 661, 'Bank of Sigma', 3206),
(19, 'Pay', '2017-06-20 14:25:59', 112500, 661, 'Bank of Delta', 55112),
(23, 'Hello again', '2018-11-16 15:25:59', 990, 661, 'Bank of Sigma', 3206),
(27, 'Ticket', '2018-11-16 15:25:59', 6025, 661, 'Bank of Sigma', 3212),
(31, 'Car', '2019-03-16 15:25:59', 1203.41, 661, 'Bank of Delta', 55112),
(35, "Thank you for your help!!! Here's 5000HKD", '2020-03-16 15:25:59', 5000, 661, 'Bank of Delta', 55331),
(39, 'Pay for bills', '2021-03-16 15:25:59', 352.22, 661, 'Bank of Sigma', 3206);

INSERT INTO login_history VALUES
('2019-10-07 21:58:52', 1001),
('2018-12-31 16:13:31', 1001),
('2017-11-20 14:42:04', 1001),
('2016-12-31 13:33:21', 1001);



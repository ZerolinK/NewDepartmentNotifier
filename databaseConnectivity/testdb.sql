-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Dec 01, 2014 at 11:38 PM
-- Server version: 5.6.17
-- PHP Version: 5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `testdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `report`
--

CREATE TABLE IF NOT EXISTS `report` (
  `Report_ID` int(11) NOT NULL AUTO_INCREMENT,
  `User_ID` int(11) NOT NULL,
  `Summary` text NOT NULL,
  `Description` text NOT NULL,
  `Votes` int(11) NOT NULL,
  `Is_Resolved` tinyint(1) NOT NULL,
  `Date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Report_ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=40 ;

--
-- Dumping data for table `report`
--

INSERT INTO `report` (`Report_ID`, `User_ID`, `Summary`, `Description`, `Votes`, `Is_Resolved`, `Date`) VALUES
(1, 6003090, 'Computer Login', 'I can''t log into my computer! Other people have tried to log in also, but they can''t log in either!', 11, 0, '2014-11-30 13:54:49'),
(2, 6003090, 'Computer Logout', 'I was able to log into my computer, but now it hangs on the logout screen and wont log out at all.', 2, 0, '2014-11-30 13:54:49'),
(3, 6003090, 'Programming', 'I dont know how to do this! Can someone please help me!', 7, 0, '2014-11-30 13:54:49'),
(36, 6003090, 'No food', 'We''re starving. There''s absolutely no food in the vending machines!', 0, 0, '2014-11-30 18:22:08'),
(37, 6003090, 'Bike Pump', 'The bike pump near the computer science parking lot is broken. Can someone fix it soon please?', 3, 0, '2014-11-30 18:22:34'),
(38, 6003090, 'Broken Mac', 'Mac desktop in lab is broken. But no one really cares.', 1, 1, '2014-11-30 18:23:04'),
(39, 6003090, 'Broken window', 'Window broken in JCCL. Please fix this. It is unsightly.', 3, 1, '2014-11-30 18:24:05');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `ID` int(11) NOT NULL,
  `FName` text NOT NULL,
  `LName` text NOT NULL,
  `Email` varchar(16) NOT NULL,
  `Pass` text NOT NULL,
  `Role` tinyint(1) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`ID`, `FName`, `LName`, `Email`, `Pass`, `Role`) VALUES
(2995664, 'Marc', 'Roger', 'mroge009@fiu.edu', 'pbkdf2:sha1:1000$dViNo6Ky$a8830a16e96bb1ad786d0102994c76d7572daa4a', 1),
(3654955, 'Steve', 'Ignetti', 'signe001@fiu.edu', 'pbkdf2:sha1:1000$rY80gllE$74ea69c666d259c4f0a9baa23488871b411996d0', 0),
(6003090, 'David', 'Vizcaino', 'dvizc002@fiu.edu', 'pbkdf2:sha1:1000$2AayyrjX$a0b9194b7fe86f7e60fdf1118d626fd51c50b98f', 0);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

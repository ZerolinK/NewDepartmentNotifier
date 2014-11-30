-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Nov 30, 2014 at 10:58 PM
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=28 ;

--
-- Dumping data for table `report`
--

INSERT INTO `report` (`Report_ID`, `User_ID`, `Summary`, `Description`, `Votes`, `Is_Resolved`, `Date`) VALUES
(1, 6003090, 'Computer Login', 'I cant log into my computer!', 0, 0, '2014-11-30 13:54:49'),
(2, 6003090, 'Computer Logout', 'I cant log out of my computer!', 0, 0, '2014-11-30 13:54:49'),
(3, 6003090, 'Programming', 'I dont know how to do this!', 0, 0, '2014-11-30 13:54:49');

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
(1586390, 'Daniel', 'Gonzalez', 'dgonz023@fiu.edu', 'dpnet', 0),
(2995664, 'Marc', 'Roger', 'mroge009@fiu.edu', 'pbkdf2:sha1:1000$dViNo6Ky$a8830a16e96bb1ad786d0102994c76d7572daa4a', 1),
(6003090, 'David', 'Vizcaino', 'dvizc002@fiu.edu', 'pbkdf2:sha1:1000$2AayyrjX$a0b9194b7fe86f7e60fdf1118d626fd51c50b98f', 0);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

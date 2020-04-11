-- phpMyAdmin SQL Dump
-- version 4.8.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 11, 2020 at 03:51 PM
-- Server version: 10.1.32-MariaDB
-- PHP Version: 5.6.36

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `learn`
--

-- --------------------------------------------------------

--
-- Table structure for table `articles`
--

CREATE TABLE `articles` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `author` varchar(100) NOT NULL,
  `body` text NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `comment_count` int(11) NOT NULL DEFAULT '0',
  `like_count` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `articles`
--

INSERT INTO `articles` (`id`, `title`, `author`, `body`, `date`, `comment_count`, `like_count`) VALUES
(2, 'C++ is powerfull and oop.', 'ac_arpan', '<p>C++ is a object oriented language.</p>\r\n', '2019-11-16 16:11:18', 3, 1),
(3, 'This is rayan\'s first post', 'rk_rayan', 'Rayan just want to wish everyone Goodnight!\r\n', '2019-11-16 16:34:33', 1, 0),
(4, 'Let\'s learn about Angular.', 'ac_arpan', '<p>Angular is a very widely used front-end web development framework.</p>\r\n', '2019-11-17 07:58:02', 3, 1),
(5, 'Machine Learning is trendy', 'geeky_blood', '<p>ML or Machine Learning is a great field of interest for most of modern day&#39;s computer engineer.</p>\r\n', '2019-11-17 16:27:26', 5, 3),
(6, 'Paramedical is great field.', 'rust_puja', '<p>I am an working professional in this field.</p>\r\n', '2019-11-24 07:43:18', 2, 0),
(7, 'my second post', 'rk_rayan', 'We should learn about express.js now a days', '2019-12-16 13:55:02', 0, 0),
(8, 'Pubg Tricks', 'pubg_freak', 'We can spray with m416 using 6x.', '2019-12-16 13:58:25', 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `comments`
--

CREATE TABLE `comments` (
  `id` int(11) NOT NULL,
  `author` varchar(50) NOT NULL,
  `body` varchar(255) NOT NULL,
  `article_id` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `comments`
--

INSERT INTO `comments` (`id`, `author`, `body`, `article_id`, `date`) VALUES
(1, 'ac_arpan', 'Great! The article is informative. Thanks buddy!', 5, '2019-11-19 08:02:49'),
(2, 'rk_rayan', 'I think, this is over-hyped though!', 5, '2019-11-19 08:07:46'),
(3, 'rk_rayan', 'Yes! this is my favorite language  ', 2, '2019-11-19 08:09:51'),
(4, 'rk_rayan', 'One of the best front-end framework.', 4, '2019-11-19 08:11:38'),
(5, 'rk_rayan', 'Test Comment', 3, '2019-11-19 08:14:02'),
(6, 'geeky_blood', 'I also want to learn it!', 4, '2019-11-19 08:16:47'),
(7, 'geeky_blood', 'AI is quite close to it.', 5, '2019-11-19 08:40:12'),
(8, 'geeky_blood', 'STL is one of it\'s greatest libraries.', 2, '2019-11-19 08:51:25'),
(9, 'rust_puja', 'I also want to learn it. It is looking interesting.', 2, '2019-11-24 07:32:54'),
(10, 'ac_arpan', 'I see!', 6, '2019-11-24 07:44:12'),
(11, 'ac_arpan', 'Great! The article is informative. Thanks buddy!', 5, '2019-11-24 07:45:48'),
(13, 'rk_rayan', 'This is a great field!', 6, '2019-11-24 07:51:27'),
(14, 'pubg_freak', 'Ki kaka valo to!', 4, '2019-11-25 13:21:47'),
(15, 'rk_rayan', 'i just want to add another comment', 5, '2019-12-16 13:56:02');

-- --------------------------------------------------------

--
-- Table structure for table `likes`
--

CREATE TABLE `likes` (
  `id` int(11) NOT NULL,
  `article_id` int(11) NOT NULL,
  `liker_username` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `likes`
--

INSERT INTO `likes` (`id`, `article_id`, `liker_username`) VALUES
(10, 2, 'ac_arpan'),
(16, 5, 'ac_arpan'),
(18, 5, 'pubg_freak'),
(19, 5, 'rk_rayan'),
(20, 4, 'pubg_freak');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `sno` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `propic` varchar(250) NOT NULL DEFAULT 'none.jpg'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`sno`, `name`, `username`, `password`, `email`, `date`, `propic`) VALUES
(2, 'Arpan Chowdhury', 'ac_arpan', '$5$rounds=535000$bgeM70YMVMwr5gq2$2OlyBbvxLf7ErgDZK2fOgw63eUSYemedvj0Zsx4EL65', 'arpanchowdhury050@gmail.com', '2019-11-15 15:51:41', '20180101_001704.jpg'),
(3, 'Rayan Chakrabarty', 'rk_rayan', '$5$rounds=535000$VO0SSl4ZfxX/ASQ9$9mHJc2yrHvlmMFy4rbFJ997v/vVsL/UGJaPAJ296lz6', 'rayan@gmail.com', '2019-11-16 16:33:09', '20180526_130157.jpg'),
(4, 'Rittwick Bhabak', 'geeky_blood', '$5$rounds=535000$CO8UpkY3aQ.e.A/O$4M15Sn.4EA7qYT.DJyxP.rVn4yCwJRJFzHX8ikpb1O/', 'physicscricket@gmail.com', '2019-11-17 16:24:58', 'IMG_20190105_164354.jpg'),
(5, 'Sujoy Ghosh', 'coding_maestro', '$5$rounds=535000$uWtOmWgmQ4UQ0x9W$fiInSUmVN/mo66Ce4Hu4z8Z0hMyMjP8X7yr7NKslU14', 'sujoy@gmail.com', '2019-11-17 16:30:02', 'none.jpg'),
(6, 'Ranajit Dutta', 'pubg_freak', '$5$rounds=535000$5RAqEK8vaBCqSijN$mT3/2EPDOal2Z9Uqm0uLe.Y9UR.V2YFZURyuX9gtGp9', 'roni@gmail.com', '2019-11-17 16:31:00', '20180526_151542.jpg'),
(8, 'Arpita Chowdhury', 'rust_puja', '$5$rounds=535000$XJK8uMBhutMWycLd$J61s5qu.SFRIWdmkPeENX0x.SBd5Dzq289wlCHfWoN8', 'puja@gmail.com', '2019-11-24 07:29:52', '20180526_151542.jpg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `articles`
--
ALTER TABLE `articles`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `likes`
--
ALTER TABLE `likes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`sno`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `articles`
--
ALTER TABLE `articles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `comments`
--
ALTER TABLE `comments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `likes`
--
ALTER TABLE `likes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

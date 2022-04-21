/*
SQLyog Community v13.1.7 (64 bit)
MySQL - 5.6.12-log : Database - college_web
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`college_web` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `college_web`;

/*Table structure for table `attendance` */

DROP TABLE IF EXISTS `attendance`;

CREATE TABLE `attendance` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `slid` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `hour` int(11) DEFAULT NULL,
  PRIMARY KEY (`aid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `attendance` */

insert  into `attendance`(`aid`,`slid`,`date`,`hour`) values 
(1,5,'2022-03-04',1);

/*Table structure for table `chat` */

DROP TABLE IF EXISTS `chat`;

CREATE TABLE `chat` (
  `chat_id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime DEFAULT NULL,
  `from_id` int(11) DEFAULT NULL,
  `to_id` int(11) DEFAULT NULL,
  `message` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`chat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `chat` */

insert  into `chat`(`chat_id`,`date`,`from_id`,`to_id`,`message`) values 
(1,'2022-03-04 06:25:22',5,3,'kshkfhsdf'),
(2,'2022-03-04 06:25:27',5,3,'kfhkhsdhf'),
(3,'2022-03-04 07:00:49',6,5,'khfkjsdfs');

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `complint` varchar(200) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `reply` varchar(150) DEFAULT NULL,
  `lid` int(11) DEFAULT NULL,
  `type` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`cid`,`complint`,`date`,`status`,`reply`,`lid`,`type`) values 
(1,'kjhjhdfjsdhzf','2022-03-04','pending','pending',3,NULL),
(3,'      hjkhj jkkhkhj kjkh khjhjj kjjjj ','2022-03-04','pending','pending',8,'student');

/*Table structure for table `course` */

DROP TABLE IF EXISTS `course`;

CREATE TABLE `course` (
  `course_id` int(11) NOT NULL AUTO_INCREMENT,
  `did` int(11) DEFAULT NULL,
  `course_code` varchar(100) DEFAULT NULL,
  `course_name` varchar(100) DEFAULT NULL,
  `sem` int(11) DEFAULT NULL,
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `course` */

insert  into `course`(`course_id`,`did`,`course_code`,`course_name`,`sem`) values 
(1,1,'BSC EL','BSC ELECTRONICS',6);

/*Table structure for table `department` */

DROP TABLE IF EXISTS `department`;

CREATE TABLE `department` (
  `did` int(11) NOT NULL AUTO_INCREMENT,
  `department_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`did`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `department` */

insert  into `department`(`did`,`department_name`) values 
(1,'BSC');

/*Table structure for table `fee` */

DROP TABLE IF EXISTS `fee`;

CREATE TABLE `fee` (
  `fid` int(11) NOT NULL AUTO_INCREMENT,
  `cid` int(11) DEFAULT NULL,
  `sem` int(11) DEFAULT NULL,
  `fee` varchar(10) DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `late_date` date DEFAULT NULL,
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `fee` */

insert  into `fee`(`fid`,`cid`,`sem`,`fee`,`due_date`,`late_date`) values 
(1,1,1,'1500','2022-12-31','2023-12-31');

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `fid` int(11) NOT NULL AUTO_INCREMENT,
  `lid` int(11) DEFAULT NULL,
  `feedback` varchar(150) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `feedback` */

insert  into `feedback`(`fid`,`lid`,`feedback`,`date`,`type`) values 
(1,5,'jhskjfashas','2022-03-04','student'),
(2,3,'kdsfksdhfksd','2022-03-04',''),
(3,3,'fkjsdhkjfdsh','2022-03-04',''),
(4,3,'fkjsdhkjfdsh','2022-03-04',''),
(5,3,'fkjsdhkjfdsh','2022-03-04',''),
(6,3,'jjfkjkkjdhf khkh jhkjhk ','2022-03-04',''),
(7,3,'hjggh hkh kjh','2022-03-04',''),
(8,3,'kkhkjh','2022-03-04','');

/*Table structure for table `hod_assignment` */

DROP TABLE IF EXISTS `hod_assignment`;

CREATE TABLE `hod_assignment` (
  `hid` int(11) NOT NULL AUTO_INCREMENT,
  `did` int(11) DEFAULT NULL,
  `staff_lid` int(11) DEFAULT NULL,
  PRIMARY KEY (`hid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `hod_assignment` */

insert  into `hod_assignment`(`hid`,`did`,`staff_lid`) values 
(1,1,3);

/*Table structure for table `internal_mark` */

DROP TABLE IF EXISTS `internal_mark`;

CREATE TABLE `internal_mark` (
  `mid` int(11) NOT NULL AUTO_INCREMENT,
  `slid` int(11) DEFAULT NULL,
  `subid` int(11) DEFAULT NULL,
  `mark` int(11) DEFAULT NULL,
  PRIMARY KEY (`mid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `internal_mark` */

insert  into `internal_mark`(`mid`,`slid`,`subid`,`mark`) values 
(1,5,1,15);

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `lid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `stlid` int(11) DEFAULT NULL COMMENT 'for parent to login',
  PRIMARY KEY (`lid`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`lid`,`username`,`password`,`type`,`stlid`) values 
(1,'admin@gmail.com','admin','admin',NULL),
(2,'linil@gmail.com','1','subadmin',NULL),
(3,'tlikhil@gmail.com','11','hod',NULL),
(4,'ravi@gmail.com','3330','student',NULL),
(5,'ravi@gmail.com','1','student',NULL),
(6,'sujatah@gmail.com','1','staff',NULL),
(7,'mamtha@gmail.com','1','student',NULL),
(8,'bindya@gmail.com','1','student',NULL),
(9,'kavi@gmail.com','100','student',NULL),
(10,'kavi@gmail.com','100','parent',9),
(11,'shyni@gmail.com','5245','student',NULL),
(12,'shyni@gmail.com','5445','parent',11);

/*Table structure for table `notes` */

DROP TABLE IF EXISTS `notes`;

CREATE TABLE `notes` (
  `note_id` int(11) NOT NULL AUTO_INCREMENT,
  `sub_id` int(11) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  `notes` varchar(250) DEFAULT NULL,
  `description` varchar(250) DEFAULT NULL,
  `staff_lid` int(11) DEFAULT NULL,
  PRIMARY KEY (`note_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `notes` */

insert  into `notes`(`note_id`,`sub_id`,`course_id`,`notes`,`description`,`staff_lid`) values 
(1,1,1,'/static/notes/2022-03-04-Mar-48-57.pdf','dfsdfsd',6);

/*Table structure for table `notification` */

DROP TABLE IF EXISTS `notification`;

CREATE TABLE `notification` (
  `nid` int(11) NOT NULL AUTO_INCREMENT,
  `lid` int(11) DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `content` varchar(250) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`nid`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

/*Data for the table `notification` */

insert  into `notification`(`nid`,`lid`,`title`,`content`,`date`) values 
(1,2,'jkfdskljj','KLDFKJFJKLDS','2022-03-03'),
(2,3,',dhfh','hkjhjh','2022-03-04'),
(3,3,'kashhsdkjfh','hkjdshhskjdf','2022-03-04'),
(6,2,'ksjfkjdsl','jlkjkjfkjk','2022-03-04');

/*Table structure for table `punishment` */

DROP TABLE IF EXISTS `punishment`;

CREATE TABLE `punishment` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `slid` int(11) DEFAULT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `reason` varchar(50) DEFAULT NULL,
  `punishment` varchar(100) DEFAULT NULL,
  `from_date` date DEFAULT NULL,
  `to_date` date DEFAULT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `punishment` */

insert  into `punishment`(`pid`,`slid`,`photo`,`reason`,`punishment`,`from_date`,`to_date`) values 
(1,2,'/static/punishment/2022-03-04-Mar-27-53.jpg','hfjkdhfkhjsdhf','khfkjsdhfjksdhfhsd','2022-03-11','2022-03-25');

/*Table structure for table `question` */

DROP TABLE IF EXISTS `question`;

CREATE TABLE `question` (
  `qid` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) DEFAULT NULL,
  `questions` varchar(500) DEFAULT NULL,
  `reply` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`qid`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `question` */

insert  into `question`(`qid`,`userid`,`questions`,`reply`,`status`,`date`) values 
(1,3,'shit','pending','pending','2021-12-23'),
(2,3,'kooi','done','replied','2021-12-26'),
(3,3,'guys','what','pending','2021-12-28'),
(4,3,'going','free','pending','2021-12-30');

/*Table structure for table `research` */

DROP TABLE IF EXISTS `research`;

CREATE TABLE `research` (
  `doctorid` int(11) DEFAULT NULL,
  `researchid` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(500) DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `content` varchar(500) DEFAULT NULL,
  `picture` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`researchid`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

/*Data for the table `research` */

insert  into `research`(`doctorid`,`researchid`,`description`,`title`,`content`,`picture`) values 
(NULL,9,'gfbz','vsCXV','xcVbCF\"\"\"\"','/static/flowers.jpg'),
(NULL,7,'hejtm','trejmj','afesgrhd\"\"\"','/static/20211229_122748.230720.jpg');

/*Table structure for table `staff` */

DROP TABLE IF EXISTS `staff`;

CREATE TABLE `staff` (
  `staff_id` int(11) NOT NULL AUTO_INCREMENT,
  `staff_name` varchar(50) DEFAULT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `photo` varchar(150) DEFAULT NULL,
  `qualification` varchar(100) DEFAULT NULL,
  `experience` varchar(100) DEFAULT NULL,
  `contact` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `staff_lid` int(11) DEFAULT NULL,
  `did` int(11) DEFAULT NULL,
  PRIMARY KEY (`staff_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `staff` */

insert  into `staff`(`staff_id`,`staff_name`,`gender`,`dob`,`photo`,`qualification`,`experience`,`contact`,`email`,`staff_lid`,`did`) values 
(1,'Likhil','male','2022-03-05','/static/staff/2022-03-04-Mar-49-45.jpg','Btech','10 years in CAPEC','7854125487','tlikhil@gmail.com',3,1),
(2,'Sujatha','female','2008-11-30','/static/staff/2022-03-04-Mar-28-59.jpg','Med','10 years','7845126589','sujatah@gmail.com',6,1);

/*Table structure for table `student` */

DROP TABLE IF EXISTS `student`;

CREATE TABLE `student` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `sname` varchar(50) DEFAULT NULL,
  `cid` int(11) DEFAULT NULL,
  `sem` int(11) DEFAULT NULL,
  `photo` varchar(150) DEFAULT NULL,
  `admission_no` varchar(30) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `contact` varchar(16) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `slid` int(11) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `student` */

insert  into `student`(`sid`,`sname`,`cid`,`sem`,`photo`,`admission_no`,`dob`,`contact`,`email`,`slid`,`gender`) values 
(2,'Bindya',1,1,'/static/student/2022-03-04-Mar-27-01.jpg','21547854','2000-09-18','788945214587','bindya@gmail.com',8,'female'),
(3,'Kavi',1,1,'/static/student/2022-03-04-Mar-03-08.jpg','457845','2022-12-31','7854877878','kavi@gmail.com',9,'male'),
(4,'Shyni',1,1,'/static/student/2022-03-04-Mar-10-09.jpg','78788778','2022-12-31','7845784578','shyni@gmail.com',11,'female');

/*Table structure for table `subadmin` */

DROP TABLE IF EXISTS `subadmin`;

CREATE TABLE `subadmin` (
  `subadmin_id` int(11) NOT NULL AUTO_INCREMENT,
  `sublid` int(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `designation` varchar(100) DEFAULT NULL,
  `photo` varchar(200) DEFAULT NULL,
  `gender` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`subadmin_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `subadmin` */

insert  into `subadmin`(`subadmin_id`,`sublid`,`name`,`phone`,`email`,`designation`,`photo`,`gender`) values 
(1,2,'LINIL C','9946520656','linil@gmail.com','Test','/static/subadmin/2022-03-03-Mar-49-14.jpg','male');

/*Table structure for table `subject` */

DROP TABLE IF EXISTS `subject`;

CREATE TABLE `subject` (
  `sub_id` int(11) NOT NULL AUTO_INCREMENT,
  `cid` int(11) DEFAULT NULL,
  `sem` int(11) DEFAULT NULL,
  `sub_code` varchar(100) DEFAULT NULL,
  `sub_name` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`sub_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `subject` */

insert  into `subject`(`sub_id`,`cid`,`sem`,`sub_code`,`sub_name`) values 
(1,1,1,'kk','kkkkkk');

/*Table structure for table `subject_allocation` */

DROP TABLE IF EXISTS `subject_allocation`;

CREATE TABLE `subject_allocation` (
  `alloc_id` int(11) NOT NULL AUTO_INCREMENT,
  `sub_id` int(11) DEFAULT NULL,
  `staff_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`alloc_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `subject_allocation` */

insert  into `subject_allocation`(`alloc_id`,`sub_id`,`staff_id`) values 
(1,1,1),
(2,0,0),
(3,1,2);

/*Table structure for table `time_table` */

DROP TABLE IF EXISTS `time_table`;

CREATE TABLE `time_table` (
  `tid` int(11) NOT NULL AUTO_INCREMENT,
  `sub_id` int(11) DEFAULT NULL,
  `day` varchar(10) DEFAULT NULL,
  `hour` varchar(10) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  `sem` int(11) DEFAULT NULL,
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `time_table` */

insert  into `time_table`(`tid`,`sub_id`,`day`,`hour`,`course_id`,`sem`) values 
(1,1,'sunday','1',1,1);

/*Table structure for table `tips` */

DROP TABLE IF EXISTS `tips`;

CREATE TABLE `tips` (
  `tipsid` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(50) DEFAULT NULL,
  `image` varchar(50) DEFAULT NULL,
  `title` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`tipsid`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `tips` */

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `userid` int(11) NOT NULL AUTO_INCREMENT,
  `lid` int(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `phonenumber` int(11) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `photo` varchar(50) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `district` varchar(50) DEFAULT NULL,
  `pin` int(11) DEFAULT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `users` */

insert  into `users`(`userid`,`lid`,`name`,`gender`,`phonenumber`,`email`,`photo`,`place`,`district`,`pin`) values 
(1,3,'shibu','m',13253132,'khgjtrgu','jhfyuhj','fugkh','jhhgbb',1234);

/*Table structure for table `vaccine` */

DROP TABLE IF EXISTS `vaccine`;

CREATE TABLE `vaccine` (
  `vid` int(11) NOT NULL AUTO_INCREMENT,
  `vaccine` varchar(50) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `animal` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`vid`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `vaccine` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

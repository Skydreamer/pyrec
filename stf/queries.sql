create database pyrec_db character set 'utf8';

use pyrec_db;

CREATE TABLE `files` (
		`id` integer not null auto_increment,
		`name` varchar(60) not null,
		`description` text,
		`duration` int not null,
		`path` text not null,
		`hash` char(40),
		`add_time` timestamp,
		primary key(`id`)
		);

CREATE TABLE `parts`(
		`id` integer not null auto_increment,
		`file_id` integer not null,
		`start_time` integer not null,
		`end_time` integer not null,
		`text` text character set 'utf8',
		primary key(`id`),
		constraint `file_id_fk` foreign key (`file_id`) references `files`(`id`)
		);
		

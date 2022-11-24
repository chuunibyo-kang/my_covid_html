CREATE DATABASE covid;

USE covid;

-- 搭建世界疫情历史表，存放累计确诊人数、每日确诊增加人数、
-- 累计疑似人数、每日疑似新增人数、累计治愈人数、治愈新增人数
-- 死亡人数、新增死亡人数
CREATE TABLE history_data(
update_date date NOT NULL,
confirm int(11) DEFAULT NULL,
confirm_add int(11) DEFAULT NULL,
heal int(11) DEFAULT NULL,
heal_add int(11) DEFAULT NULL,
dead int(11) DEFAULT NULL,
dead_add int(11) DEFAULT NULL,
PRIMARY KEY(update_date) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 这是各省疫情表
-- 存放更新时间、省和各地级市的累计确诊人数、新增确诊人数
-- 累计治愈人数、累计死亡人数
CREATE TABLE details_data (
id int(11) NOT NULL AUTO_INCREMENT,
update_date datetime NOT NULL,
province VARCHAR(50) DEFAULT NULL,
city VARCHAR(50) DEFAULT NULL,
confirm int(11) DEFAULT NULL,
confirm_add int(11) DEFAULT NULL,
heal int(11) DEFAULT NULL,
dead int(11) DEFAULT NULL,
PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 这是本土相关的表
-- 存放更新时间、现有确诊、今日新增确诊、现有无症状、今日新增无症状
CREATE TABLE mainland_data(
id int(11) NOT NULL AUTO_INCREMENT,
update_date datetime NOT NULL,
mainland_confirm_now int(11) DEFAULT NULL,
mainland_confirm_add int(11) DEFAULT NULL,
mainland_asymptomatic_now int(11) DEFAULT NULL,
mainland_asymptomatic_add int(11) DEFAULT NULL,
PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




       



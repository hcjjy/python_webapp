-- schema.sql 把sql脚本放到Mysql命令：mysql -u root -p < schema.sql
drop database if exists JC;
create database JC;
use JC;
grant select, insert, update, delete on JC.* to 'root'@'localhost' identified by 'root';

create table Users(
	id varchar(50) not null,
	email varchar(50) not null,
	passwd varchar(50) not null,
	admin bool not null,
	name varchar(50) not null,
	image varchar(500) not null,
	created_at real not null,
	unique key idx_email(email),
	key idx_created_at(created_at), -- similay index索引
	primary key primary_key_name(id)
)engine = innodb default charset = utf8;

create table blogs(
	id varchar(50) not null,
	user_id varchar(50) not null,
	user_name varchar(50) not null,
	user_image varchar(50) not null,
	name varchar(50) not null,
	summary varchar(200) not null,
	content mediumtext not null,
	created_at real not null,
	key idx_created_at(created_at),
	primary key(id)
)engine = innodb default charset = utf8;

create table comments(
	id varchar(50) not null,
	blog_id varchar(50) not null,
	user_id varchar(50) not null,
	user_name varchar(50) not null,
	content mediumtext not null,
	created_at real not null,
	key idx_created_at(created_at),
	primary key(id)
)engine = innodb default charset = utf8;	

















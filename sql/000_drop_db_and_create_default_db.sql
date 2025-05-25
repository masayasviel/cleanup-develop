-- DROP DB
DROP DATABASE IF EXISTS `my_database`;

-- CREATE DEFAULT DB
CREATE DATABASE IF NOT EXISTS `my_database`;
GRANT ALL ON my_database.* TO 'my_user'@'%';

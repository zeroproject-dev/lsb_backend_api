CREATE DATABASE IF NOT EXISTS lsb;
USE lsb;

CREATE TABLE IF NOT EXISTS `T_USER` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `first_name` VARCHAR(255) NOT NULL,
  `second_name` VARCHAR(255),
  `first_surname` VARCHAR(255) NOT NULL,
  `second_surname` VARCHAR(255),
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) DEFAULT NULL,
  `state` ENUM('active', 'inactive') DEFAULT 'active',
  `role_id` INT
);

CREATE TABLE IF NOT EXISTS `T_ROLE` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `description` VARCHAR(255),
  `state` ENUM('active', 'inactive') DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS `T_PERMISSION` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `description` VARCHAR(255),
  `state` ENUM('active', 'inactive') DEFAULT 'active',
  `module_id` INT
);

CREATE TABLE IF NOT EXISTS `T_MODULE` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `description` VARCHAR(255),
  `state` ENUM('active', 'inactive') DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS `T_ROLE_PERMISSION` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `permission_id` INT,
  `role_id` INT
);

CREATE TABLE IF NOT EXISTS `T_WORD` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `word` VARCHAR(255) NOT NULL,
  `state` ENUM('active', 'inactive') DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS `T_WORD_VIDEO` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `word_id` INT,
  `video_id` INT
);

CREATE TABLE IF NOT EXISTS `T_VIDEO` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `path` VARCHAR(255) NOT NULL,
  `preview` VARCHAR(255),
  `points` VARCHAR(255),
  `duration` FLOAT,
  `bucket` VARCHAR(255) NOT NULL,
  `region` VARCHAR(255) NOT NULL,
  `uploaded_by` INT NOT NULL,
  `uploaded_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `state` ENUM('active', 'inactive') DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS `T_AUDIT_LOG` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `entity_name` VARCHAR(255),
  `entity_id` INT,
  `action` ENUM('insert', 'update', 'delete'),
  `changed_columns` VARCHAR(255),
  `changed_data` JSON,
  `timestamp` TIMESTAMP,
  `performed_by` INT
);

ALTER TABLE `T_USER` ADD FOREIGN KEY (`role_id`) REFERENCES `T_ROLE` (`id`);
ALTER TABLE `T_PERMISSION` ADD FOREIGN KEY (`module_id`) REFERENCES `T_MODULE` (`id`);
ALTER TABLE `T_ROLE_PERMISSION` ADD FOREIGN KEY (`permission_id`) REFERENCES `T_PERMISSION` (`id`);
ALTER TABLE `T_ROLE_PERMISSION` ADD FOREIGN KEY (`role_id`) REFERENCES `T_ROLE` (`id`);
ALTER TABLE `T_WORD_VIDEO` ADD FOREIGN KEY (`word_id`) REFERENCES `T_WORD` (`id`);
ALTER TABLE `T_WORD_VIDEO` ADD FOREIGN KEY (`video_id`) REFERENCES `T_VIDEO` (`id`);
ALTER TABLE `T_VIDEO` ADD FOREIGN KEY (`uploaded_by`) REFERENCES `T_USER` (`id`);
ALTER TABLE `T_AUDIT_LOG` ADD FOREIGN KEY (`performed_by`) REFERENCES `T_USER` (`id`);


INSERT IGNORE INTO T_MODULE (id, name, description) VALUES (1, 'usuarios', 'Modulo de gestion de usuarios');
INSERT IGNORE INTO T_MODULE (id, name, description) VALUES (2, 'words', 'Modulo de gestion de palabras');
-- INSERT IGNORE INTO T_MODULE (id, name, description) VALUES (3, 'nn', 'Modulo de gestion de la inteligencia artificial');
INSERT IGNORE INTO T_MODULE (id, name, description) VALUES (4, 'roles', 'Modulo de gestion de roles');

-- usuarios
INSERT IGNORE INTO T_PERMISSION (id, name, description, module_id) VALUES (1, 'Listar usuarios', 'Leer la lista de usuarios', 1);
INSERT IGNORE INTO T_PERMISSION (id, name, description, module_id) VALUES (2, 'Agregar usuario', 'Alta de usuario', 1);
INSERT IGNORE INTO T_PERMISSION (id, name, description, module_id) VALUES (3, 'Eliminar usuario', 'Baja de usuario', 1);
INSERT IGNORE INTO T_PERMISSION (id, name, description, module_id) VALUES (4, 'Modificar usuario', 'Modificar usuario', 1);

-- Permissions to admin
INSERT IGNORE INTO T_ROLE_PERMISSION (id, role_id, permission_id) VALUES (1, 1, 1);
INSERT IGNORE INTO T_ROLE_PERMISSION (id, role_id, permission_id) VALUES (2, 1, 2);
INSERT IGNORE INTO T_ROLE_PERMISSION (id, role_id, permission_id) VALUES (3, 1, 3);
INSERT IGNORE INTO T_ROLE_PERMISSION (id, role_id, permission_id) VALUES (4, 1, 4);

-- videos
INSERT IGNORE INTO T_PERMISSION (id, name, description, module_id) VALUES (5, 'Listar videos', 'Obtener la lista de videos', 2);
INSERT IGNORE INTO T_PERMISSION (id, name, description, module_id) VALUES (6, 'Agregar video', 'Alta de video', 2);
INSERT IGNORE INTO T_PERMISSION (id, name, description, module_id) VALUES (7, 'Eliminar video', 'Baja de video', 2);
INSERT IGNORE INTO T_PERMISSION (id, name, description, module_id) VALUES (8, 'Modificar video', 'Modificar video', 2);

-- permissions to admin
INSERT IGNORE INTO T_ROLE_PERMISSION (id, role_id, permission_id) VALUES (5, 1, 5);
INSERT IGNORE INTO T_ROLE_PERMISSION (id, role_id, permission_id) VALUES (6, 1, 6);
INSERT IGNORE INTO T_ROLE_PERMISSION (id, role_id, permission_id) VALUES (7, 1, 7);
INSERT IGNORE INTO T_ROLE_PERMISSION (id, role_id, permission_id) VALUES (8, 1, 8);

-- roles
INSERT IGNORE INTO T_PERMISSION (id, name, description, module_id) VALUES (9, 'Listar roles', 'Leer la lista de roles', 4);
INSERT IGNORE INTO T_PERMISSION (id, name, description, module_id) VALUES (10, 'Agregar roles', 'Alta de roles', 4);
INSERT IGNORE INTO T_PERMISSION (id, name, description, module_id) VALUES (11, 'Eliminar roles', 'Baja de roles', 4);
INSERT IGNORE INTO T_PERMISSION (id, name, description, module_id) VALUES (12, 'Modificar roles', 'Modificar roles', 4);

-- Permissions to admin
INSERT IGNORE INTO T_ROLE_PERMISSION (id, role_id, permission_id) VALUES (9, 1, 9);
INSERT IGNORE INTO T_ROLE_PERMISSION (id, role_id, permission_id) VALUES (10, 1, 10);
INSERT IGNORE INTO T_ROLE_PERMISSION (id, role_id, permission_id) VALUES (11, 1, 11);
INSERT IGNORE INTO T_ROLE_PERMISSION (id, role_id, permission_id) VALUES (12, 1, 12);


INSERT IGNORE INTO T_WORD (id, word) VALUES (1, 'hola');
INSERT IGNORE INTO T_WORD (id, word) VALUES (2, 'gracias');
INSERT IGNORE INTO T_WORD (id, word) VALUES (3, 'te amo');


INSERT IGNORE INTO T_ROLE (id, name, description) VALUES (1, 'Administrador', 'Rol con la capacidad de interactuar y modificar todos los modulos del sistema');
INSERT IGNORE INTO T_ROLE (id, name, description) VALUES (2, 'Usuario', 'Rol sin ningun permiso');
INSERT IGNORE INTO T_USER (id, first_name, second_name, first_surname, second_surname, email, password, role_id) VALUES (1, 'Admin', 'Admin', 'Admin', 'Admin', 'admin@gmail.com', 'scrypt:32768:8:1$Hq5smcbcyeY5OVFv$1669c0117099265d6b9d0119ec92e3f68087e6242bb047ae0f9f25d0583e1a9bc399fd5b1917d5c1c0bcfa40d64cefae578f3901cbf51d597ac20e1d0a8f2189', 1);

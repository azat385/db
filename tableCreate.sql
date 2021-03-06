CREATE TABLE `rpi_plc` (
	`id` INTEGER PRIMARY KEY AUTOINCREMENT,
	`time` timestamp DEFAULT (datetime('now','localtime')),
	`destination` TEXT,
	`packet_loss` DECIMAL(10,3),
	`min` DECIMAL(10,3),
	`avg` DECIMAL(10,3),
	`max` DECIMAL(10,3),
	`mdev` DECIMAL(10,3)
);

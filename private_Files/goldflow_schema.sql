CREATE DATABASE IF NOT EXISTS `gold_flow`;
USE `gold_flow`;

-- ✅ Drop and Recreate Users Table
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `sso_unique_id` CHAR(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NOT NULL UNIQUE, -- UUID Format
  `first_name` VARCHAR(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NOT NULL,
  `last_name` VARCHAR(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NOT NULL,
  `email` VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NOT NULL UNIQUE, -- Email field
  `password` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NOT NULL, -- Hashed password
  `national_id` VARCHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NOT NULL UNIQUE,
  `phone_number` CHAR(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NOT NULL UNIQUE,
  `card_number` VARCHAR(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci UNIQUE,
  `user_type` TINYINT NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `rial_balance` DECIMAL(24,8) NOT NULL DEFAULT 0, -- ✅ Increased to DECIMAL(24,8)
  `gold_balance` DECIMAL(24,8) NOT NULL DEFAULT 0, -- ✅ Increased to DECIMAL(24,8)
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_persian_ci;


LOCK TABLES `users` WRITE;
INSERT INTO `users` (`sso_unique_id`, `first_name`, `last_name`, `email`, `password`, `phone_number`, `national_id`, `card_number`, `user_type`, `gold_balance`, `rial_balance`) VALUES 
(UUID(), 'gold_vault', 'vault', 'goldvault@example.com', '$2b$12$EXAMPLEHASH', '09123456789', '1234567890', '5011121214122532', 3, 9000000000000.00000000, 9999999900000.00000000),
-- (UUID(), 'hassan', 'Bouzarpour', 'hassan@example.com', '$2b$12$EXAMPLEHASH', '09124100011', '0022140143', '1255561101525360', 4, 90000000.00000000, 5000000.00000000),
(UUID(), 'ali', 'Moradi', 'ali@example.com', '$2b$12$EXAMPLEHASH', '09125550022', '0022140144', '5012251012165432', 4, 50000000.00000000, 3000000.00000000),
(UUID(), 'jasem', 'mamadi', 'jasem@example.com', '$2b$1sd2$EXAMPLEHASH', '09121421516', '0020151262', '5022262026232525', 2, 50000000.00000000, 3000000.00000000),
(UUID(), 'reza', 'Ahmadi', 'reza@example.com', '$2b$12$EXAMPLEHASH', '09127778899', '0022140155', '5966251014122523', 4, 70000000.00000000, 4000000.00000000);
UNLOCK TABLES;



-- ✅ Drop and Recreate Assets Table
DROP TABLE IF EXISTS `assets`;
CREATE TABLE `assets` (
  `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NOT NULL,
  `code` VARCHAR(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NOT NULL UNIQUE,
  `unit_fa` VARCHAR(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NOT NULL,
  `image_path` VARCHAR(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NOT NULL,
  `description` VARCHAR(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NOT NULL,
  `current_price_per_gram` DECIMAL(24,8) NOT NULL, -- ✅ Changed to DECIMAL for precision
  `buy_price` DECIMAL(24,8) NOT NULL, -- ✅ Changed to DECIMAL for precision
  `sell_price` DECIMAL(24,8) NOT NULL, -- ✅ Changed to DECIMAL for precision
  `total_buy_limit` BIGINT NOT NULL,
  `total_sell_limit` BIGINT NOT NULL,
  `daily_buy_limit_per_user` BIGINT NOT NULL,
  `daily_sell_limit_per_user` BIGINT NOT NULL,
  `total_balance` BIGINT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_persian_ci;



LOCK TABLES `assets` WRITE;

INSERT INTO `assets` VALUES 
(1, '18k Gold', 'GOLD', 'گرم', '/static/uploaded_files/gold.png', '18K Gold or 750 Gold.', 65093000.00000000, 23700704.00000000, 23334412.00000000, 600000000000, 400000000000, 600000000000, 400000000000, 1000000000),
(2, 'Iranian Rial', 'IRR', 'ریال', '/static', 'Iranian Rial', 1.00000000, 1.00000000, 1.00000000, 0, 0, 0, 0, 100000000000);
UNLOCK TABLES;


-- ✅ Drop and Recreate Transactions Table
DROP TABLE IF EXISTS `transactions`;
CREATE TABLE `transactions` (
  `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT UNSIGNED NOT NULL,
  `sso_unique_id` CHAR(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NOT NULL, -- UUID Format
  `asset_id` INT UNSIGNED NOT NULL,
  `rial_amount` DECIMAL(24,8) NOT NULL, -- ✅ Changed to DECIMAL for precision
  `gold_amount` DECIMAL(24,8) NOT NULL, -- ✅ Changed to DECIMAL for precision
  `create_datetime` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `shamsi_create_datetime` VARCHAR(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NOT NULL,
  `transaction_type` TINYINT NOT NULL,
  `status` TINYINT NOT NULL,
  `asset_price_at_transaction_time` DECIMAL(24,8) NOT NULL, -- ✅ Changed to DECIMAL for precision
  `description` VARCHAR(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NOT NULL,
  `last_update_datetime` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `buyer_rial_balance` DECIMAL(24,8) NOT NULL, -- ✅ Changed to DECIMAL for precision
  `buyer_gold_balance` DECIMAL(24,8) NOT NULL, -- ✅ Changed to DECIMAL for precision
  `seller_rial_balance` DECIMAL(24,8) NOT NULL, -- ✅ Changed to DECIMAL for precision
  `seller_gold_balance` DECIMAL(24,8) NOT NULL, -- ✅ Changed to DECIMAL for precision
  `buyer_id` INT UNSIGNED NOT NULL,
  `seller_id` INT UNSIGNED NOT NULL,
  `goldis_fee` DECIMAL(24,8) NOT NULL, -- ✅ Changed to DECIMAL for precision
  `payment_fee` DECIMAL(24,8) NOT NULL, -- ✅ Changed to DECIMAL for precision
  `payment_provider_type` INT NOT NULL,
  `payment_ref_id` VARCHAR(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NOT NULL,
  `invoice_number` INT NULL,
  `invoice_id` VARCHAR(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NOT NULL,
  INDEX `ipg_ref_id` (`payment_ref_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_persian_ci;

-- ✅ Drop and Recreate Logs Table
DROP TABLE IF EXISTS `logs`;
CREATE TABLE `logs` (
  `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `create_datetime` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `shamsi_create_datetime` VARCHAR(45) NOT NULL,
  `user_id` INT UNSIGNED NOT NULL,
  `user_ip` VARCHAR(15) NOT NULL,
  `user_agent` VARCHAR(256) NOT NULL,
  `referer_url` VARCHAR(2048) NOT NULL,
  `request_method` VARCHAR(8) NOT NULL,
  `full_request_query` TEXT NOT NULL, 
  `request_duration` FLOAT NOT NULL,
  `description` VARCHAR(2048) NOT NULL,
  `log_level` TINYINT UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ✅ Drop and Recreate Invoices Table
DROP TABLE IF EXISTS `invoices`;
CREATE TABLE `invoices` (
  `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT UNSIGNED NOT NULL,
  `transaction_id` INT UNSIGNED NOT NULL,
  `transaction_type` TINYINT NOT NULL,
  `invoice_number` VARCHAR(50) UNIQUE NOT NULL,
  `total_rial_amount` DECIMAL(24,8) NOT NULL,
  `total_gold_amount` DECIMAL(24,8) NOT NULL,
  `gold_price_at_transaction` DECIMAL(24,8) NOT NULL,
  `status` ENUM('pending', 'paid', 'canceled', 'failed') NOT NULL DEFAULT 'pending',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_persian_ci;


-- ✅ Withdrawal Requests Table
DROP TABLE IF EXISTS `withdrawal_requests`;
CREATE TABLE `withdrawal_requests` (
  `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT UNSIGNED NOT NULL,
  `user_phone_number` CHAR(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_persian_ci NOT NULL,
  `amount` DECIMAL(24,8) NOT NULL,
  `status` TINYINT NOT NULL DEFAULT 0, -- 0: pending, 1: approved, 2: rejected, 3: processing, 4: completed
  `admin_id` INT UNSIGNED NULL,
  `bank_name` VARCHAR(255) NOT NULL,
  `card_number` VARCHAR(16) NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_persian_ci;

DROP TABLE IF EXISTS `tickets`;
CREATE TABLE `tickets` (
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `admin_id` INT NULL,
    `subject` VARCHAR(255) NOT NULL,
    `status` TINYINT NOT NULL DEFAULT 0, -- 0: open, 1: in_progress, etc.
    `priority` TINYINT NOT NULL DEFAULT 1, -- 0: low, 1: medium, etc.
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES users(`id`),
    FOREIGN KEY (`admin_id`) REFERENCES users(`id`)
);

-- ✅ Ticket Messages Table (Should be created after tickets)
DROP TABLE IF EXISTS `ticket_messages`;
CREATE TABLE `ticket_messages` (
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `ticket_id` INT UNSIGNED NOT NULL,
    `sender_id` INT NOT NULL,
    `message` TEXT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`ticket_id`) REFERENCES tickets(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`sender_id`) REFERENCES users(`id`) ON DELETE CASCADE
);



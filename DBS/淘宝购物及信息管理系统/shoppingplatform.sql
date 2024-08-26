/*
 Navicat Premium Data Transfer

 Source Server         : mysql
 Source Server Type    : MySQL
 Source Server Version : 80036
 Source Host           : localhost:3306
 Source Schema         : shoppingplatform

 Target Server Type    : MySQL
 Target Server Version : 80036
 File Encoding         : 65001

 Date: 01/06/2024 21:28:37
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for administrators
-- ----------------------------
DROP TABLE IF EXISTS `administrators`;
CREATE TABLE `administrators`  (
  `admin_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `address` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`admin_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of administrators
-- ----------------------------
INSERT INTO `administrators` VALUES ('A1001', '管理员_甲', '1', 'admin1@example.com', '0987654321', '管理地址1');
INSERT INTO `administrators` VALUES ('A1002', '管理员_乙', 'adminpass2', 'admin2@example.com', '0987654322', '管理地址2');

-- ----------------------------
-- Table structure for buyers
-- ----------------------------
DROP TABLE IF EXISTS `buyers`;
CREATE TABLE `buyers`  (
  `buyer_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `buyer_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `preferences` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `gender` enum('男','女','未知') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '未知',
  PRIMARY KEY (`buyer_id`) USING BTREE,
  CONSTRAINT `buyers_ibfk_1` FOREIGN KEY (`buyer_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of buyers
-- ----------------------------
INSERT INTO `buyers` VALUES ('U111114', 'KSGEI', NULL, '未知');
INSERT INTO `buyers` VALUES ('U111115', 'GGJijeko', NULL, '未知');
INSERT INTO `buyers` VALUES ('U111116', 'JohnDoe', '家电', '男');
INSERT INTO `buyers` VALUES ('U111118', 'TomSmith', '食品', '男');
INSERT INTO `buyers` VALUES ('U111120', 'MichaelChen', '生活用品', '男');
INSERT INTO `buyers` VALUES ('U111121', 'AliceGreen', '家电', '女');
INSERT INTO `buyers` VALUES ('U111123', 'CharlieBlack', '食品', '男');
INSERT INTO `buyers` VALUES ('U111125', 'EveBlue', '生活用品', '女');
INSERT INTO `buyers` VALUES ('U123456', '买家_张三', '电子产品', '未知');
INSERT INTO `buyers` VALUES ('U222222', '纯爱战士', NULL, '未知');
INSERT INTO `buyers` VALUES ('U543210', '买家_赵七', '食品', '未知');
INSERT INTO `buyers` VALUES ('U654321', '买家_李四', '服饰', '未知');
INSERT INTO `buyers` VALUES ('U666666', '6号玩家', '电子产品', '男');
INSERT INTO `buyers` VALUES ('U987654', '买家_王五', '饮料', '未知');

-- ----------------------------
-- Table structure for categories
-- ----------------------------
DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories`  (
  `category_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `category_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`category_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of categories
-- ----------------------------
INSERT INTO `categories` VALUES ('C1', '服饰');
INSERT INTO `categories` VALUES ('C2', '食品');
INSERT INTO `categories` VALUES ('C3', '电子产品');
INSERT INTO `categories` VALUES ('C4', '生活用品');

-- ----------------------------
-- Table structure for order_items
-- ----------------------------
DROP TABLE IF EXISTS `order_items`;
CREATE TABLE `order_items`  (
  `order_item_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `order_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `product_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `quantity` int NOT NULL,
  `subtotal` decimal(10, 2) NOT NULL,
  `product_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`order_item_id`) USING BTREE,
  INDEX `order_id`(`order_id` ASC) USING BTREE,
  INDEX `product_id`(`product_id` ASC) USING BTREE,
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of order_items
-- ----------------------------
INSERT INTO `order_items` VALUES ('OI1001', 'O1001', 'P1001', 1, 99.99, '女士长裙');
INSERT INTO `order_items` VALUES ('OI1002', 'O1001', 'P1002', 1, 59.99, '运动鞋');
INSERT INTO `order_items` VALUES ('OI1003', 'O1002', 'P1003', 1, 3.99, '饼干');
INSERT INTO `order_items` VALUES ('OI1004', 'O1003', 'P1001', 1, 99.99, '女士长裙');
INSERT INTO `order_items` VALUES ('OI1005', 'O1003', 'P1002', 1, 59.99, '运动鞋');
INSERT INTO `order_items` VALUES ('OI1006', 'O1003', 'P1005', 2, 99.98, '衬衫');
INSERT INTO `order_items` VALUES ('OI1007', 'O1004', 'P1003', 1, 3.99, '饼干');
INSERT INTO `order_items` VALUES ('OI1008', 'O1004', 'P1004', 2, 3.99, '饮料');
INSERT INTO `order_items` VALUES ('OI1009', 'O1005', 'P1009', 1, 4999.99, '笔记本电脑');
INSERT INTO `order_items` VALUES ('OI1010', 'O1005', 'P1011', 1, 199.99, '耳机');
INSERT INTO `order_items` VALUES ('OI1011', 'O1006', 'P1010', 1, 2999.99, '智能手机');
INSERT INTO `order_items` VALUES ('OI1012', 'O1006', 'P1012', 1, 399.99, '电视');
INSERT INTO `order_items` VALUES ('OI1013', 'O1007', 'P1009', 1, 4999.99, '笔记本电脑');
INSERT INTO `order_items` VALUES ('OI1014', 'O1007', 'P1010', 1, 2999.99, '智能手机');
INSERT INTO `order_items` VALUES ('OI1015', 'O1008', 'P1004', 2, 1.99, '饮料');
INSERT INTO `order_items` VALUES ('OI1016', 'O1008', 'P1008', 2, 1597.99, '薯片');
INSERT INTO `order_items` VALUES ('OI1017', 'O1009', 'P1018', 1, 1999.99, '冰箱');
INSERT INTO `order_items` VALUES ('OI1018', 'O1010', 'P1017', 1, 299.99, '微波炉');
INSERT INTO `order_items` VALUES ('OI1019', 'O1011', 'P1020', 1, 1599.99, '洗衣机');
INSERT INTO `order_items` VALUES ('OI1020', 'O1012', 'P1032', 1, 2999.99, '最新款手机');
INSERT INTO `order_items` VALUES ('OI1021', 'O1013', 'P1028', 30, 179.70, '牛奶');
INSERT INTO `order_items` VALUES ('OI1022', 'O1014', 'P1025', 1, 159.99, '电热水壶');
INSERT INTO `order_items` VALUES ('OI1023', 'O1015', 'P1034', 10, 99.90, '茉莉花茶');
INSERT INTO `order_items` VALUES ('OI1024', 'O1016', 'P1008', 12, 23.88, '薯片');
INSERT INTO `order_items` VALUES ('OI1025', 'O1017', 'P1034', 9, 89.91, '茉莉花茶');
INSERT INTO `order_items` VALUES ('OI1026', 'O1018', 'P1035', 15, 225.00, '蜜桃乌龙茶');

-- ----------------------------
-- Table structure for orders
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders`  (
  `order_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `buyer_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `order_date` datetime NOT NULL,
  `total_amount` decimal(10, 2) NULL DEFAULT NULL,
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `recipient_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `notes` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '',
  PRIMARY KEY (`order_id`) USING BTREE,
  INDEX `orders_ibfk_1`(`buyer_id` ASC) USING BTREE,
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`buyer_id`) REFERENCES `buyers` (`buyer_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of orders
-- ----------------------------
INSERT INTO `orders` VALUES ('O1001', 'U123456', '2024-05-23 18:26:08', 159.98, '待处理', '买家_张三', '北京市海淀区中关村', '13912345678', '');
INSERT INTO `orders` VALUES ('O1002', 'U123456', '2024-05-23 18:26:08', 3.99, '已发货', '买家_张三', '北京市海淀区中关村', '13912345678', '');
INSERT INTO `orders` VALUES ('O1003', 'U654321', '2024-05-23 18:32:31', 259.97, '待处理', '买家_李四', '上海市浦东新区', '13987654321', '');
INSERT INTO `orders` VALUES ('O1004', 'U123456', '2024-05-23 18:32:31', 7.98, '已发货', '买家_张三', '北京市海淀区中关村', '13912345678', '');
INSERT INTO `orders` VALUES ('O1005', 'U987654', '2024-05-23 19:21:26', 5199.97, '待处理', '买家_王五', '天津市南开区', '13812345678', '');
INSERT INTO `orders` VALUES ('O1006', 'U654321', '2024-05-23 19:21:26', 3399.98, '已发货', 'hua', '上海市浦东新区', '13987654321', '');
INSERT INTO `orders` VALUES ('O1007', 'U987654', '2024-05-23 19:21:26', 7399.97, '待处理', '买家_王五', '天津市南开区', '13812345678', '');
INSERT INTO `orders` VALUES ('O1008', 'U543210', '2024-05-23 19:21:26', 1599.98, '已发货', '买家_赵七', '重庆市渝中区', '13687654321', '');
INSERT INTO `orders` VALUES ('O1009', 'U111116', '2024-05-24 10:20:00', 1999.99, '待处理', 'john123', '北京市朝阳区', '13812345679', '');
INSERT INTO `orders` VALUES ('O1010', 'U111118', '2024-05-24 10:30:00', 299.99, '已发货', 'TomSmith', '广州市天河区', '13812345681', '');
INSERT INTO `orders` VALUES ('O1011', 'U111120', '2024-05-24 10:40:00', 1599.99, '待处理', 'MichaelChen', '天津市南开区', '13812345683', '');
INSERT INTO `orders` VALUES ('O1012', 'U111121', '2024-05-25 09:00:00', 2999.99, '待处理', 'AliceGreen', '北京市海淀区', '13812345684', '');
INSERT INTO `orders` VALUES ('O1013', 'U111123', '2024-05-25 09:30:00', 179.70, '已发货', 'CharlieBlack', '广州市黄埔区', '13812345686', '');
INSERT INTO `orders` VALUES ('O1014', 'U111125', '2024-05-25 10:00:00', 159.99, '待处理', 'EveBlue', '天津市和平区', '13812345688', '');
INSERT INTO `orders` VALUES ('O1015', 'U111115', '2024-05-26 03:04:43', 99.90, '待处理', 'GGJijeko', '天津市河东区', '13293890433', '');
INSERT INTO `orders` VALUES ('O1016', 'U111114', '2024-05-26 03:13:49', 23.88, '待处理', 'KSGEI', '天津市津南区', '17320086608', '');
INSERT INTO `orders` VALUES ('O1017', 'U222222', '2024-05-28 00:56:39', 89.91, '已发货', 'hua', '南开大学津南校区文科组团', '13293890432', '七夕快乐');
INSERT INTO `orders` VALUES ('O1018', 'U222222', '2024-06-01 12:46:49', 225.00, '待处理', 'Xing', '南开大学津南校区文科组团近邻宝代收', '13293890432', '避免暴晒');

-- ----------------------------
-- Table structure for products
-- ----------------------------
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products`  (
  `product_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `product_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `price` decimal(10, 2) NULL DEFAULT NULL,
  `stock` int NULL DEFAULT NULL,
  `category_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `shop_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `subcategory_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`product_id`) USING BTREE,
  INDEX `shop_id`(`shop_id` ASC) USING BTREE,
  INDEX `FK_category_id`(`category_id` ASC) USING BTREE,
  INDEX `FK_subcategory_id`(`subcategory_id` ASC) USING BTREE,
  CONSTRAINT `FK_category_id` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `FK_subcategory_id` FOREIGN KEY (`subcategory_id`) REFERENCES `subcategories` (`subcategory_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of products
-- ----------------------------
INSERT INTO `products` VALUES ('P1001', '女士长裙', '优雅的女士长裙', 99.99, 50, 'C1', 'SH1001', 'C1001');
INSERT INTO `products` VALUES ('P1002', '运动鞋', '舒适的运动鞋', 59.99, 100, 'C1', 'SH1001', 'C1002');
INSERT INTO `products` VALUES ('P1003', '饼干', '酥脆的巧克力饼干', 3.99, 200, 'C2', 'SH1002', 'C2002');
INSERT INTO `products` VALUES ('P1004', '饮料', '清爽的饮料', 1.99, 300, 'C2', 'SH1002', 'C2001');
INSERT INTO `products` VALUES ('P1005', '衬衫', '时尚的男士衬衫', 49.99, 150, 'C1', 'SH1001', 'C1002');
INSERT INTO `products` VALUES ('P1006', '牛仔裤', '经典的牛仔裤', 69.99, 80, 'C1', 'SH1001', 'C1002');
INSERT INTO `products` VALUES ('P1007', '果汁', '新鲜的果汁', 2.99, 500, 'C2', 'SH1002', 'C2001');
INSERT INTO `products` VALUES ('P1008', '薯片', '香脆的薯片', 1.99, 388, 'C2', 'SH1002', 'C2002');
INSERT INTO `products` VALUES ('P1009', '笔记本电脑', '高性能笔记本电脑', 4999.99, 28, 'C3', 'SH1003', 'C3001');
INSERT INTO `products` VALUES ('P1010', '智能手机', '最新款智能手机', 2999.99, 50, 'C3', 'SH1003', 'C3002');
INSERT INTO `products` VALUES ('P1011', '耳机', '无线蓝牙耳机', 199.99, 200, 'C3', 'SH1003', 'C3003');
INSERT INTO `products` VALUES ('P1012', '电视', '4K超高清电视', 3999.99, 20, 'C3', 'SH1003', 'C3004');
INSERT INTO `products` VALUES ('P1013', '女士T恤', '舒适的女士T恤', 29.99, 100, 'C1', 'SH1001', 'C1001');
INSERT INTO `products` VALUES ('P1014', '男士西装', '高档男士西装', 199.99, 50, 'C1', 'SH1001', 'C1002');
INSERT INTO `products` VALUES ('P1015', '橙汁', '新鲜橙汁', 2.49, 300, 'C2', 'SH1002', 'C2001');
INSERT INTO `products` VALUES ('P1016', '巧克力', '美味巧克力', 4.99, 150, 'C2', 'SH1002', 'C2002');
INSERT INTO `products` VALUES ('P1017', '微波炉', '高效微波炉', 299.99, 50, 'C4', 'SH1003', 'C4001');
INSERT INTO `products` VALUES ('P1018', '冰箱', '大容量冰箱', 1999.99, 20, 'C4', 'SH1003', 'C4001');
INSERT INTO `products` VALUES ('P1019', '烤箱', '多功能烤箱', 499.99, 30, 'C4', 'SH1003', 'C4001');
INSERT INTO `products` VALUES ('P1020', '洗衣机', '节能洗衣机', 1599.99, 25, 'C4', 'SH1003', 'C4001');
INSERT INTO `products` VALUES ('P1021', '果汁机', '新鲜果汁机', 199.99, 40, 'C2', 'SH1002', 'C4001');
INSERT INTO `products` VALUES ('P1022', '吸尘器', '高效吸尘器', 299.99, 50, 'C4', 'SH1006', 'C4001');
INSERT INTO `products` VALUES ('P1023', '电饭煲', '多功能电饭煲', 199.99, 20, 'C4', 'SH1006', 'C4001');
INSERT INTO `products` VALUES ('P1024', '空气炸锅', '健康空气炸锅', 499.99, 30, 'C4', 'SH1006', 'C4001');
INSERT INTO `products` VALUES ('P1025', '电热水壶', '快速电热水壶', 159.99, 25, 'C4', 'SH1006', 'C4001');
INSERT INTO `products` VALUES ('P1026', '搅拌机', '多用途搅拌机', 199.99, 40, 'C2', 'SH1002', 'C4001');
INSERT INTO `products` VALUES ('P1027', '咖啡机', '全自动咖啡机', 999.99, 15, 'C2', 'SH1002', 'C4001');
INSERT INTO `products` VALUES ('P1028', '牛奶', '纯牛奶', 5.99, 200, 'C2', 'SH1002', 'C2001');
INSERT INTO `products` VALUES ('P1029', '薯条', '美味薯条', 2.99, 300, 'C2', 'SH1002', 'C2002');
INSERT INTO `products` VALUES ('P1030', '耳机', '降噪耳机', 299.99, 50, 'C3', 'SH1003', 'C3003');
INSERT INTO `products` VALUES ('P1031', '音响', '无线音响', 499.99, 20, 'C3', 'SH1003', 'C3003');
INSERT INTO `products` VALUES ('P1032', '手机', '最新款手机', 2999.99, 30, 'C3', 'SH1003', 'C3002');
INSERT INTO `products` VALUES ('P1033', '平板电脑', '高性能平板电脑', 1999.99, 2, 'C3', 'SH1003', 'C3001');
INSERT INTO `products` VALUES ('P1034', '茉莉花茶', '清新的淡淡花香', 9.99, 57, 'C2', 'SH1002', 'C2001');
INSERT INTO `products` VALUES ('P1035', '蜜桃乌龙茶', '甜润果香，口感独特', 15.00, 135, 'C2', 'SH1002', 'C2001');

-- ----------------------------
-- Table structure for sellers
-- ----------------------------
DROP TABLE IF EXISTS `sellers`;
CREATE TABLE `sellers`  (
  `seller_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `shop_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `seller_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `gender` enum('男','女','未知') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '未知',
  PRIMARY KEY (`seller_id`) USING BTREE,
  CONSTRAINT `sellers_ibfk_1` FOREIGN KEY (`seller_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sellers
-- ----------------------------
INSERT INTO `sellers` VALUES ('U111112', 'SH1008', 'Reminding', '女');
INSERT INTO `sellers` VALUES ('U111113', NULL, 'SKYerlooper', '未知');
INSERT INTO `sellers` VALUES ('U111117', 'SH1004', 'JaneDoe', '女');
INSERT INTO `sellers` VALUES ('U111119', 'SH1005', 'LucyLiu', '女');
INSERT INTO `sellers` VALUES ('U111122', 'SH1005', 'BobBrown', '男');
INSERT INTO `sellers` VALUES ('U111124', 'SH1006', 'DianaWhite', '女');
INSERT INTO `sellers` VALUES ('U345678', 'SH1002', '超级无敌菠萝头', '男');
INSERT INTO `sellers` VALUES ('U789012', 'SH1001', '卖家_王五', '未知');
INSERT INTO `sellers` VALUES ('U876543', 'SH1003', '卖家_陈八', '未知');
INSERT INTO `sellers` VALUES ('U999999', NULL, '', '未知');

-- ----------------------------
-- Table structure for shops
-- ----------------------------
DROP TABLE IF EXISTS `shops`;
CREATE TABLE `shops`  (
  `shop_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `shop_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `shop_description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `seller_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`shop_id`) USING BTREE,
  INDEX `shops_ibfk_1`(`seller_id` ASC) USING BTREE,
  CONSTRAINT `shops_ibfk_1` FOREIGN KEY (`seller_id`) REFERENCES `sellers` (`seller_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of shops
-- ----------------------------
INSERT INTO `shops` VALUES ('SH1001', '王五的服装店', '最新流行女装', 'U789012');
INSERT INTO `shops` VALUES ('SH1002', '赵六的零食店', '美味零食和饮料', 'U345678');
INSERT INTO `shops` VALUES ('SH1003', '陈八的电子店', '最新电子产品', 'U876543');
INSERT INTO `shops` VALUES ('SH1004', 'Jane的家居店', '家居用品', 'U111117');
INSERT INTO `shops` VALUES ('SH1005', 'Bob的电子产品店', '最新电子产品', 'U111122');
INSERT INTO `shops` VALUES ('SH1006', 'Diana的家电店', '优质家电', 'U111124');
INSERT INTO `shops` VALUES ('SH1007', 'Re鲜花', '每日上新当季鲜花', 'U111112');
INSERT INTO `shops` VALUES ('SH1008', '2', '2', 'U111112');

-- ----------------------------
-- Table structure for subcategories
-- ----------------------------
DROP TABLE IF EXISTS `subcategories`;
CREATE TABLE `subcategories`  (
  `subcategory_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `subcategory_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `category_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`subcategory_id`) USING BTREE,
  INDEX `FK_parent_category_id`(`category_id` ASC) USING BTREE,
  CONSTRAINT `FK_parent_category_id` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of subcategories
-- ----------------------------
INSERT INTO `subcategories` VALUES ('C1001', '女士服装', 'C1');
INSERT INTO `subcategories` VALUES ('C1002', '男士服装', 'C1');
INSERT INTO `subcategories` VALUES ('C1003', '项链', 'C1');
INSERT INTO `subcategories` VALUES ('C1004', '帽子', 'C1');
INSERT INTO `subcategories` VALUES ('C2001', '饮料', 'C2');
INSERT INTO `subcategories` VALUES ('C2002', '零食', 'C2');
INSERT INTO `subcategories` VALUES ('C3001', '电脑', 'C3');
INSERT INTO `subcategories` VALUES ('C3002', '手机', 'C3');
INSERT INTO `subcategories` VALUES ('C3003', '耳机', 'C3');
INSERT INTO `subcategories` VALUES ('C3004', '电视', 'C3');
INSERT INTO `subcategories` VALUES ('C4001', '家居设备', 'C4');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `user_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '',
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '',
  `user_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`user_id`) USING BTREE,
  CONSTRAINT `users_chk_1` CHECK (`user_type` in (_utf8mb4'buyer',_utf8mb4'seller'))
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES ('U111112', 'Reminding', '3', '2211999@mail.nankai.edu.cn', '13293890432', '南开大学津南校区', 'seller');
INSERT INTO `users` VALUES ('U111113', 'SKYerlooper', '123456', '', '', '', 'seller');
INSERT INTO `users` VALUES ('U111114', 'KSGEI', '654321', '', '17320086608', '天津市津南区', 'buyer');
INSERT INTO `users` VALUES ('U111115', 'GGJijeko', '951473', '', '13293890433', '天津市河东区', 'buyer');
INSERT INTO `users` VALUES ('U111116', 'JohnDoe', 'john123', 'john@example.com', '13812345679', '北京市朝阳区', 'buyer');
INSERT INTO `users` VALUES ('U111117', 'JaneDoe', 'jane123', 'jane@example.com', '13812345680', '上海市徐汇区', 'seller');
INSERT INTO `users` VALUES ('U111118', 'TomSmith', 'tom123', 'tom@example.com', '13812345681', '广州市天河区', 'buyer');
INSERT INTO `users` VALUES ('U111119', 'LucyLiu', 'lucy123', 'lucy@example.com', '13812345682', '深圳市南山区', 'seller');
INSERT INTO `users` VALUES ('U111120', 'MichaelChen', 'michael123', 'michael@example.com', '13812345683', '天津市南开区', 'buyer');
INSERT INTO `users` VALUES ('U111121', 'AliceGreen', 'alice123', 'alice@example.com', '13812345684', '北京市海淀区', 'buyer');
INSERT INTO `users` VALUES ('U111122', 'BobBrown', 'bob123', 'bob@example.com', '13812345685', '上海市浦东新区', 'seller');
INSERT INTO `users` VALUES ('U111123', 'CharlieBlack', 'charlie123', 'charlie@example.com', '13812345686', '广州市黄埔区', 'buyer');
INSERT INTO `users` VALUES ('U111124', 'DianaWhite', 'diana123', 'diana@example.com', '13812345687', '深圳市福田区', 'seller');
INSERT INTO `users` VALUES ('U111125', 'EveBlue', 'eve123', 'eve@example.com', '13812345688', '天津市和平区', 'buyer');
INSERT INTO `users` VALUES ('U123456', '买家_张三', 'password234', 'zhangsan@example.com', '13912345678', '北京市海淀区中关村', 'buyer');
INSERT INTO `users` VALUES ('U222222', '纯爱战士', '2', '2211999@mail.nankai.edu.cn', '17320086608', '天津市津南区海河教育园区', 'buyer');
INSERT INTO `users` VALUES ('U345678', '超级无敌菠萝头', '123', 'zhaoliu@example.com', '13887654321', '深圳市南山区', 'seller');
INSERT INTO `users` VALUES ('U543210', '买家_赵七', 'password123', 'zhaoqi@example.com', '13687654321', '重庆市渝中区', 'buyer');
INSERT INTO `users` VALUES ('U654321', '买家_李四', 'password123', 'lisi@example.com', '13987654321', '上海市浦东新区', 'buyer');
INSERT INTO `users` VALUES ('U666666', '6号玩家', '6', '', '', '', 'buyer');
INSERT INTO `users` VALUES ('U789012', '卖家_王五', 'password123', 'wangwu@example.com', '13812345678', '广州市天河区', 'seller');
INSERT INTO `users` VALUES ('U876543', '卖家_陈八', 'password123', 'chenba@example.com', '13512345678', '成都市锦江区', 'seller');
INSERT INTO `users` VALUES ('U987654', '买家_王五', 'password123', 'wangwu@example.com', '13712345678', '天津市南开区', 'buyer');
INSERT INTO `users` VALUES ('U999999', 'happykid', '999999999', '999999999@qq.com', '16637735657', '四川省成都市', 'seller');

-- ----------------------------
-- Triggers structure for table products
-- ----------------------------
DROP TRIGGER IF EXISTS `check_product_price_stock`;
delimiter ;;
CREATE TRIGGER `check_product_price_stock` BEFORE INSERT ON `products` FOR EACH ROW BEGIN
    IF NEW.price < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '产品价格不能为负数';
    END IF;
    IF NEW.stock < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '产品库存不能为负数';
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table products
-- ----------------------------
DROP TRIGGER IF EXISTS `check_product_price_stock_update`;
delimiter ;;
CREATE TRIGGER `check_product_price_stock_update` BEFORE UPDATE ON `products` FOR EACH ROW BEGIN
    IF NEW.price < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '产品价格不能为负数';
    END IF;
    IF NEW.stock < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '产品库存不能为负数';
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table users
-- ----------------------------
DROP TRIGGER IF EXISTS `after_user_insert`;
delimiter ;;
CREATE TRIGGER `after_user_insert` AFTER INSERT ON `users` FOR EACH ROW BEGIN
    IF NEW.user_type = 'buyer' THEN
        INSERT INTO buyers (buyer_id, buyer_name) VALUES (NEW.user_id, NEW.username);
    ELSEIF NEW.user_type = 'seller' THEN
        INSERT INTO sellers (seller_id, seller_name) VALUES (NEW.user_id, NEW.username);
    END IF;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;

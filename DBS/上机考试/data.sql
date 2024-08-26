-- 删除所有数据
DELETE FROM order_items;
DELETE FROM orders;
DELETE FROM products;
DELETE FROM categories;
DELETE FROM sellers;
DELETE FROM shops;
DELETE FROM buyers;
DELETE FROM users;
DELETE FROM administrators;

-- 插入一些基本的用户数据
INSERT INTO users (user_id, username, password, email, phone, address, user_type) VALUES
('U123456', '买家_张三', 'password123', 'zhangsan@example.com', '13912345678', '北京市海淀区中关村', 'buyer'),
('U654321', '买家_李四', 'password123', 'lisi@example.com', '13987654321', '上海市浦东新区', 'buyer'),
('U789012', '卖家_王五', 'password123', 'wangwu@example.com', '13812345678', '广州市天河区', 'seller'),
('U345678', '卖家_赵六', 'password123', 'zhaoliu@example.com', '13887654321', '深圳市南山区', 'seller');

-- 插入一些基本的买家数据
INSERT INTO buyers (buyer_id, user_id) VALUES
('B1', 'U123456'),
('B2', 'U654321');

-- 插入一些基本的卖家数据，并关联到店铺
INSERT INTO sellers (seller_id, user_id, shop_id) VALUES
('S1', 'U789012', 'SH1001'),
('S2', 'U345678', 'SH1002');

-- 插入一些基本的店铺数据
INSERT INTO shops (shop_id, shop_name, shop_description, seller_id) VALUES
('SH1001', '王五的服装店', '最新流行女装', 'S1'),
('SH1002', '赵六的零食店', '美味零食和饮料', 'S2');

-- 插入一些基本的分类数据
INSERT INTO categories (category_id, category_name) VALUES
('C1', '服饰'),
('C2', '食品'),
('C3', '生鲜'),
('C4', '生活用品');

-- 插入一些基本的产品数据，并关联到店铺和分类
INSERT INTO products (product_id, product_name, description, price, stock, category_id, shop_id) VALUES
('P1001', '女士长裙', '优雅的女士长裙', 99.99, 50, 'C1', 'SH1001'),
('P1002', '运动鞋', '舒适的运动鞋', 59.99, 100, 'C1', 'SH1001'),
('P1003', '饼干', '酥脆的巧克力饼干', 3.99, 200, 'C2', 'SH1002'),
('P1004', '饮料', '清爽的饮料', 1.99, 300, 'C2', 'SH1002');

-- 插入一些基本的订单数据
INSERT INTO orders (order_id, buyer_id, order_date, total_amount, status) VALUES
('O1001', 'B1', NOW(), 159.98, '待处理'),
('O1002', 'B2', NOW(), 3.99, '已发货');

-- 插入一些基本的订单明细数据
INSERT INTO order_items (order_item_id, order_id, product_id, quantity, subtotal) VALUES
('OI1001', 'O1001', 'P1001', 1, 99.99),
('OI1002', 'O1001', 'P1002', 1, 59.99),
('OI1003', 'O1002', 'P1003', 1, 3.99);

-- 插入一些基本的管理员数据
INSERT INTO administrators (admin_id, username, password, email, phone, address) VALUES
('A1001', '管理员_甲', 'adminpass1', 'admin1@example.com', '0987654321', '管理地址1'),
('A1002', '管理员_乙', 'adminpass2', 'admin2@example.com', '0987654322', '管理地址2');

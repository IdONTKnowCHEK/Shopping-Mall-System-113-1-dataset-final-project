-- 初始化資料庫
CREATE DATABASE IF NOT EXISTS SOGO;
USE SOGO;

-- Shopping Mall Table
CREATE TABLE IF NOT EXISTS Shopping_Mall (
    Branch_Name VARCHAR(100) PRIMARY KEY,
    Address VARCHAR(255),
    Contact VARCHAR(20),
    Business_Hours VARCHAR(50),
    Floor_Area INT,
    Web_URL VARCHAR(255)
);

-- Shops Table
CREATE TABLE IF NOT EXISTS Shops (
    Store_Name VARCHAR(100) PRIMARY KEY,
    Branch_Name VARCHAR(100),
    Floor_Location VARCHAR(50),
    Phone VARCHAR(20),
    Web_URL VARCHAR(255),
    FOREIGN KEY (Branch_Name) REFERENCES Shopping_Mall(Branch_Name)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Goods Table
CREATE TABLE IF NOT EXISTS Goods (
    Name VARCHAR(100),
    Store_Name VARCHAR(100),
    Stock_Quantity INT,
    PRIMARY KEY (Name, Store_Name),
    FOREIGN KEY (Store_Name) REFERENCES Shops(Store_Name)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- g_Name Table
CREATE TABLE IF NOT EXISTS g_Name (
    Name VARCHAR(100) PRIMARY KEY,
    Price DECIMAL(10, 2)
);

-- Supplier Table
CREATE TABLE IF NOT EXISTS Supplier (
    Name VARCHAR(100) PRIMARY KEY,
    Address VARCHAR(255),
    Contact VARCHAR(20)
);

-- Purchase Detail Table
CREATE TABLE IF NOT EXISTS Purchase_Detail (
    Serial_Number INT PRIMARY KEY AUTO_INCREMENT,
    Supplier VARCHAR(100),
    Time DATETIME,
    Store_Name VARCHAR(100),
    Goods VARCHAR(100),
    Amount INT,
    FOREIGN KEY (Supplier) REFERENCES Supplier(Name)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (Store_Name) REFERENCES Shops(Store_Name)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Goods) REFERENCES Goods(Name)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- Promotional Campaign Table
CREATE TABLE IF NOT EXISTS Promotional_Campaign (
    Store_Name VARCHAR(100),
    Name VARCHAR(100),
    Start_Time DATETIME,
    End_Time DATETIME,
    Method VARCHAR(50),
    PRIMARY KEY (Store_Name, Name),
    FOREIGN KEY (Store_Name) REFERENCES Shops(Store_Name)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Mall Employee Table
CREATE TABLE IF NOT EXISTS Mall_Employee (
    Name VARCHAR(100),
    Contact VARCHAR(20),
    Position VARCHAR(50),
    Shift_Time VARCHAR(50),
    Branch_Name VARCHAR(100),
    PRIMARY KEY (Name, Branch_Name),
    FOREIGN KEY (Branch_Name) REFERENCES Shopping_Mall(Branch_Name)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Shop Employee Table
CREATE TABLE IF NOT EXISTS Shop_Employee (
    Name VARCHAR(100),
    Contact VARCHAR(20),
    Position VARCHAR(50),
    Shift_Time VARCHAR(50),
    Store_Name VARCHAR(100),
    PRIMARY KEY (Name, Store_Name),
    FOREIGN KEY (Store_Name) REFERENCES Shops(Store_Name)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Shopping Sheet Table
CREATE TABLE IF NOT EXISTS Shopping_Sheet (
    Store_Name VARCHAR(100),
    Time DATETIME,
    Price DECIMAL(10, 2),
    Payment VARCHAR(50),
    PRIMARY KEY (Store_Name, Time),
    FOREIGN KEY (Store_Name) REFERENCES Shops(Store_Name)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 初始化資料庫
CREATE DATABASE IF NOT EXISTS SOGO;
USE SOGO;

-- 插入 Shopping_Mall 資料
INSERT INTO Shopping_Mall (Branch_Name, Address, Contact, Business_Hours, Floor_Area, Web_URL) VALUES
('台北忠孝館', '台北市忠孝東路4段45號', '02-27765555', '11:00-21:30', 35000, 'https://info.sogo.com.tw/tp1'),
('新竹店', '新竹市中央路239號', '03-6200000', '11:00-21:30', 20000, 'https://info.sogo.com.tw/hcbc');

-- 插入 Shops 資料
INSERT INTO Shops (Store_Name, Branch_Name, Floor_Location, Phone, Web_URL) VALUES
('台隆手創館_廣三門市', '台北忠孝館', 'B1', '04-2329-2386', 'https://shopping.hands.com.tw/?lang=zh-TW'),
('BIG TRAIN_新竹店', '新竹店', '4F', '03-5457003', 'https://info.sogo.com.tw/hcbc/brand/18030816244449261');

-- 插入 Goods 資料
INSERT INTO Goods (Name, Store_Name, Stock_Quantity) VALUES
('花漾戀愛修容組 GLOW FLEUR CHEEKS', '台隆手創館_廣三門市', 0),
('BIG TRAIN 條紋雪紡短袖女上衣(藍)', 'BIG TRAIN_新竹店', 0);

-- 插入 g_Name 資料
INSERT INTO g_Name (Name, Price) VALUES
('花漾戀愛修容組 GLOW FLEUR CHEEKS', 1200.00),
('BIG TRAIN 條紋雪紡短袖女上衣(藍)', 690.00);

-- 插入 Supplier 資料
INSERT INTO Supplier (Name, Address, Contact) VALUES
('義隆供應商', '台北市大安區忠孝東路一段100號', '02-12345678'),
('悅巧精品公司', '新竹市東區光復路85號', '03-67890123');

-- 插入 Purchase_Detail 資料
INSERT INTO Purchase_Detail (Supplier, Time, Store_Name, Goods, Amount) VALUES
('義隆供應商', '2023-03-01 12:35:09', '台隆手創館_廣三門市', '花漾戀愛修容組 GLOW FLEUR CHEEKS', 50),
('悅巧精品公司', '2023-05-02 15:17:23', 'BIG TRAIN_新竹店', 'BIG TRAIN 條紋雪紡短袖女上衣(藍)', 100);

-- 插入 Promotional_Campaign 資料
INSERT INTO Promotional_Campaign (Store_Name, Name, Start_Time, End_Time, Method) VALUES
('台隆手創館_廣三門市', '夏日嘉年華', '2023-06-01 10:00:00', '2023-06-05 18:00:00', '折扣促銷'),
('BIG TRAIN_新竹店', '春季特賣', '2023-03-15 10:00:00', '2023-03-20 18:00:00', '贈品優惠');

-- 插入 Mall_Employee 資料
INSERT INTO Mall_Employee (Name, Contact, Position, Shift_Time, Branch_Name) VALUES
('陳智偉', '0966-466166', '店長', '11:00-21:30', '台北忠孝館'),
('張詠萱', '0977-432109', '兼職人員', '9:00-16:30', '新竹店');

-- 插入 Shop_Employee 資料
INSERT INTO Shop_Employee (Name, Contact, Position, Shift_Time, Store_Name) VALUES
('陳家琪', '0932-425789', '店長', '11:00-21:30', '台隆手創館_廣三門市'),
('黃士汝', '0915-924736', '門市店員', '9:00-16:30', 'BIG TRAIN_新竹店');

-- 插入 Shopping_Sheet 資料
INSERT INTO Shopping_Sheet (Store_Name, Time, Price, Payment) VALUES
('台隆手創館_廣三門市', '2023-05-27 12:20:48', 3590.00, 'credit card'),
('BIG TRAIN_新竹店', '2023-05-29 21:18:47', 1890.00, 'credit card');


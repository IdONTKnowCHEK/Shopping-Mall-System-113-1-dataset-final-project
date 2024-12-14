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

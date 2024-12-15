from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ShoppingMall(db.Model):
    __tablename__ = 'shopping_mall'
    branch_name = db.Column(db.String(100), primary_key=True)
    address = db.Column(db.String(255))
    contact = db.Column(db.String(20))
    business_hours = db.Column(db.String(50))
    floor_area = db.Column(db.Integer)
    web_url = db.Column(db.String(255))

    shops = db.relationship('Shops', backref='mall', cascade="all, delete-orphan")


class Shops(db.Model):
    __tablename__ = 'shops'
    store_name = db.Column(db.String(100), primary_key=True)
    branch_name = db.Column(db.String(100), db.ForeignKey('shopping_mall.branch_name', ondelete='CASCADE', onupdate='CASCADE'))
    floor_location = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    web_url = db.Column(db.String(255))

    goods = db.relationship('Goods', backref='shop', cascade="all, delete-orphan")
    shop_employees = db.relationship('ShopEmployee', backref='shop', cascade="all, delete-orphan")
    campaigns = db.relationship('PromotionalCampaign', backref='shop', cascade="all, delete-orphan")
    purchase_details = db.relationship('PurchaseDetail', backref='shop', cascade="all, delete-orphan")
    shopping_sheets = db.relationship('ShoppingSheet', backref='shop', cascade="all, delete-orphan")


class Goods(db.Model):
    __tablename__ = 'goods'
    name = db.Column(db.String(100), primary_key=True)
    store_name = db.Column(db.String(100), db.ForeignKey('shops.store_name', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    stock_quantity = db.Column(db.Integer)

    purchase_details = db.relationship('PurchaseDetail', backref='goods', cascade="all, delete-orphan")


class GName(db.Model):
    __tablename__ = 'g_name'
    name = db.Column(db.String(100), primary_key=True)
    price = db.Column(db.Numeric(10, 2))


class Supplier(db.Model):
    __tablename__ = 'supplier'
    name = db.Column(db.String(100), primary_key=True)
    address = db.Column(db.String(255))
    contact = db.Column(db.String(20))

    purchase_details = db.relationship('PurchaseDetail', backref='supplier', cascade="all, delete-orphan")


class PurchaseDetail(db.Model):
    __tablename__ = 'purchase_detail'
    serial_number = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier = db.Column(db.String(100), db.ForeignKey('supplier.name', ondelete='SET NULL', onupdate='CASCADE'))
    time = db.Column(db.DateTime)
    store_name = db.Column(db.String(100), db.ForeignKey('shops.store_name', ondelete='CASCADE', onupdate='CASCADE'))
    goods = db.Column(db.String(100), db.ForeignKey('goods.name', ondelete='SET NULL', onupdate='CASCADE'))
    amount = db.Column(db.Integer)


class PromotionalCampaign(db.Model):
    __tablename__ = 'promotional_campaign'
    store_name = db.Column(db.String(100), db.ForeignKey('shops.store_name', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    name = db.Column(db.String(100), primary_key=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    method = db.Column(db.String(50))


class MallEmployee(db.Model):
    __tablename__ = 'mall_employee'
    name = db.Column(db.String(100), primary_key=True)
    contact = db.Column(db.String(20))
    position = db.Column(db.String(50))
    shift_time = db.Column(db.String(50))
    branch_name = db.Column(db.String(100), db.ForeignKey('shopping_mall.branch_name', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)


class ShopEmployee(db.Model):
    __tablename__ = 'shop_employee'
    name = db.Column(db.String(100), primary_key=True)
    contact = db.Column(db.String(20))
    position = db.Column(db.String(50))
    shift_time = db.Column(db.String(50))
    store_name = db.Column(db.String(100), db.ForeignKey('shops.store_name', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)


class ShoppingSheet(db.Model):
    __tablename__ = 'shopping_sheet'
    store_name = db.Column(db.String(100), db.ForeignKey('shops.store_name', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    time = db.Column(db.DateTime, primary_key=True)
    price = db.Column(db.Numeric(10, 2))
    payment = db.Column(db.String(50))

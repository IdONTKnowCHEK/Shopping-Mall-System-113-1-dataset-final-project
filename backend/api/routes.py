from flask import Blueprint
from api.test_route import test_bp
from api.goods_route import goods_bp
from api.employees_route import employees_bp
from api.promotions_route import promotions_bp
from api.purchase_detail_route import purchase_detail_bp
from api.suppliers_route import suppliers_bp
from api.stores_route import stores_bp
from api.transactions_route import transactions_bp

def register_blueprints(app):
    app.register_blueprint(test_bp)
    app.register_blueprint(goods_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(promotions_bp)
    app.register_blueprint(purchase_detail_bp)
    app.register_blueprint(suppliers_bp)
    app.register_blueprint(stores_bp)
    app.register_blueprint(transactions_bp)        
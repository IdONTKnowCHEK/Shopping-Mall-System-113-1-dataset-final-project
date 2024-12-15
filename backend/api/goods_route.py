from flask import Blueprint, jsonify, request, current_app

goods_bp = Blueprint('goods', __name__)

@goods_bp.route('/shop/goods', methods=['GET'])
def get_shop_goods():
    """
    獲取指定店鋪的商品列表
    ---
    tags:
      - Goods API
    parameters:
      - name: shop_name
        in: query
        type: string
        required: true
        description: 店鋪名稱
    responses:
      200:
        description: 返回商品列表
        examples:
          application/json: 
            [
              {"name": "商品1", "price": 100, "stock": 50},
              {"name": "商品2", "price": 200, "stock": 30}
            ]
      400:
        description: 店鋪名稱缺失或請求無效
        examples:
          application/json: {"error": "Shop name is required"}
    """
    shop_name = request.args.get('shop_name')
    if not shop_name:
        return jsonify({"error": "Shop name is required"}), 400

    # 使用 current_app 獲取 SQLAlchemy 的資料庫會話
    db = current_app.extensions['sqlalchemy'].db

    query = """
        SELECT goods.Name, g_Name.price, goods.Stock_quantity
        FROM goods 
        JOIN g_Name ON goods.Name = g_Name.Name 
        WHERE Store_name = :shop_name
    """

    # 執行 SQL 查詢並返回結果
    results = db.session.execute(query, {"shop_name": shop_name}).fetchall()
    
    # 將結果格式化為 JSON
    goods = [{"name": r[0], "price": r[1], "stock": r[2]} for r in results]

    return jsonify(goods)

from flask import Blueprint, jsonify, request, make_response, json
from models.models import db
from sqlalchemy import text

goods_bp = Blueprint('goods', __name__)

@goods_bp.route('/goods/shop', methods=['GET'])
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
    try:
        # 從 Query 參數取得 shop_name
        shop_name = request.args.get('shop_name')
        if not shop_name:
            return jsonify({"error": "Shop name is required"}), 400

        # 查詢指定店鋪的商品資訊：名稱、價格、庫存
        query = text("""
            SELECT g.Name AS goods_name, gn.Price AS price, g.Stock_Quantity AS stock
            FROM Goods g
            JOIN g_Name gn ON g.Name = gn.Name
            WHERE g.Store_Name = :shop_name;
        """)
        results = db.session.execute(query, {"shop_name": shop_name}).fetchall()

        goods_list = []
        for row in results:
            goods_list.append({
                "name": row[0],
                "price": float(row[1]),
                "stock": row[2]
            })

        # JSON 序列化，確保中文正常顯示
        json_str = json.dumps(goods_list, ensure_ascii=False)

        response = make_response(json_str, 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
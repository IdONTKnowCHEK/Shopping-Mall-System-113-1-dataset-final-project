from flask import Blueprint, jsonify, request, make_response, json
from models.models import db
from sqlalchemy import text

goods_bp = Blueprint('goods', __name__)

@goods_bp.route('/goods/shop', methods=['GET'])
def get_shop_goods():
    """
    取得指定店鋪的商品列表
    
    從 Goods 與 g_Name 資料表中查詢特定店鋪 (Store_Name) 的所有商品資訊，包括名稱、價格、庫存數量等，並以 JSON 清單形式回傳。
    例如: 23區_台北忠孝館
    ---
    tags:
      - Goods API
    summary: "取得指定店鋪的商品列表"
    description: "透過 query string 接收參數 shop_name，查詢該店鋪所擁有的商品，並返回商品名稱、價格、庫存資訊等。"
    parameters:
      - name: shop_name
        in: query
        type: string
        required: true
        description: 店鋪名稱
    responses:
      200:
        description: 成功返回指定店鋪的商品列表
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
      500:
        description: 內部伺服器錯誤
        examples:
          application/json:
            {
              "error": "Internal server error",
              "details": "詳細錯誤資訊"
            }
    """
    
    try:
        # 從 Query 參數取得 shop_name
        shop_name = request.args.get('shop_name')
        if not shop_name:
            return jsonify({"error": "Shop name is required"}), 400

        # 查詢指定店鋪的商品資訊
        query = text("""
            SELECT Name AS goods_name, Price AS price, Stock_Quantity AS stock
            FROM Goods
            WHERE Store_Name = :shop_name;
        """)
        results = db.session.execute(query, {"shop_name": shop_name}).fetchall()

        goods_list = []
        for row in results:
            goods_list.append({
                "name": row[0],
                "price": float(row[1]),
                "stock": row[2],
                "price": row[1]  # 確保價格欄位正確返回
            })

        # JSON 序列化，確保中文正常顯示
        json_str = json.dumps(goods_list, ensure_ascii=False)

        response = make_response(json_str, 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
from flask import Blueprint, jsonify, request, current_app

promotions_bp = Blueprint('promotions', __name__)

@promotions_bp.route('/shop/promotions', methods=['GET'])
def get_shop_promotions():
    """
    獲取指定店鋪的促銷活動
    ---
    tags:
      - Promotions API
    parameters:
      - name: shop_name
        in: query
        type: string
        required: true
        description: 店鋪名稱
    responses:
      200:
        description: 返回促銷活動列表
        examples:
          application/json:
            [
              {
                "name": "夏日嘉年華",
                "start_time": "2023-06-01 10:00:00",
                "end_time": "2023-06-05 18:00:00",
                "method": "折扣促銷"
              },
              {
                "name": "新年特惠",
                "start_time": "2024-01-01 00:00:00",
                "end_time": "2024-01-10 23:59:59",
                "method": "買一送一"
              }
            ]
      400:
        description: 缺少參數或請求無效
        examples:
          application/json: {"error": "Shop name is required"}
    """
    shop_name = request.args.get('shop_name')
    
    if not shop_name:
        return jsonify({"error": "Shop name is required"}), 400

    # 使用 current_app 獲取 SQLAlchemy 的資料庫會話
    db = current_app.extensions['sqlalchemy'].db

    query = """
        SELECT Name, Start_time, End_time, Method
        FROM promotional_campaign
        WHERE Store_Name = :shop_name
        AND Start_time > CURDATE()
    """

    # 執行 SQL 查詢並返回結果
    results = db.session.execute(query, {"shop_name": shop_name}).fetchall()

    # 將結果格式化為 JSON
    promotions = [
        {
            "name": r[0],
            "start_time": r[1],
            "end_time": r[2],
            "method": r[3]
        }
        for r in results
    ]

    return jsonify(promotions)

@promotions_bp.route('/promotions-by-method', methods=['GET'])
def get_promotions_by_method():
    """
    查詢促銷活動（按促銷方式）
    ---
    tags:
      - Promotions API
    parameters:
      - name: method
        in: query
        type: string
        required: true
        description: 促銷方式 (例如 折扣促銷, 贈品促銷)
    responses:
      200:
        description: 返回按促銷方式篩選的促銷活動
        examples:
          application/json:
            [
              {
                "store_name": "商店1",
                "promotion_name": "夏日促銷",
                "start_time": "2023-06-01 10:00:00",
                "end_time": "2023-06-10 18:00:00"
              }
            ]
      400:
        description: 缺少參數或請求無效
        examples:
          application/json:
            {"error": "Promotion method is required"}
      404:
        description: 找不到促銷活動
        examples:
          application/json:
            {"error": "No promotions found for method: 折扣促銷"}
    """
    method = request.args.get('method')  # 獲取促銷方式參數
    if not method:
        return jsonify({"error": "Promotion method is required"}), 400

    # 使用 current_app 獲取資料庫會話
    db = current_app.extensions['sqlalchemy'].db

    query = """
        SELECT Store_Name, Name, Start_time, End_time 
        FROM promotional_campaign 
        WHERE Method = :method;
    """
    results = db.session.execute(query, {"method": method}).fetchall()

    if not results:
        return jsonify({"error": f"No promotions found for method: {method}"}), 404

    # 將結果格式化為 JSON
    promotions = [
        {
            "store_name": row[0],
            "promotion_name": row[1],
            "start_time": row[2],
            "end_time": row[3]
        }
        for row in results
    ]
    return jsonify(promotions)

@promotions_bp.route('/promotions-by-date', methods=['GET'])
def get_promotions_by_date():
    """
    查詢促銷活動（按日期）
    ---
    tags:
      - Promotions API
    parameters:
      - name: date
        in: query
        type: string
        required: true
        description: 查詢的日期 (格式 YYYY-MM-DD)
    responses:
      200:
        description: 返回在指定日期進行中的促銷活動
        examples:
          application/json:
            [
              {
                "store_name": "商店1",
                "promotion_name": "夏日促銷",
                "start_time": "2023-06-01 10:00:00",
                "end_time": "2023-06-10 18:00:00",
                "method": "折扣促銷"
              }
            ]
      400:
        description: 缺少參數或請求無效
        examples:
          application/json:
            {"error": "Date is required"}
      404:
        description: 找不到促銷活動
        examples:
          application/json:
            {"error": "No promotions found for date: 2023-12-15"}
    """
    date = request.args.get('date')  # 獲取日期參數
    if not date:
        return jsonify({"error": "Date is required"}), 400

    # 使用 current_app 獲取資料庫會話
    db = current_app.extensions['sqlalchemy'].db

    query = """
        SELECT Store_Name, Name, Start_time, End_time, Method 
        FROM promotional_campaign 
        WHERE Start_time <= :date AND End_time >= :date;
    """
    results = db.session.execute(query, {"date": date}).fetchall()

    if not results:
        return jsonify({"error": f"No promotions found for date: {date}"}), 404

    # 將結果格式化為 JSON
    promotions = [
        {
            "store_name": row[0],
            "promotion_name": row[1],
            "start_time": row[2],
            "end_time": row[3],
            "method": row[4]
        }
        for row in results
    ]
    return jsonify(promotions)

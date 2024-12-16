from flask import Blueprint, jsonify, request, make_response, json
from models.models import db
from sqlalchemy import text

promotions_bp = Blueprint('promotions', __name__)

@promotions_bp.route('/promotions/shop', methods=['GET'])
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
              }
            ]
      400:
        description: 缺少參數或請求無效
        examples:
          application/json: {"error": "Shop name is required"}
    """
    try:
        shop_name = request.args.get('shop_name')
        if not shop_name:
            return jsonify({"error": "Shop name is required"}), 400

        query = text("""
            SELECT Name, Start_Time, End_Time, Method
            FROM Promotional_Campaign
            WHERE Store_Name = :shop_name;
        """)
        results = db.session.execute(query, {"shop_name": shop_name}).fetchall()

        promotions = []
        for row in results:
            promotions.append({
                "name": row[0],
                "start_time": str(row[1]),
                "end_time": str(row[2]),
                "method": row[3]
            })

        json_str = json.dumps(promotions, ensure_ascii=False)
        response = make_response(json_str, 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@promotions_bp.route('/promotions/method', methods=['GET'])
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
        description: 促銷方式 (例如 折扣促銷, 贈品優惠)
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
          application/json: {"error": "Promotion method is required"}
      404:
        description: 找不到促銷活動
        examples:
          application/json: {"error": "No promotions found for method: 折扣促銷"}
    """
    try:
        method = request.args.get('method')
        if not method:
            return jsonify({"error": "Promotion method is required"}), 400

        query = text("""
            SELECT Store_Name, Name, Start_Time, End_Time
            FROM Promotional_Campaign
            WHERE Method = :method;
        """)
        results = db.session.execute(query, {"method": method}).fetchall()

        if not results:
            return jsonify({"error": f"No promotions found for method: {method}"}), 404

        promotions = []
        for row in results:
            promotions.append({
                "store_name": row[0],
                "promotion_name": row[1],
                "start_time": str(row[2]),
                "end_time": str(row[3])
            })

        json_str = json.dumps(promotions, ensure_ascii=False)
        response = make_response(json_str, 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@promotions_bp.route('/promotions/date', methods=['GET'])
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
          application/json: {"error": "Date is required"}
      404:
        description: 找不到促銷活動
        examples:
          application/json: {"error": "No promotions found for date: 2023-12-15"}
    """
    try:
        input_date = request.args.get('date')
        if not input_date:
            return jsonify({"error": "Date is required"}), 400
        
        # 由於 Promotional_Campaign 表中 Start_Time / End_Time 為 DATETIME
        # 需要比較 input_date 是否落在 Start_Time 與 End_Time 之間
        # 一般作法：Start_Time <= input_date的結束時刻 (23:59:59)，End_Time >= input_date的開始時刻 (00:00:00)
        # SQL 可使用 between 或邏輯判斷
        date_start = f"{input_date} 00:00:00"
        date_end = f"{input_date} 23:59:59"

        query = text("""
            SELECT Store_Name, Name, Start_Time, End_Time, Method
            FROM Promotional_Campaign
            WHERE Start_Time <= :date_end
              AND End_Time >= :date_start;
        """)
        results = db.session.execute(query, {"date_start": date_start, "date_end": date_end}).fetchall()

        if not results:
            return jsonify({"error": f"No promotions found for date: {input_date}"}), 404

        promotions = []
        for row in results:
            promotions.append({
                "store_name": row[0],
                "promotion_name": row[1],
                "start_time": str(row[2]),
                "end_time": str(row[3]),
                "method": row[4]
            })

        json_str = json.dumps(promotions, ensure_ascii=False)
        response = make_response(json_str, 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
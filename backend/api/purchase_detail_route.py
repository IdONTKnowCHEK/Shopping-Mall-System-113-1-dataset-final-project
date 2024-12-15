from flask import Blueprint, jsonify, request, current_app

purchase_detail_bp = Blueprint('purchase_detail', __name__)

@purchase_detail_bp.route('/shop/purchase-details', methods=['GET'])
def get_purchase_details():
    """
    獲取指定店鋪的進貨明細
    ---
    tags:
      - Purchase Details API
    parameters:
      - name: shop_name
        in: query
        type: string
        required: true
        description: 店鋪名稱
    responses:
      200:
        description: 返回進貨明細列表
        examples:
          application/json:
            [
              {
                "serial_number": "1",
                "supplier": "義隆供應商",
                "time": "2023-03-01 12:35:09",
                "goods": "10Days 恬褋仕 柔眠枕(晨曦白)10cm",
                "amount": 14
              },
              {
                "serial_number": "2",
                "supplier": "順豐供應商",
                "time": "2023-03-02 14:15:00",
                "goods": "高級抗菌毛巾",
                "amount": 20
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
        SELECT serial_number, supplier, time, goods, amount
        FROM purchase_detail
        WHERE Store_name = :shop_name
    """

    # 執行 SQL 查詢並返回結果
    results = db.session.execute(query, {"shop_name": shop_name}).fetchall()

    # 將結果格式化為 JSON
    purchase_details = [
        {
            "serial_number": r[0],
            "supplier": r[1],
            "time": r[2],
            "goods": r[3],
            "amount": r[4]
        }
        for r in results
    ]

    return jsonify(purchase_details)

@purchase_detail_bp.route('/purchase-details-by-date', methods=['GET'])
def get_purchase_details_by_date():
    """
    查詢特定日期的進貨明細
    ---
    tags:
      - Purchase Details API
    parameters:
      - name: date
        in: query
        type: string
        required: true
    responses:
      200:
        description: 返回特定日期的進貨明細
        examples:
          application/json:
            [
              {
                "serial_number": "1",
                "store_name": "商店1",
                "supplier": "供應商A",
                "time": "2023-12-15 10:30:00",
                "goods": "商品A",
                "amount": 50
              },
              {
                "serial_number": "2",
                "store_name": "商店2",
                "supplier": "供應商B",
                "time": "2023-12-15 11:00:00",
                "goods": "商品B",
                "amount": 30
              }
            ]
      400:
        description: 缺少參數或請求無效
        examples:
          application/json:
            {"error": "Date is required"}
      404:
        description: 找不到進貨明細
        examples:
          application/json:
            {"error": "No purchase details found for date: 2023-12-15"}
    """
    date = request.args.get('date')  # 獲取日期參數
    if not date:
        return jsonify({"error": "Date is required"}), 400

    # 使用 current_app 獲取資料庫會話
    db = current_app.extensions['sqlalchemy'].db

    query = """
        SELECT serial_number, Store_name, supplier, time, goods, amount 
        FROM purchase_detail 
        WHERE DATE(time) = :date;
    """
    results = db.session.execute(query, {"date": date}).fetchall()

    if not results:
        return jsonify({"error": f"No purchase details found for date: {date}"}), 404

    # 將結果格式化為 JSON
    purchase_details = [
        {
            "serial_number": row[0],
            "store_name": row[1],
            "supplier": row[2],
            "time": row[3],
            "goods": row[4],
            "amount": row[5]
        }
        for row in results
    ]
    return jsonify(purchase_details)



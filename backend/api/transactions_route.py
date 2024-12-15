from flask import Blueprint, jsonify, request, current_app

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/transactions-by-date', methods=['GET'])
def get_transactions_by_date():
    """
    查詢特定日期的交易
    ---
    tags:
      - Transactions API
    parameters:
      - name: date
        in: query
        type: string
        required: true
    responses:
      200:
        description: 返回特定日期的交易記錄
        examples:
          application/json:
            [
              {
                "store_name": "商店1",
                "time": "2023-12-15 12:20:48",
                "price": 3590,
                "payment": "credit card"
              },
              {
                "store_name": "商店2",
                "time": "2023-12-15 14:00:12",
                "price": 1250,
                "payment": "cash"
              }
            ]
      400:
        description: 缺少參數或請求無效
        examples:
          application/json:
            {"error": "Date is required"}
      404:
        description: 找不到交易記錄
        examples:
          application/json:
            {"error": "No transactions found for date: 2023-12-15"}
    """
    date = request.args.get('date')  # 獲取日期參數
    if not date:
        return jsonify({"error": "Date is required"}), 400

    # 使用 current_app 獲取資料庫會話
    db = current_app.extensions['sqlalchemy'].db

    query = """
        SELECT Store_Name, time, Price, Payment 
        FROM shopping_sheet 
        WHERE DATE(time) = :date;
    """
    results = db.session.execute(query, {"date": date}).fetchall()

    if not results:
        return jsonify({"error": f"No transactions found for date: {date}"}), 404

    # 將結果格式化為 JSON
    transactions = [
        {
            "store_name": row[0],
            "time": row[1],
            "price": row[2],
            "payment": row[3]
        }
        for row in results
    ]
    return jsonify(transactions)

@transactions_bp.route('/transactions-by-payment', methods=['GET'])
def get_transactions_by_payment():
    """
    查詢特定付款方式的交易
    ---
    tags:
      - Transactions API
    parameters:
      - name: payment
        in: query
        type: string
        required: true
        description: 付款方式 (例如 credit card, cash)
    responses:
      200:
        description: 返回特定付款方式的交易記錄
        examples:
          application/json:
            [
              {
                "store_name": "商店1",
                "time": "2023-12-15 12:20:48",
                "price": 3590,
                "payment": "credit card"
              },
              {
                "store_name": "商店2",
                "time": "2023-12-15 14:00:12",
                "price": 1250,
                "payment": "credit card"
              }
            ]
      400:
        description: 缺少參數或請求無效
        examples:
          application/json:
            {"error": "Payment method is required"}
      404:
        description: 找不到交易記錄
        examples:
          application/json:
            {"error": "No transactions found for payment: credit card"}
    """
    payment = request.args.get('payment')  # 獲取付款方式參數
    if not payment:
        return jsonify({"error": "Payment method is required"}), 400

    # 使用 current_app 獲取資料庫會話
    db = current_app.extensions['sqlalchemy'].db

    query = """
        SELECT Store_Name, time, Price, Payment 
        FROM shopping_sheet 
        WHERE Payment = :payment;
    """
    results = db.session.execute(query, {"payment": payment}).fetchall()

    if not results:
        return jsonify({"error": f"No transactions found for payment: {payment}"}), 404

    # 將結果格式化為 JSON
    transactions = [
        {
            "store_name": row[0],
            "time": row[1],
            "price": row[2],
            "payment": row[3]
        }
        for row in results
    ]
    return jsonify(transactions)

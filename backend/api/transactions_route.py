from flask import Blueprint, jsonify, request, current_app, Response, make_response, json
from models.models import db
from sqlalchemy import text

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/transactions-by-date', methods=['GET'])
def get_transactions_by_date():
    """
    查詢特定日期的交易
    
    透過 query string 接收參數 date（格式 YYYY-MM-DD），自動組合出當天的起始與結束時間 (00:00:00 ~ 23:59:59)，
    並從 Shopping_Sheet 資料表中篩選所有落在該日期的交易記錄。

    ---
    tags:
      - Transactions API
    summary: "查詢特定日期的交易記錄"
    description: "依指定日期，回傳所有於該日期發生的交易，包含商店名稱、交易時間、金額與付款方式。"
    parameters:
      - name: date
        in: query
        type: string
        required: true
        description: "欲查詢的日期 (格式 YYYY-MM-DD)"
    responses:
      200:
        description: 成功返回該日期的交易記錄列表
        examples:
          application/json:
            [
              {
                "store_name": "商店1",
                "time": "2023-12-15 12:20:48",
                "price": 3590,
                "payment": "credit card"
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
        input_date = request.args.get('date')
        if not input_date:
            return jsonify({"error": "Date is required"}), 400
        
        # 組合當天的起止時間
        date_start = f"{input_date} 00:00:00"
        date_end = f"{input_date} 23:59:59"

        # Shopping_Sheet 表中包含交易紀錄
        query = text("""
            SELECT Store_Name, Time, Price, Payment
            FROM Shopping_Sheet
            WHERE Time BETWEEN :date_start AND :date_end
            ORDER BY Time;
        """)
        results = db.session.execute(query, {"date_start": date_start, "date_end": date_end}).fetchall()

        if not results:
            return jsonify({"error": f"No transactions found for date: {input_date}"}), 404

        transactions = []
        for row in results:
            transactions.append({
                "store_name": row[0],
                "time": str(row[1]),
                "price": float(row[2]),
                "payment": row[3]
            })

        json_str = json.dumps(transactions, ensure_ascii=False)
        response = make_response(json_str, 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@transactions_bp.route('/transactions-by-payment', methods=['GET'])
def get_transactions_by_payment():
    """
    查詢特定付款方式的交易

    透過 query string 接收參數 payment（例如 "credit card", "cash" 等），
    從 Shopping_Sheet 資料表中篩選對應付款方式的交易紀錄並按時間排序返回。

    ---
    tags:
      - Transactions API
    summary: "查詢指定付款方式的交易紀錄"
    description: "根據付款方式 (payment) 篩選 Shopping_Sheet 表中的交易記錄，若無查詢到符合條件的交易則回傳 404。"
    parameters:
      - name: payment
        in: query
        type: string
        required: true
        description: "付款方式 (例如 credit card, cash)"
    responses:
      200:
        description: 成功返回特定付款方式的交易記錄
        examples:
          application/json:
            [
              {
                "store_name": "商店1",
                "time": "2023-12-15 12:20:48",
                "price": 3590,
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
        payment = request.args.get('payment')
        if not payment:
            return jsonify({"error": "Payment method is required"}), 400
        
        query = text("""
            SELECT Store_Name, Time, Price, Payment
            FROM Shopping_Sheet
            WHERE Payment = :payment
            ORDER BY Time;
        """)
        results = db.session.execute(query, {"payment": payment}).fetchall()

        if not results:
            return jsonify({"error": f"No transactions found for payment: {payment}"}), 404

        transactions = []
        for row in results:
            transactions.append({
                "store_name": row[0],
                "time": str(row[1]),
                "price": float(row[2]),
                "payment": row[3]
            })

        json_str = json.dumps(transactions, ensure_ascii=False)
        response = make_response(json_str, 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
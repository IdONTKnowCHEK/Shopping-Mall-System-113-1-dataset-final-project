from flask import Blueprint, jsonify, request, current_app, Response, make_response, json
from models.models import db
from sqlalchemy import text

suppliers_bp = Blueprint('suppliers', __name__)

@suppliers_bp.route('/supplier', methods=['GET'])
def get_supplier_info():
    """
    取得供應商的詳細資訊
    
    根據 query string 接收的 supplier_name，從 Supplier 資料表中找出供應商的完整資料（名稱、地址、聯絡方式）。
    若找不到對應的供應商則回傳 404。
    
    ---
    tags:
      - Supplier API
    summary: "查詢供應商資訊"
    description: "透過 query string 接收一個必填參數 supplier_name，返回該供應商的詳細資訊（名稱、地址、聯絡方式等）。"
    parameters:
      - name: supplier_name
        in: query
        type: string
        required: true
        description: "供應商名稱"
    responses:
      200:
        description: 成功返回供應商的詳細資訊
        examples:
          application/json:
            {
              "name": "義隆供應商",
              "address": "台北市大安區忠孝東路一段100號",
              "contact": "02-12345678"
            }
      400:
        description: 缺少參數或請求無效
        examples:
          application/json: {"error": "Supplier name is required"}
      404:
        description: 找不到供應商
        examples:
          application/json: {"error": "Supplier not found"}
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
        supplier_name = request.args.get('supplier_name')
        if not supplier_name:
            return jsonify({"error": "Supplier name is required"}), 400

        query = text("""
            SELECT Name, Address, Contact
            FROM Supplier
            WHERE Name = :supplier_name;
        """)
        result = db.session.execute(query, {"supplier_name": supplier_name}).fetchone()

        if not result:
            return jsonify({"error": "Supplier not found"}), 404
        
        data = {
            "name": result[0],
            "address": result[1],
            "contact": result[2]
        }

        json_str = json.dumps(data, ensure_ascii=False)
        response = make_response(json_str, 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
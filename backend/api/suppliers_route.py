from flask import Blueprint, jsonify, request, current_app, Response, make_response, json
from models.models import db
from sqlalchemy import text

suppliers_bp = Blueprint('suppliers', __name__)

@suppliers_bp.route('/supplier', methods=['GET'])
def get_supplier_info():
    """
    獲取供應商的詳細資訊
    ---
    tags:
      - Supplier API
    parameters:
      - name: supplier_name
        in: query
        type: string
        required: true
        description: 供應商名稱
    responses:
      200:
        description: 返回供應商的詳細資訊
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
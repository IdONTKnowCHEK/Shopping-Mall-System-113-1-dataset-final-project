from flask import Blueprint, jsonify, request, current_app

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
    supplier_name = request.args.get('supplier_name')
    
    if not supplier_name:
        return jsonify({"error": "Supplier name is required"}), 400

    # 使用 current_app 獲取 SQLAlchemy 的資料庫會話
    db = current_app.extensions['sqlalchemy'].db

    query = """
        SELECT Name, Address, Contact
        FROM supplier
        WHERE Name = :supplier_name
    """

    # 執行 SQL 查詢
    result = db.session.execute(query, {"supplier_name": supplier_name}).fetchone()

    if not result:
        return jsonify({"error": "Supplier not found"}), 404

    # 格式化結果為 JSON
    supplier_info = {
        "name": result[0],
        "address": result[1],
        "contact": result[2]
    }

    return jsonify(supplier_info)

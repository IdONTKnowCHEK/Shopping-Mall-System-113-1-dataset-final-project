from flask import Blueprint, jsonify, request, current_app, Response, make_response, json
from models.models import db
from sqlalchemy import text

import json

branches_bp = Blueprint('branches', __name__)

@branches_bp.route('/branches', methods=['GET'])
def get_branches():
    """
    獲取所有分店名稱
    ---
    tags:
      - Branches API
    responses:
      200:
        description: 返回所有分店名稱列表
        examples:
          application/json:
            [
              "台北忠孝館",
              "台北復興館",
              "高雄店"
            ]
    """
    
    try:
        query = text("SELECT Branch_Name FROM Shopping_Mall;")
        results = db.session.execute(query).fetchall()

        branches = [row[0] for row in results]

        # 手動序列化確保不會轉成 \uXXXX
        json_str = json.dumps(branches, ensure_ascii=False)

        # 設定正確的 Content-Type 與 charset
        response = make_response(json_str, 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
    

@branches_bp.route('/branches/store', methods=['GET'])
def get_stores_by_branch():
    """
    根據分店名稱查詢商店
    ---
    tags:
      - Branches API
    parameters:
      - name: branch
        in: query
        type: string
        required: true
        description: 分店名稱
    responses:
      200:
        description: 返回指定分店的商店列表
        examples:
          application/json:
            [
              "商店1",
              "商店2",
              "商店3"
            ]
      400:
        description: 缺少參數或請求無效
        examples:
          application/json:
            {"error": "Branch name is required"}
    """
    try:
        # 從 query string 拿取分店名稱
        branch = request.args.get('branch')
        if not branch:
            return jsonify({"error": "Branch name is required"}), 400

        # 查詢對應分店的所有商店名稱
        query = text("""
            SELECT Store_Name
            FROM Shops
            WHERE Branch_Name = :branch;
        """)
        results = db.session.execute(query, {"branch": branch}).fetchall()

        store_list = [row[0] for row in results]

        # JSON 序列化
        json_str = json.dumps(store_list, ensure_ascii=False)
        response = make_response(json_str, 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
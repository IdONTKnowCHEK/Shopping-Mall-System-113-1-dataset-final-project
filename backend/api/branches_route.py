from flask import Blueprint, jsonify, request, current_app, Response, make_response, json
from models.models import db
from sqlalchemy import text

import json

branches_bp = Blueprint('branches', __name__)

@branches_bp.route('/branches', methods=['GET'])
def get_branches():
    """
    取得所有分店名稱
    
    從 Shopping_Mall 資料表中查詢所有 Branch_Name，並以 JSON 清單形式返回。
    
    ---
    tags:
      - Branches API
    summary: "取得所有分店名稱"
    description: "從資料庫 Shopping_Mall 表中選取所有分店名稱（Branch_Name）並以 JSON 格式返回。"
    responses:
      200:
        description: 成功返回所有分店名稱列表
        examples:
          application/json:
            [
              "台北忠孝館",
              "台北復興館",
              "高雄店"
            ]
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
    
    從 Shops 資料表中查詢指定分店（Branch_Name）所屬的商店名稱清單，並以 JSON 格式返回。
    
    ---
    tags:
      - Branches API
    summary: "根據分店名稱查詢商店"
    description: "透過 query string 接收一個 branch 參數（必填），查詢其對應的商店名稱列表。"
    parameters:
      - name: branch
        in: query
        type: string
        required: true
        description: 分店名稱
    responses:
      200:
        description: 成功返回指定分店的商店列表
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
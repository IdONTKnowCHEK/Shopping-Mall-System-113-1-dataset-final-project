from flask import Blueprint, jsonify, request, current_app, Response, make_response
from models.models import db
from sqlalchemy import text

import json

stores_bp = Blueprint('stores', __name__)

@stores_bp.route('/top-stores', methods=['GET'])
def get_top_stores():
    """
    獲取營業額最高的 10 家商店
    ---
    tags:
      - Revenue API
    responses:
      200:
        description: 返回營業額前 10 名的商店資訊
        examples:
          application/json:
            [
              {
                "rank": 1,
                "store_name": "台北忠孝館",
                "revenue": 1000000
              },
              {
                "rank": 2,
                "store_name": "台北復興館",
                "revenue": 800000
              }
            ]
    """

    query = text("""
        SELECT RANK() OVER (ORDER BY SUM(Price) DESC) AS RANK, Store_Name, SUM(Price) AS Revenue
        FROM shopping_sheet
        GROUP BY Store_Name
        ORDER BY RANK
        LIMIT 10;
    """)

    results = db.session.execute(query).fetchall()

    # 將結果轉為 JSON 格式
    top_stores = [
        {"rank": row[0], "store_name": row[1], "revenue": row[2]}
        for row in results
    ]
    return jsonify(top_stores)

@stores_bp.route('/stores', methods=['GET'])
def get_stores():
    """
    獲取所有商店名稱
    ---
    tags:
      - Stores API
    responses:
      200:
        description: 返回所有商店名稱列表
        examples:
          application/json:
            [
              "商店1",
              "商店2",
              "商店3"
            ]
    """
    # 使用 current_app 獲取資料庫會話
    db = current_app.extensions['sqlalchemy'].db

    query = "SELECT Store_Name FROM shops;"
    results = db.session.execute(query).fetchall()

    # 將商店名稱整理為 JSON 格式
    stores = [row[0] for row in results]
    return jsonify(stores)

@stores_bp.route('/branch-stores', methods=['GET'])
def get_stores_by_branch():
    """
    根據分店名稱查詢商店
    ---
    tags:
      - Stores API
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
    branch = request.args.get('branch')  # 獲取分店名稱參數
    if not branch:
        return jsonify({"error": "Branch name is required"}), 400

    # 使用 current_app 獲取資料庫會話
    db = current_app.extensions['sqlalchemy'].db

    query = "SELECT Store_Name FROM shops WHERE Branch_Name = :branch;"
    results = db.session.execute(query, {"branch": branch}).fetchall()

    # 將商店名稱整理為 JSON 格式
    stores = [row[0] for row in results]
    return jsonify(stores)

@stores_bp.route('/branches', methods=['GET'])
def get_branches():
    """
    獲取所有分店名稱
    ---
    tags:
      - Stores API
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


@stores_bp.route('/branch-revenue', methods=['GET'])
def get_branch_revenue():
    """
    獲取指定分店的總營業額
    ---
    tags:
      - Revenue API
    parameters:
      - name: branch
        in: query
        type: string
        required: true
        description: 分店名稱
    responses:
      200:
        description: 返回分店的總營業額
        examples:
          application/json:
            {
              "branch_name": "台北忠孝館",
              "total_revenue": 1000000
            }
      400:
        description: 缺少參數或請求無效
        examples:
          application/json:
            {"error": "Branch name is required"}
    """
    branch = request.args.get('branch')  # 獲取分店名稱參數
    if not branch:
        return jsonify({"error": "Branch name is required"}), 400

    # 使用 current_app 獲取資料庫會話
    db = current_app.extensions['sqlalchemy'].db

    query = """
        SELECT shops.Branch_Name, SUM(shopping_sheet.Price) AS SUM_Price
        FROM shopping_sheet
        JOIN shops ON shopping_sheet.Store_Name = shops.Store_Name
        WHERE shops.Branch_Name = :branch
        GROUP BY shops.Branch_Name;
    """
    result = db.session.execute(query, {"branch": branch}).fetchone()

    if not result:
        return jsonify

@stores_bp.route('/branch-stores-revenue', methods=['GET'])
def get_branch_stores_revenue():
    """
    獲取指定分店內商店的營業額排名
    ---
    tags:
      - Revenue API
    parameters:
      - name: branch
        in: query
        type: string
        required: true
        description: 分店名稱
    responses:
      200:
        description: 返回分店內商店的營業額排名
        examples:
          application/json:
            [
              {
                "rank": 1,
                "store_name": "商店1",
                "revenue": 500000
              },
              {
                "rank": 2,
                "store_name": "商店2",
                "revenue": 300000
              }
            ]
      400:
        description: 缺少參數或請求無效
        examples:
          application/json:
            {"error": "Branch name is required"}
      404:
        description: 找不到營業額數據
        examples:
          application/json:
            {"error": "No revenue data found for branch: 台北忠孝館"}
    """
    branch = request.args.get('branch')  # 獲取分店名稱參數
    if not branch:
        return jsonify({"error": "Branch name is required"}), 400

    # 使用 current_app 獲取資料庫會話
    db = current_app.extensions['sqlalchemy'].db

    query = """
        SELECT RANK() OVER (ORDER BY SUM(Price) DESC) AS RANK, shops.Store_Name, SUM(Price)
        FROM shopping_sheet
        JOIN shops ON shops.Store_Name = shopping_sheet.Store_Name
        WHERE Branch_Name = :branch
        GROUP BY shops.Store_Name
        ORDER BY RANK;
    """
    results = db.session.execute(query, {"branch": branch}).fetchall()

    if not results:
        return jsonify({"error": f"No revenue data found for branch: {branch}"}), 404

    # 將結果格式化為 JSON
    revenue_ranking = [
        {"rank": row[0], "store_name": row[1], "revenue": row[2]}
        for row in results
    ]
    return jsonify(revenue_ranking)
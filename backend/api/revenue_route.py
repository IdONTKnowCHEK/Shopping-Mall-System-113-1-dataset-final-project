from flask import Blueprint, jsonify, request, current_app, Response, make_response, json
from models.models import db
from sqlalchemy import text

import json

revenue_bp = Blueprint('revenue', __name__)


@revenue_bp.route('/revenue/top-stores', methods=['GET'])
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
                "store_name": "台隆手創館_廣三門市",
                "revenue": 3590.00
              },
              {
                "rank": 2,
                "store_name": "BIG TRAIN_新竹店",
                "revenue": 1890.00
              }
            ]
    """
    try:
        # 針對 Shopping_Sheet 統計各家商店總營業額，並選取前 10 名
        query = text("""
            SELECT Store_Name, SUM(Price) AS revenue
            FROM Shopping_Sheet
            GROUP BY Store_Name
            ORDER BY revenue DESC
            LIMIT 10;
        """)
        results = db.session.execute(query).fetchall()

        top_stores = []
        rank = 1
        for row in results:
            store_name = row[0]
            revenue = float(row[1])
            top_stores.append({
                "rank": rank,
                "store_name": store_name,
                "revenue": revenue
            })
            rank += 1

        # 轉成 JSON 字串並確保中文正常顯示
        json_str = json.dumps(top_stores, ensure_ascii=False)

        # 設定正確的 Content-Type 與 charset
        response = make_response(json_str, 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@revenue_bp.route('/revenue/branch', methods=['GET'])
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
    try:
        branch = request.args.get('branch')
        if not branch:
            return jsonify({"error": "Branch name is required"}), 400

        # 統計該分店（Branch_Name）底下所有商店的總營業額
        query = text("""
            SELECT SM.Branch_Name, SUM(SS.Price) AS total_revenue
            FROM Shopping_Sheet SS
            JOIN Shops S ON SS.Store_Name = S.Store_Name
            JOIN Shopping_Mall SM ON S.Branch_Name = SM.Branch_Name
            WHERE SM.Branch_Name = :branch
            GROUP BY SM.Branch_Name;
        """)
        result = db.session.execute(query, {"branch": branch}).fetchone()

        if result and result[1] is not None:
            data = {
                "branch_name": result[0],
                "total_revenue": float(result[1])
            }
        else:
            # 如果沒查到任何資料，可視需求回傳 0 或直接回傳空值
            data = {
                "branch_name": branch,
                "total_revenue": 0
            }

        json_str = json.dumps(data, ensure_ascii=False)
        response = make_response(json_str, 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@revenue_bp.route('/revenue/branch/stores', methods=['GET'])
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
                "store_name": "BIG TRAIN_新竹店",
                "revenue": 1890
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
    
    try:
        branch = request.args.get('branch')
        if not branch:
            return jsonify({"error": "Branch name is required"}), 400

        # 查詢該分店內所有商店的營業額，並依照營業額降序排序
        query = text("""
            SELECT S.Store_Name, COALESCE(SUM(SS.Price), 0) AS revenue
            FROM Shops S
            LEFT JOIN Shopping_Sheet SS ON S.Store_Name = SS.Store_Name
            WHERE S.Branch_Name = :branch
            GROUP BY S.Store_Name
            ORDER BY revenue DESC;
        """)
        results = db.session.execute(query, {"branch": branch}).fetchall()

        if not results:
            return jsonify({"error": f"No revenue data found for branch: {branch}"}), 404

        # 整理排名格式
        store_revenue_list = []
        rank = 1
        for row in results:
            store_name = row[0]
            revenue = float(row[1])
            store_revenue_list.append({
                "rank": rank,
                "store_name": store_name,
                "revenue": revenue
            })
            rank += 1

        # 如果 revenue 全部都是 0，視需求也可以回傳 404 或是回傳 rank list
        # 這裡範例：若找到店家但營業額都為 0，仍回傳空排名結果即可

        json_str = json.dumps(store_revenue_list, ensure_ascii=False)
        response = make_response(json_str, 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
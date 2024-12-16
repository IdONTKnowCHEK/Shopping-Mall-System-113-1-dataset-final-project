from flask import Blueprint, jsonify, request, current_app, Response, make_response, json
from models.models import db
from sqlalchemy import text

import json

stores_bp = Blueprint('stores', __name__)


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
              "台隆手創館_廣三門市",
              "BIG TRAIN_新竹店"
            ]
    """
    try:
        # 從 Shops 資料表選取 Store_Name 欄位
        query = text("SELECT Store_Name FROM Shops;")
        results = db.session.execute(query).fetchall()

        # 將 SQL 查詢結果整理成 list
        store_names = [row[0] for row in results]

        # 序列化為 JSON 並確保中文正常顯示
        json_str = json.dumps(store_names, ensure_ascii=False)

        # 以 make_response 設定正確的 Content-Type 與 charset
        response = make_response(json_str, 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
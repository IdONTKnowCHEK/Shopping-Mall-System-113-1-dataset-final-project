from flask import Blueprint, jsonify, request, make_response, json
from models.models import db
from sqlalchemy import text


employees_bp = Blueprint('employees', __name__)

@employees_bp.route('/shop/employees', methods=['GET'])
def get_shop_employees():
    """
    獲取指定店鋪的員工列表
    ---
    tags:
      - Employees API
    parameters:
      - name: shop_name
        in: query
        type: string
        required: true
        description: 店鋪名稱
    responses:
      200:
        description: 返回員工列表
        examples:
          application/json:
            [
              {
                "name": "陳家琪",
                "contact": "0932-425789",
                "position": "店長",
                "working_hours": "11:00~21:30"
              }
            ]
      400:
        description: 店鋪名稱缺失或請求無效
        examples:
          application/json: {"error": "Shop name is required"}
    """
    try:
        shop_name = request.args.get('shop_name')
        if not shop_name:
            return jsonify({"error": "Shop name is required"}), 400

        query = text("""
            SELECT Name, Contact, Position, Shift_Time
            FROM Shop_Employee
            WHERE Store_Name = :shop_name;
        """)
        results = db.session.execute(query, {"shop_name": shop_name}).fetchall()

        employee_list = []
        for row in results:
            employee_list.append({
                "name": row[0],
                "contact": row[1],
                "position": row[2],
                # working_hours 命名可自行調整
                "working_hours": row[3]  
            })

        json_str = json.dumps(employee_list, ensure_ascii=False)
        response = make_response(json_str, 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@employees_bp.route('/shop/employees/time', methods=['GET'])
def get_employees_by_time():
    """
    獲取特定時間正在工作的員工
    ---
    tags:
      - Employees API
    parameters:
      - name: shop_name
        in: query
        type: string
        required: true
        description: 店鋪名稱
      - name: time
        in: query
        type: string
        required: true
        description: 查詢的時間（格式建議 HH:MM）
    responses:
      200:
        description: 返回正在工作的員工列表
        examples:
          application/json:
            [
              {
                "name": "陳家琪",
                "contact": "0932-425789",
                "position": "店長"
              }
            ]
      400:
        description: 缺少參數或請求無效
        examples:
          application/json: {"error": "Shop name and time are required"}
    """
    try:
        shop_name = request.args.get('shop_name')
        query_time = request.args.get('time')  # 假設格式為 HH:MM，例如 '14:30'
        if not shop_name or not query_time:
            return jsonify({"error": "Shop name and time are required"}), 400

        # 查詢該店鋪下的所有員工
        query = text("""
            SELECT Name, Contact, Position, Shift_Time
            FROM Shop_Employee
            WHERE Store_Name = :shop_name;
        """)
        results = db.session.execute(query, {"shop_name": shop_name}).fetchall()

        # 將 query_time（HH:MM）轉為以分鐘計算，方便比對
        def time_to_minutes(t):
            h, m = t.split(":")
            return int(h)*60 + int(m)

        query_minutes = time_to_minutes(query_time)
        
        working_employees = []
        for row in results:
            name, contact, position, shift_str = row
            # 假設 shift_str 格式為 'HH:MM-HH:MM'
            # 例如 '9:00-16:30'
            if shift_str and '-' in shift_str:
                start_str, end_str = shift_str.split('-')
                start_minutes = time_to_minutes(start_str)
                end_minutes = time_to_minutes(end_str)
                
                # 簡化判斷：query_minutes 介於 start_minutes 與 end_minutes 之間
                # 若跨天班表（例如 22:00-06:00）則需更複雜處理，這裡僅示範一般情況。
                if start_minutes <= query_minutes <= end_minutes:
                    working_employees.append({
                        "name": name,
                        "contact": contact,
                        "position": position
                    })

        json_str = json.dumps(working_employees, ensure_ascii=False)
        response = make_response(json_str, 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@employees_bp.route('/branch/employees', methods=['GET'])
def get_branch_employees():
    """
    獲取指定分店的員工資料
    ---
    tags:
      - Employees API
    parameters:
      - name: branch
        in: query
        type: string
        required: true
        description: 分店名稱
    responses:
      200:
        description: 返回分店的員工資料列表
        examples:
          application/json:
            [
              {
                "name": "陳智偉",
                "contact": "0966-466166",
                "position": "店長",
                "start_work_time": "11:00",
                "end_work_time": "21:30"
              }
            ]
      400:
        description: 缺少參數或請求無效
        examples:
          application/json:
            {"error": "Branch name is required"}
      404:
        description: 找不到員工資料
        examples:
          application/json:
            {"error": "No employee data found for branch: 台北忠孝館"}
    """
    try:
        branch = request.args.get('branch')
        if not branch:
            return jsonify({"error": "Branch name is required"}), 400

        query = text("""
            SELECT Name, Contact, Position, Shift_Time
            FROM Mall_Employee
            WHERE Branch_Name = :branch;
        """)
        results = db.session.execute(query, {"branch": branch}).fetchall()

        if not results:
            return jsonify({"error": f"No employee data found for branch: {branch}"}), 404

        employees = []
        for row in results:
            name, contact, position, shift_str = row
            # 分割 Shift_Time，假設格式為 '11:00-21:30'
            start_work_time, end_work_time = '', ''
            if shift_str and '-' in shift_str:
                start_work_time, end_work_time = shift_str.split('-')

            employees.append({
                "name": name,
                "contact": contact,
                "position": position,
                "start_work_time": start_work_time,
                "end_work_time": end_work_time
            })

        json_str = json.dumps(employees, ensure_ascii=False)
        response = make_response(json_str, 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@employees_bp.route('/position-employees', methods=['GET'])
def get_position_employees():
    """
    獲取指定職位的員工資料
    ---
    tags:
      - Employees API
    parameters:
      - name: position
        in: query
        type: string
        required: true
        description: 職位名稱
    responses:
      200:
        description: 返回指定職位的員工資料列表
        examples:
          application/json:
            [
              {
                "name": "陳家琪",
                "contact": "0932-425789",
                "work_time": "11:00~21:30",
                "location": "台北忠孝館"
              }
            ]
      400:
        description: 缺少參數或請求無效
        examples:
          application/json:
            {"error": "Position is required"}
      404:
        description: 找不到員工資料
        examples:
          application/json:
            {"error": "No employee data found for position: 店長"}
    """
    try:
        position = request.args.get('position')
        if not position:
            return jsonify({"error": "Position is required"}), 400

        # 在兩張表中查詢相同職位的員工：Mall_Employee & Shop_Employee
        # 注意：Shift_Time 命名一致，但位置欄位在 Mall_Employee 是 Branch_Name，而在 Shop_Employee 是 Store_Name。
        # 可使用 UNION ALL 將兩邊資料合併，最後用同一結構回傳。
        query = text("""
            SELECT Name, Contact, Position, Shift_Time, Branch_Name AS location, 'mall' AS source
            FROM Mall_Employee
            WHERE Position = :pos

            UNION ALL

            SELECT Name, Contact, Position, Shift_Time, Store_Name AS location, 'shop' AS source
            FROM Shop_Employee
            WHERE Position = :pos;
        """)
        results = db.session.execute(query, {"pos": position}).fetchall()

        if not results:
            return jsonify({"error": f"No employee data found for position: {position}"}), 404

        employees = []
        for row in results:
            name, contact, pos, shift_time, location, source = row
            employees.append({
                "name": name,
                "contact": contact,
                "work_time": shift_time,
                "location": location
            })

        json_str = json.dumps(employees, ensure_ascii=False)
        response = make_response(json_str, 200)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

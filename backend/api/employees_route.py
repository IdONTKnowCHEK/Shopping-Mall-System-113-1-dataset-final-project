from flask import Blueprint, jsonify, request, make_response, json
from models.models import db
from sqlalchemy import text


employees_bp = Blueprint('employees', __name__)

@employees_bp.route('/employees/shop', methods=['GET'])
def get_shop_employees():
    """
    取得指定店鋪的員工列表
    
    從 Shop_Employee 資料表中查詢所有屬於指定店鋪 (Store_Name) 的員工資訊，並返回 JSON 清單。
    
    ---
    tags:
      - Employees API
    summary: "取得指定店鋪的員工列表"
    description: "透過 query string 接收參數 shop_name，查詢對應店鋪的員工資料，包含姓名、連絡方式、職位、排班時段等。"
    parameters:
      - name: shop_name
        in: query
        type: string
        required: true
        description: 店鋪名稱
    responses:
      200:
        description: 成功返回員工列表
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
          application/json:
            {"error": "Shop name is required"}
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
        shop_name = request.args.get('shop_name')
        if not shop_name:
            return jsonify({"error": "Shop name is required"}), 400

        # 查詢該店鋪下的所有員工
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


@employees_bp.route('/employees/shop/time', methods=['GET'])
def get_employees_by_time():
    """
    取得特定時間正在工作的員工

    透過 query string 接收兩個參數：
    - shop_name：店鋪名稱
    - time：查詢的時間（建議格式 HH:MM）

    系統會從 Shop_Employee 表取得該店鋪下所有員工的排班資訊，並判斷指定時間點是否落在員工的班表區間。如果員工當前正在上班，便將其資訊（姓名、聯絡方式、職位等）返回。

    ---
    tags:
      - Employees API
    summary: "依據店鋪名稱與時間，查詢正在工作的員工"
    description: "判斷員工排班時段與指定時間（HH:MM）間的關係，返回符合條件的員工清單。"
    parameters:
      - name: shop_name
        in: query
        type: string
        required: true
        description: "店鋪名稱"
      - name: time
        in: query
        type: string
        required: true
        description: "查詢的時間（格式 HH:MM）"
    responses:
      200:
        description: 成功返回正在工作的員工列表
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
          application/json:
            {"error": "Shop name and time are required"}
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


@employees_bp.route('/employees/branch', methods=['GET'])
def get_branch_employees():
    """
    取得指定分店的員工資料
    
    從 Mall_Employee 資料表中查詢指定分店 (Branch_Name) 的員工資訊，並返回 JSON 清單。
    Shift_Time 以「start_work_time - end_work_time」的格式呈現，例如「11:00 - 21:30」。
    
    ---
    tags:
      - Employees API
    summary: "取得指定分店的員工資料"
    description: "透過 query string 接收參數 branch，查詢該分店所屬的員工，包括姓名、聯絡方式、職位與上下班時間。"
    parameters:
      - name: branch
        in: query
        type: string
        required: true
        description: 分店名稱
    responses:
      200:
        description: 成功返回分店員工資料列表
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
        branch = request.args.get('branch')
        if not branch:
            return jsonify({"error": "Branch name is required"}), 400

        # 查詢該分店下的所有員工
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


@employees_bp.route('/employees/position', methods=['GET'])
def get_position_employees():
    """
    取得指定職位的員工資料
    
    從 Mall_Employee 與 Shop_Employee 資料表查詢指定職位 (Position) 的所有員工，並將兩者合併後返回 JSON 清單。
    為了區分不同來源（分店員工或店舖員工），可在回傳結構中加入來源欄位（如 source），或依需求整併顯示。
    
    ---
    tags:
      - Employees API
    summary: "取得指定職位的員工資料"
    description: "透過 query string 接收參數 position，從 Mall_Employee 與 Shop_Employee 各自找出符合該職位的員工，並返回統一格式的 JSON 資料。"
    parameters:
      - name: position
        in: query
        type: string
        required: true
        description: 職位名稱
    responses:
      200:
        description: 成功返回指定職位的員工資料列表
        examples:
          application/json:
            [
              {
                "name": "陳家琪",
                "contact": "0932-425789",
                "work_time": "11:00-21:30",
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
        position = request.args.get('position')
        if not position:
            return jsonify({"error": "Position is required"}), 400

        # UNION Mall_Employee 與 Shop_Employee 兩個資料表
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

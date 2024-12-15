from flask import Blueprint, jsonify, request, current_app

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
              },
              {
                "name": "王小明",
                "contact": "0987-654321",
                "position": "員工",
                "working_hours": "09:00~18:00"
              }
            ]
      400:
        description: 店鋪名稱缺失或請求無效
        examples:
          application/json: {"error": "Shop name is required"}
    """
    shop_name = request.args.get('shop_name')
    if not shop_name:
        return jsonify({"error": "Shop name is required"}), 400

    db = current_app.extensions['sqlalchemy'].db

    query = """
        SELECT Name, contact, Position, CONCAT(Start_work_time, '~', End_work_time) AS working_hours
        FROM shop_employee 
        WHERE store_name = :shop_name
    """

    results = db.session.execute(query, {"shop_name": shop_name}).fetchall()

    employees = [
        {
            "name": r[0],
            "contact": r[1],
            "position": r[2],
            "working_hours": r[3]
        }
        for r in results
    ]

    return jsonify(employees)
  
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
              },
              {
                "name": "王小明",
                "contact": "0987-654321",
                "position": "員工"
              }
            ]
      400:
        description: 缺少參數或請求無效
        examples:
          application/json: {"error": "Shop name and time are required"}
    """
    shop_name = request.args.get('shop_name')
    time = request.args.get('time')

    if not shop_name or not time:
        return jsonify({"error": "Shop name and time are required"}), 400

    db = current_app.extensions['sqlalchemy'].db

    query = """
        SELECT Name, contact, Position 
        FROM shop_employee 
        WHERE store_name = :shop_name 
        AND :time >= Start_work_time 
        AND End_work_time >= :time
    """

    # 執行 SQL 查詢並返回結果
    results = db.session.execute(query, {"shop_name": shop_name, "time": time}).fetchall()

    # 將結果格式化為 JSON
    employees = [
        {
            "name": r[0],
            "contact": r[1],
            "position": r[2]
        }
        for r in results
    ]

    return jsonify(employees)

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
              },
              {
                "name": "林怡如",
                "contact": "0912-345678",
                "position": "兼職人員",
                "start_work_time": "09:00",
                "end_work_time": "16:30"
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
    branch = request.args.get('branch')  # 獲取分店名稱參數
    if not branch:
        return jsonify({"error": "Branch name is required"}), 400

    # 使用 current_app 獲取資料庫會話
    db = current_app.extensions['sqlalchemy'].db

    query = """
        SELECT Name, contact, Position, Start_work_time, End_work_time
        FROM mall_employee
        WHERE Branch_Name = :branch;
    """
    results = db.session.execute(query, {"branch": branch}).fetchall()

    if not results:
        return jsonify({"error": f"No employee data found for branch: {branch}"}), 404

    # 將結果格式化為 JSON
    employees = [
        {
            "name": row[0],
            "contact": row[1],
            "position": row[2],
            "start_work_time": row[3],
            "end_work_time": row[4]
        }
        for row in results
    ]
    return jsonify(employees)

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
              },
              {
                "name": "林士昇",
                "contact": "0966-487512",
                "work_time": "09:00~18:00",
                "location": "新竹店"
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
    position = request.args.get('position')  # 獲取職位名稱參數
    if not position:
        return jsonify({"error": "Position is required"}), 400

    # 使用 current_app 獲取資料庫會話
    db = current_app.extensions['sqlalchemy'].db

    # 查詢分店員工
    query_mall = """
        SELECT Name, contact, Start_work_time, End_work_time, Branch_Name
        FROM mall_employee
        WHERE Position = :position;
    """
    mall_results = db.session.execute(query_mall, {"position": position}).fetchall()

    # 查詢商店員工
    query_shop = """
        SELECT Name, contact, Start_work_time, End_work_time, Store_Name
        FROM shop_employee
        WHERE Position = :position;
    """
    shop_results = db.session.execute(query_shop, {"position": position}).fetchall()

    # 合併結果
    results = mall_results + shop_results

    if not results:
        return jsonify({"error": f"No employee data found for position: {position}"}), 404

    # 格式化結果為 JSON
    employees = [
        {
            "name": row[0],
            "contact": row[1],
            "work_time": f"{row[2]}~{row[3]}",
            "location": row[4]
        }
        for row in results
    ]
    return jsonify(employees)


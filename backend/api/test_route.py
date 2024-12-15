from flask import Blueprint, request, jsonify

test_bp = Blueprint("test", __name__)  # 定義 Blueprint
base_url = "/api/test/"  # 定義路由前綴

@test_bp.route(base_url+'add', methods=['POST'])
def add_numbers():
    """
    計算兩個數字的和
    ---
    tags:
      - Test API
    parameters:
      - name: num1
        in: formData
        type: number
        required: true
        description: 第一個數字
      - name: num2
        in: formData
        type: number
        required: true
        description: 第二個數字
    responses:
      200:
        description: 返回加總結果
        examples:
          application/json: {"result": 3}
      400:
        description: 無效請求
    """
    try:
        # 獲取表單中的參數
        num1 = float(request.form.get("num1"))
        num2 = float(request.form.get("num2"))
        return jsonify({"result": num1 + num2})
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input"}), 400

@test_bp.route(base_url+'sub', methods=['POST'])
def sub_numbers():
    """
    計算兩個數字的差
    ---
    tags:
      - Test API
    parameters:
      - name: num1
        in: formData
        type: number
        required: true
        description: 第一個數字
      - name: num2
        in: formData
        type: number
        required: true
        description: 第二個數字
    responses:
      200:
        description: 返回加總結果
        examples:
          application/json: {"result": 3}
      400:
        description: 無效請求
    """
    try:
        # 獲取表單中的參數
        num1 = float(request.form.get("num1"))
        num2 = float(request.form.get("num2"))
        return jsonify({"result": num1 - num2})
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input"}), 400
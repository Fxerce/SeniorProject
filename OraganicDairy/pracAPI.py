from flask import Flask, request, jsonify, send_file
import qrcode
from barcode import Code128
from barcode.writer import ImageWriter
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/generate', methods=['POST'])
def generate_codes():
    try:
        # รับข้อมูลจาก Request
        data = request.json
        product_id = data.get('product_id')
        milk_tank_number = data.get('milk_tank_number')

        # ตรวจสอบข้อมูลที่จำเป็น
        if not product_id or not milk_tank_number:
            return jsonify({"error": "Missing product_id or milk_tank_number"}), 400

        # สร้าง QR Code
        qr_data = f"ProductID: {product_id}, MilkTank: {milk_tank_number}"
        qr = qrcode.make(qr_data)
        qr_filename = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_qrcode.png")
        qr.save(qr_filename)

        # สร้าง Barcode
        barcode_data = f"{product_id}-{milk_tank_number}"
        barcode = Code128(barcode_data, writer=ImageWriter())
        barcode_filename = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_barcode.png")
        barcode.save(barcode_filename)

        # ส่ง URL ของไฟล์ที่สร้างกลับไป
        return jsonify({
            "qr_code_url": qr_filename,
            "barcode_url": barcode_filename
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename))

if __name__ == "__main__":
    app.run(debug=True)

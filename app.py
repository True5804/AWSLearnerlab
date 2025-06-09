from flask import Flask, request, jsonify, send_file,render_template
import mysql.connector
import json
import bcrypt
import datetime

app = Flask(__name__)

db = mysql.connector.connect(
    host="awslabdb.cemubq89koh0.us-east-1.rds.amazonaws.com",          
    port = 3306,
    user="admin",      
    password= "Nutncsie123",  
    database = "labdb"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin_panel():
    return render_template('Admin.html')

@app.route('/supplier')
def supplier_panel():
    return render_template('Supplier.html')

@app.route('/hospital')
def hospital_panel():
    return render_template('hospital.html')

@app.route('/suppliers')
def view_suppliers():
    return render_template('view_suppliers.html')

@app.route('/hospitals')
def view_hospitals():
    return render_template('view_hospitals.html')

@app.route('/track')
def track():
    return render_template('track.html')

@app.route('/api/suppliers')
def get_suppliers():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT supplier_name, tel_number, add_time FROM suppliers")
    suppliers = cursor.fetchall()
    cursor.close()
    return jsonify(suppliers)

@app.route('/api/add_supplier', methods=['POST'])
def add_supplier():
    data = request.json
    name = data.get('supplierName')
    phone = data.get('supplierPhone')
    username = data.get('username')
    password = data.get('password')

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    cursor = db.cursor()
    cursor.execute("INSERT INTO suppliers (supplier_name, tel_number, add_time) VALUES (%s, %s, %s)",
                   (name, phone, now))
    cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, 'supplier')",
                   (username, hashed_pw))
    db.commit()
    cursor.close()
    return jsonify({"status": "supplier and account added"})

@app.route('/api/hospitals')
def get_hospitals():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT hospital_name, hospital_address, tel_number, add_time FROM hospitals")
    hospitals = cursor.fetchall()
    cursor.close()
    return jsonify(hospitals)

@app.route('/api/add_hospital', methods=['POST'])
def add_hospital():
    data = request.json
    hospital_address = data.get('hospitalAddress')
    name = data.get('hospitalName')
    phone = data.get('hospitalPhone')
    username = data.get('username')
    password = data.get('password')

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    cursor = db.cursor()
    cursor.execute("INSERT INTO hospitals (hospital_name, hospital_address, tel_number, add_time) VALUES (%s, %s, %s, %s)",
                   (name, hospital_address, phone, now))
    cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, 'hospital')",
                   (username, hashed_pw))
    db.commit()
    cursor.close()
    return jsonify({"status": "hospital and account added"})

@app.route('/api/donors')
def api_get_donors():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM donors")
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows)

@app.route('/api/add_donor', methods=['POST'])
def api_add_donor():
    data = request.json
    cursor = db.cursor()
    sql = """
        INSERT INTO donors (donorName, age, gender, phone_number, bloodGroup, bloodVolume, donatedTime)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data['donorName'],
        int(data['age']),
        data['gender'],
        data['phone_number'],
        data['bloodGroup'],
        int(data['bloodVolume']),
        data['donatedTime']
    )

    cursor.execute("""
        INSERT INTO blood (blood_group, donor_name, volume, status)
        VALUES (%s, %s, %s, 'Active')
    """, (data['bloodGroup'], data['donorName'], int(data['bloodVolume'])))
    
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    return jsonify(success=True, message="✅ Donor and blood added")


@app.route('/api/patients')
def api_get_patients():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows)

@app.route('/api/add_patient', methods=['POST'])
def add_patient():
    data = request.json
    blood_id = data['usedBloodId']
    blood_group = data['bloodGroup']

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM blood WHERE id = %s", (blood_id,))
    blood = cursor.fetchone()

    if not blood:
        return jsonify(success=False, message="❌ Blood ID not found")
    if blood['status'] != 'Fulfilled':
        return jsonify(success=False, message="⛔ Blood not yet marked as Fulfilled")
    if blood['blood_group'] != blood_group:
        return jsonify(success=False, message="❌ Blood group mismatch")

    cursor.execute("""
        INSERT INTO patients (patientName, age, gender, phone_number, bloodGroup, bloodVolume, usedBloodId, usedTime)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data['patientName'], data['age'], data['gender'], data['phone_number'],
        data['bloodGroup'], data['bloodVolume'], blood_id, data['usedTime']
    ))

    db.commit()
    cursor.close()
    return jsonify(success=True, message="✅ Patient registered and blood used")

@app.route('/api/request_blood', methods=['POST'])
def request_blood():
    data = request.json
    blood_group = data['bloodGroup']
    amount = int(data['amount'])

    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM blood
        WHERE status = 'Active' AND blood_group = %s
        ORDER BY id ASC LIMIT 1
    """, (blood_group,))
    candidates = cursor.fetchall()

    total_available = sum(b['volume'] for b in candidates)

    if total_available < amount:
        return jsonify(success=False, message="❌ Not enough blood volume available")

    # 標記足夠血液為 shipped
    shipped_ids = []
    shipped_volume = 0
    for b in candidates:
        if shipped_volume >= amount:
            break
        cursor.execute("UPDATE blood SET status = 'Shipped' WHERE id = %s", (b['id'],))
        shipped_ids.append(b['id'])
        shipped_volume += b['volume']

    db.commit()
    cursor.close()
    return jsonify(success=True, blood_ids=shipped_ids, message=f"✅ {shipped_volume}ml marked as Shipped")

@app.route('/api/ship_blood', methods=['POST'])
def ship_blood():
    data = request.json
    blood_id = data.get("bloodId")

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT status FROM blood WHERE id = %s", (blood_id,))
    blood = cursor.fetchone()

    if not blood:
        return jsonify(success=False, message="❌ Blood ID not found")
    if blood['status'] != 'Shipped':
        return jsonify(success=False, message="⛔ Blood not in 'Shipped' state")

    cursor.execute("UPDATE blood SET status = 'Fulfilled' WHERE id = %s", (blood_id,))
    db.commit()
    cursor.close()
    return jsonify(success=True, message="✅ Blood marked as Fulfilled")

@app.route('/api/blood_status/<int:blood_id>')
def get_blood_status(blood_id):
    cursor = db.cursor()
    cursor.execute("SELECT status FROM blood WHERE id = %s", (blood_id,))
    row = cursor.fetchone()
    cursor.close()

    if not row:
        return jsonify(status="Unknown")
    return jsonify(status=row[0])

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    if not username or not password or not role:
        return jsonify(success=False, message="Missing credentials")

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT password FROM users WHERE username = %s AND role = %s", (username, role))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        return jsonify(success=False, message="User not found")

    hashed_pw = user["password"].encode('utf-8')
    if bcrypt.checkpw(password.encode('utf-8'), hashed_pw):
        redirect_map = {
            "admin": "/admin",
            "supplier": "/supplier",
            "hospital": "/hospital"
        }
        return jsonify(success=True, redirect_url=redirect_map.get(role, "/"))
    else:
        return jsonify(success=False, message="Incorrect password")

@app.route('/api/change_password', methods=['POST'])
def change_password():
    data = request.json
    username = data.get("username")
    old_password = data.get("oldPassword")
    new_password = data.get("newPassword")

    if not username or not old_password or not new_password:
        return jsonify(success=False, message="Missing required fields")

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user:
        return jsonify(success=False, message="User not found")

    stored_hash = user['password'].encode('utf-8')

    if not bcrypt.checkpw(old_password.encode('utf-8'), stored_hash):
        return jsonify(success=False, message="Old password incorrect")

    new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_hash, username))
    db.commit()
    cursor.close()
    return jsonify(success=True, message="Password updated successfully")

import boto3
import os
from werkzeug.utils import secure_filename

S3_BUCKET = 'finalprojects3'
S3_REGION = 'us-east-1'  
S3_FOLDER = 'uploads'

s3 = boto3.client('s3', region_name=S3_REGION)

@app.route('/api/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(success=False, message="No file part in the request")
    
    file = request.files['file']
    if file.filename == '':
        return jsonify(success=False, message="No selected file")
    
    filename = secure_filename(file.filename)
    s3_key = f"{S3_FOLDER}/{filename}"

    try:
        s3.upload_fileobj(file, S3_BUCKET, s3_key)
        file_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{s3_key}"
        return jsonify(success=True, message="✅ File uploaded", url=file_url)
    except Exception as e:
        return jsonify(success=False, message=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)

from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from flask_cors import CORS
from datetime import datetime
import os, json

app = Flask(__name__)
CORS(app)

# ✅ Firebase setup (local + cloud)
if "FIREBASE_KEY" in os.environ:
    firebase_key = json.loads(os.environ["FIREBASE_KEY"])
    cred = credentials.Certificate(firebase_key)
else:
    cred = credentials.Certificate("firebase_key.json")

firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def home():
    return "Attendance Server Running"

# ✅ MARK ATTENDANCE WITH DATE
@app.route('/mark', methods=['POST'])
def mark():
    data = request.json
    data['date'] = datetime.now().strftime("%Y-%m-%d")
    db.collection('attendance').add(data)
    return jsonify({"msg": "Marked"})

# ✅ VIEW WITH ID
@app.route('/view', methods=['GET'])
def view():
    docs = db.collection('attendance').stream()
    data = []

    for doc in docs:
        item = doc.to_dict()
        item['id'] = doc.id   # 🔥 important
        data.append(item)

    return jsonify(data)

# ✅ DELETE RECORD
@app.route('/delete/<doc_id>', methods=['DELETE'])
def delete(doc_id):
    db.collection('attendance').document(doc_id).delete()
    return jsonify({"msg": "Deleted"})

if __name__ == '__main__':
    app.run(debug=True)
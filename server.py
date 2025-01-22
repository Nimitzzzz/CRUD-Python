from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bansos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Penerima(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nik = db.Column(db.String(16), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    alamat = db.Column(db.String(200), nullable=False)
    jenis_bansos = db.Column(db.String(50), nullable=False)
    tanggal_terima = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Belum Disalurkan')

with app.app_context():
    db.create_all()

@app.route('/api/penerima', methods=['GET'])
def get_penerima():
    penerima_list = Penerima.query.all()
    output = []
    for penerima in penerima_list:
        data = {
            'id': penerima.id,
            'nik': penerima.nik,
            'nama': penerima.nama,
            'alamat': penerima.alamat,
            'jenis_bansos': penerima.jenis_bansos,
            'tanggal_terima': penerima.tanggal_terima.strftime("%Y-%m-%d %H:%M:%S"),
            'status': penerima.status
        }
        output.append(data)
    return jsonify(output)

@app.route('/api/penerima', methods=['POST'])
def add_penerima():
    data = request.get_json()
    
    new_penerima = Penerima(
        nik=data['nik'],
        nama=data['nama'],
        alamat=data['alamat'],
        jenis_bansos=data['jenis_bansos'],
        status=data['status']
    )
    
    try:
        db.session.add(new_penerima)
        db.session.commit()
        return jsonify({'message': 'Data penerima berhasil ditambahkan'}), 201
    except:
        return jsonify({'message': 'Terjadi kesalahan saat menambahkan data'}), 400

@app.route('/api/penerima/<int:id>', methods=['PUT'])
def update_penerima(id):
    penerima = Penerima.query.get_or_404(id)
    data = request.get_json()
    
    penerima.nik = data['nik']
    penerima.nama = data['nama']
    penerima.alamat = data['alamat']
    penerima.jenis_bansos = data['jenis_bansos']
    penerima.status = data['status']
    
    try:
        db.session.commit()
        return jsonify({'message': 'Data penerima berhasil diperbarui'})
    except:
        return jsonify({'message': 'Terjadi kesalahan saat memperbarui data'}), 400

@app.route('/api/penerima/<int:id>', methods=['DELETE'])
def delete_penerima(id):
    penerima = Penerima.query.get_or_404(id)
    
    try:
        db.session.delete(penerima)
        db.session.commit()
        return jsonify({'message': 'Data penerima berhasil dihapus'})
    except:
        return jsonify({'message': 'Terjadi kesalahan saat menghapus data'}), 400

if __name__ == '__main__':
    app.run(debug=True)
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from database.database import SessionLocal
from models.model_matakuliah import MataKuliah
from schemas.schema_matakuliah import MataKuliahCreate, MataKuliahOut

matakuliah_bp = Blueprint("matakuliah_bp", __name__)

@matakuliah_bp.route("/matakuliah")
def list_matakuliah():
    session = SessionLocal()
    data = session.query(MataKuliah).all()
    result = [MataKuliahOut.model_validate(m).model_dump() for m in data]
    session.close()
    return jsonify(result)

@matakuliah_bp.route("/matakuliah/<int:id_matkul>")
def get_matakuliah(id_matkul):
    session = SessionLocal()
    m = session.query(MataKuliah).filter(MataKuliah.id_matkul==id_matkul).first()
    if not m:
        session.close()
        return jsonify({"status":"not found"}), 404
    out = MataKuliahOut.model_validate(m).model_dump()
    session.close()
    return jsonify(out)

@matakuliah_bp.route("/matakuliah", methods=["POST"])
def add_matakuliah():
    json_data = request.get_json()
    try:
        m_in = MataKuliahCreate(**json_data)
    except ValidationError as e:
        return jsonify({"status":"error","errors":e.errors()}),400
    session = SessionLocal()
    m = MataKuliah(nama_matkul=m_in.nama_matkul, sks=m_in.sks)
    session.add(m)
    session.commit()
    out = MataKuliahOut.model_validate(m).model_dump()
    session.close()
    return jsonify({"status":"success","matakuliah":out})

@matakuliah_bp.route("/matakuliah/<int:id_matkul>", methods=["PUT"])
def update_matakuliah(id_matkul):
    json_data = request.get_json()
    try:
        m_in = MataKuliahCreate(**json_data)
    except ValidationError as e:
        return jsonify({"status":"error","errors":e.errors()}),400
    session = SessionLocal()
    m = session.query(MataKuliah).filter(MataKuliah.id_matkul==id_matkul).first()
    if not m:
        session.close()
        return jsonify({"status":"not found"}), 404
    m.nama_matkul = m_in.nama_matkul
    m.sks = m_in.sks
    session.commit()
    out = MataKuliahOut.model_validate(m).model_dump()
    session.close()
    return jsonify({"status":"success","matakuliah":out})

@matakuliah_bp.route("/matakuliah/<int:id_matkul>", methods=["DELETE"])
def delete_matakuliah(id_matkul):
    session = SessionLocal()
    m = session.query(MataKuliah).filter(MataKuliah.id_matkul==id_matkul).first()
    if not m:
        session.close()
        return jsonify({"status":"not found"}), 404
    session.delete(m)
    session.commit()
    session.close()
    return jsonify({"status":"deleted"})

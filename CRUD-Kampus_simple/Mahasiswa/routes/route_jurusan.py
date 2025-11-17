from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from database.database import SessionLocal
from models.model_jurusan import Jurusan
from schemas.schema_jurusan import JurusanCreate, JurusanOut

jurusan_bp = Blueprint("jurusan_bp", __name__)

@jurusan_bp.route("/jurusan")
def list_jurusan():
    session = SessionLocal()
    data = session.query(Jurusan).all()
    result = [JurusanOut.model_validate(j).model_dump() for j in data]
    session.close()
    return jsonify(result)

@jurusan_bp.route("/jurusan/<int:id_jurusan>")
def get_jurusan(id_jurusan):
    session = SessionLocal()
    j = session.query(Jurusan).filter(Jurusan.id_jurusan==id_jurusan).first()
    if not j:
        session.close()
        return jsonify({"status":"not found"}), 404
    out = JurusanOut.model_validate(j).model_dump()
    session.close()
    return jsonify(out)

@jurusan_bp.route("/jurusan", methods=["POST"])
def add_jurusan():
    json_data = request.get_json()
    try:
        j_in = JurusanCreate(**json_data)
    except ValidationError as e:
        return jsonify({"status": "error", "errors": e.errors()}), 400
    session = SessionLocal()
    j = Jurusan(nama_jurusan=j_in.nama_jurusan)
    session.add(j)
    session.commit()
    out = JurusanOut.model_validate(j).model_dump()
    session.close()
    return jsonify({"status":"success","jurusan":out})

@jurusan_bp.route("/jurusan/<int:id_jurusan>", methods=["PUT"])
def update_jurusan(id_jurusan):
    json_data = request.get_json()
    try:
        j_in = JurusanCreate(**json_data)
    except ValidationError as e:
        return jsonify({"status": "error", "errors": e.errors()}), 400
    session = SessionLocal()
    j = session.query(Jurusan).filter(Jurusan.id_jurusan==id_jurusan).first()
    if not j:
        session.close()
        return jsonify({"status":"not found"}), 404
    j.nama_jurusan = j_in.nama_jurusan
    session.commit()
    out = JurusanOut.model_validate(j).model_dump()
    session.close()
    return jsonify({"status":"success","jurusan":out})

@jurusan_bp.route("/jurusan/<int:id_jurusan>", methods=["DELETE"])
def delete_jurusan(id_jurusan):
    session = SessionLocal()
    j = session.query(Jurusan).filter(Jurusan.id_jurusan==id_jurusan).first()
    if not j:
        session.close()
        return jsonify({"status":"not found"}), 404
    session.delete(j)
    session.commit()
    session.close()
    return jsonify({"status":"deleted"})

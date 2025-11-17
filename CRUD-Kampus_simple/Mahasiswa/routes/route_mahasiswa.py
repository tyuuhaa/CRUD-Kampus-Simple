from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from database.database import SessionLocal
from models.model_mahasiswa import Mahasiswa
from models.model_matakuliah import MataKuliah
from schemas.schema_mahasiswa import MahasiswaCreate, MahasiswaOut
mahasiswa_bp = Blueprint("mahasiswa_bp", __name__)

@mahasiswa_bp.route("/mahasiswa")
def list_mahasiswa():
    session = SessionLocal()
    data = session.query(Mahasiswa).all()
    result = [MahasiswaOut.model_validate(m).model_dump() for m in data]
    session.close()
    return jsonify(result)

@mahasiswa_bp.route("/mahasiswa/<nim>")
def get_mahasiswa(nim):
    session = SessionLocal()
    m = session.query(Mahasiswa).filter(Mahasiswa.nim==nim).first()
    if not m:
        session.close()
        return jsonify({"status":"not found"}), 404
    out = MahasiswaOut.model_validate(m).model_dump()
    session.close()
    return jsonify(out)

@mahasiswa_bp.route("/mahasiswa", methods=["POST"])
def add_mahasiswa():
    json_data = request.get_json()
    try:
        mhs_in = MahasiswaCreate(**json_data)
    except ValidationError as e:
        return jsonify({"status": "error", "errors": e.errors()}), 400

    session = SessionLocal()
    mhs = Mahasiswa(
        nim=mhs_in.nim,
        nama=mhs_in.nama,
        tahun_masuk=mhs_in.tahun_masuk,
        alamat=mhs_in.alamat,
        tanggal_lahir=mhs_in.tanggal_lahir,
        id_jurusan=mhs_in.id_jurusan
    )
    if mhs_in.matkul_ids:
        mhs.matakuliah = session.query(MataKuliah).filter(MataKuliah.id_matkul.in_(mhs_in.matkul_ids)).all()

    session.add(mhs)
    session.commit()
    out = MahasiswaOut.model_validate(mhs).model_dump()
    session.close()
    return jsonify({"status": "success", "mahasiswa": out})

@mahasiswa_bp.route("/mahasiswa/<nim>", methods=["PUT"])
def update_mahasiswa(nim):
    json_data = request.get_json()
    try:
        mhs_in = MahasiswaCreate(**json_data)
    except ValidationError as e:
        return jsonify({"status": "error", "errors": e.errors()}), 400

    session = SessionLocal()
    mhs = session.query(Mahasiswa).filter(Mahasiswa.nim==nim).first()
    if not mhs:
        session.close()
        return jsonify({"status":"not found"}), 404

    mhs.nama = mhs_in.nama
    mhs.tahun_masuk = mhs_in.tahun_masuk
    mhs.alamat = mhs_in.alamat
    mhs.tanggal_lahir = mhs_in.tanggal_lahir
    mhs.id_jurusan = mhs_in.id_jurusan
    if mhs_in.matkul_ids:
        mhs.matakuliah = session.query(MataKuliah).filter(MataKuliah.id_matkul.in_(mhs_in.matkul_ids)).all()
    else:
        mhs.matakuliah = []

    session.commit()
    out = MahasiswaOut.model_validate(mhs).model_dump()
    session.close()
    return jsonify({"status":"success","mahasiswa":out})

@mahasiswa_bp.route("/mahasiswa/<nim>", methods=["DELETE"])
def delete_mahasiswa(nim):
    session = SessionLocal()
    mhs = session.query(Mahasiswa).filter(Mahasiswa.nim==nim).first()
    if not mhs:
        session.close()
        return jsonify({"status":"not found"}), 404
    session.delete(mhs)
    session.commit()
    session.close()
    return jsonify({"status":"deleted"})

from flask import Flask
from routes.route_mahasiswa import mahasiswa_bp
from routes.route_jurusan import jurusan_bp
from routes.route_matakuliah import matakuliah_bp
from database.base import Base
from database.database import engine

# Buat tabel
Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.register_blueprint(mahasiswa_bp)
app.register_blueprint(jurusan_bp)
app.register_blueprint(matakuliah_bp)

if __name__ == "__main__":
    app.run(debug=True)

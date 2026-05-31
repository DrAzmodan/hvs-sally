"""
HVS Sally — Backend Flask para Railway
Base de datos: JSON en archivo local (Railway persiste el volumen)
"""
import os, json, time, hashlib
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

# ── BASE DE DATOS (archivo JSON) ──────────────────────────
DATA_FILE = os.path.join(os.path.dirname(__file__), 'hvs_data.json')

ESTRUCTURA_INICIAL = {
    "ventas": [], "fondos": [], "egresos": [], "ingresos": [],
    "retiros": [], "hospitalizados": [], "consentimientos": [],
    "crm": [], "planes": [], "pedidos": [], "expedientes": [],
    "codigos": [], "usuarios": {"hvs": "sally2025", "admin": "hvs2025"},
    "config": {
        "clinica": "Hospital Veterinario Sally",
        "dir": "Av. 16 de Septiembre #15, Cuanalan, Acolman, Edo. Méx.",
        "tel": "55 2851 2857",
        "director": "Dr. Rafael A. Valladares García, H.C.",
        "cedula": "09150354",
        "pension": 200
    }
}

def leer_db():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Asegurar que todas las claves existen
            for k, v in ESTRUCTURA_INICIAL.items():
                if k not in data:
                    data[k] = v
            return data
    except Exception as e:
        print(f"Error leyendo DB: {e}")
    return dict(ESTRUCTURA_INICIAL)

def guardar_db(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error guardando DB: {e}")
        return False

# ── AUTENTICACIÓN ─────────────────────────────────────────
@app.route('/api/login', methods=['POST'])
def login():
    body = request.get_json() or {}
    usuario = (body.get('usuario') or '').strip().lower()
    password = (body.get('password') or '').strip()
    db = leer_db()
    usuarios = db.get('usuarios', {})
    if usuario in usuarios and usuarios[usuario] == password:
        token = hashlib.sha256(f"{usuario}{time.time()}hvs_sally".encode()).hexdigest()
        return jsonify({"ok": True, "token": token, "usuario": usuario})
    return jsonify({"ok": False, "msg": "Usuario o contraseña incorrectos"}), 401

@app.route('/api/cambiar-password', methods=['POST'])
def cambiar_password():
    body = request.get_json() or {}
    usuario = body.get('usuario', 'hvs')
    nueva = body.get('nueva', '')
    if not nueva or len(nueva) < 4:
        return jsonify({"ok": False, "msg": "Contraseña muy corta"}), 400
    db = leer_db()
    db['usuarios'][usuario] = nueva
    guardar_db(db)
    return jsonify({"ok": True})

# ── CRUD GENÉRICO ─────────────────────────────────────────
@app.route('/api/<coleccion>', methods=['GET'])
def obtener(coleccion):
    db = leer_db()
    if coleccion not in db:
        return jsonify([])
    return jsonify(db[coleccion])

@app.route('/api/<coleccion>', methods=['POST'])
def agregar(coleccion):
    body = request.get_json() or {}
    db = leer_db()
    if coleccion not in db:
        db[coleccion] = []
    if isinstance(db[coleccion], list):
        db[coleccion].append(body)
    guardar_db(db)
    return jsonify({"ok": True})

@app.route('/api/<coleccion>/bulk', methods=['POST'])
def agregar_bulk(coleccion):
    """Reemplaza toda la colección de una vez"""
    body = request.get_json()
    if not isinstance(body, list):
        return jsonify({"ok": False, "msg": "Se esperaba una lista"}), 400
    db = leer_db()
    db[coleccion] = body
    guardar_db(db)
    return jsonify({"ok": True, "count": len(body)})

@app.route('/api/<coleccion>/<int:idx>', methods=['PUT'])
def actualizar(coleccion, idx):
    body = request.get_json() or {}
    db = leer_db()
    if coleccion not in db or not isinstance(db[coleccion], list):
        return jsonify({"ok": False}), 404
    if idx < 0 or idx >= len(db[coleccion]):
        return jsonify({"ok": False}), 404
    db[coleccion][idx] = body
    guardar_db(db)
    return jsonify({"ok": True})

@app.route('/api/<coleccion>/<int:idx>', methods=['DELETE'])
def eliminar(coleccion, idx):
    db = leer_db()
    if coleccion not in db or not isinstance(db[coleccion], list):
        return jsonify({"ok": False}), 404
    if idx < 0 or idx >= len(db[coleccion]):
        return jsonify({"ok": False}), 404
    db[coleccion].pop(idx)
    guardar_db(db)
    return jsonify({"ok": True})

# ── CONFIGURACIÓN ─────────────────────────────────────────
@app.route('/api/config', methods=['GET'])
def obtener_config():
    db = leer_db()
    return jsonify(db.get('config', ESTRUCTURA_INICIAL['config']))

@app.route('/api/config', methods=['POST'])
def guardar_config():
    body = request.get_json() or {}
    db = leer_db()
    db['config'].update(body)
    guardar_db(db)
    return jsonify({"ok": True})

# ── BACKUP COMPLETO ───────────────────────────────────────
@app.route('/api/backup', methods=['GET'])
def backup():
    db = leer_db()
    # No incluir contraseñas en el backup
    backup_data = {k: v for k, v in db.items() if k != 'usuarios'}
    return jsonify(backup_data)

@app.route('/api/backup', methods=['POST'])
def restaurar():
    body = request.get_json() or {}
    db = leer_db()
    for k, v in body.items():
        if k != 'usuarios':  # No sobrescribir contraseñas
            db[k] = v
    guardar_db(db)
    return jsonify({"ok": True})

# ── SERVIR EL FRONTEND ────────────────────────────────────
@app.route('/')
def index():
    import glob
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    html_files = glob.glob(os.path.join(static_dir, '*.html'))
    if html_files:
        filename = os.path.basename(html_files[0])
        return send_from_directory('static', filename)
    return "HVS Sally — index.html no encontrado en /static", 404

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

# ── HEALTH CHECK ──────────────────────────────────────────
@app.route('/health')
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

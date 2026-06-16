import os
import sqlite3
from flask import Flask, request, jsonify, render_template, send_from_directory, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PIL import Image
import imagehash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
DB_PATH = os.path.join(BASE_DIR, 'data', 'images.db')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

app = Flask(__name__, root_path=BASE_DIR, instance_path=BASE_DIR)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-for-local')

# Simple admin credentials (override via env vars in production)
ADMIN_USER = os.environ.get('E_LIXO_ADMIN_USER', 'admin')
ADMIN_PASS = os.environ.get('E_LIXO_ADMIN_PASS', 'password')

# Predefined explanations for each category
CATEGORY_EXPLANATIONS = {
    'Equipamentos de informática': 'Computadores, notebooks, monitores, impressoras e acessórios relacionados ao processamento de dados.',
    'Dispositivos de comunicação': 'Celulares, modems, roteadores e outros dispositivos usados para comunicação de voz e dados.',
    'Equipamentos de áudio e vídeo': 'Televisores, caixas de som, câmeras, aparelhos de som e similares.',
    'Pilhas e baterias': 'Pilhas alcalinas, baterias recarregáveis e baterias de lítio usadas em equipamentos eletrônicos.',
    'Carregadores e cabos': 'Carregadores, cabos USB, cabos de energia e adaptadores associados a dispositivos eletrônicos.',
    'Eletrodomésticos eletrônicos': 'Aparelhos domésticos com componentes eletrônicos, como micro-ondas, liquidificadores e ferros elétricos.',
    'Equipamentos de iluminação': 'Lâmpadas, luminárias e lâmpadas LED contendo componentes eletrônicos ou materiais recicláveis especiais.',
    'Componentes eletrônicos': 'Placas, resistores, capacitores, chips, e outros componentes usados em circuitos eletrônicos.'
}

# Mapping of common ImageNet labels to the waste categories in this app.
LABEL_TO_CATEGORY = {
    'computer': 'Equipamentos de informática',
    'laptop': 'Equipamentos de informática',
    'desktop computer': 'Equipamentos de informática',
    'notebook': 'Equipamentos de informática',
    'monitor': 'Equipamentos de informática',
    'keyboard': 'Equipamentos de informática',
    'mouse': 'Equipamentos de informática',
    'cellular telephone': 'Dispositivos de comunicação',
    'mobile phone': 'Dispositivos de comunicação',
    'radio': 'Dispositivos de comunicação',
    'telephone': 'Dispositivos de comunicação',
    'modem': 'Dispositivos de comunicação',
    'router': 'Dispositivos de comunicação',
    'television': 'Equipamentos de áudio e vídeo',
    'speaker': 'Equipamentos de áudio e vídeo',
    'headphone': 'Equipamentos de áudio e vídeo',
    'camera': 'Equipamentos de áudio e vídeo',
    'microphone': 'Equipamentos de áudio e vídeo',
    'battery': 'Pilhas e baterias',
    'coin cell': 'Pilhas e baterias',
    'charger': 'Carregadores e cabos',
    'cable': 'Carregadores e cabos',
    'power cord': 'Carregadores e cabos',
    'adapter': 'Carregadores e cabos',
    'microwave': 'Eletrodomésticos eletrônicos',
    'toaster': 'Eletrodomésticos eletrônicos',
    'blender': 'Eletrodomésticos eletrônicos',
    'vacuum': 'Eletrodomésticos eletrônicos',
    'lamp': 'Equipamentos de iluminação',
    'light bulb': 'Equipamentos de iluminação',
    'candle': 'Equipamentos de iluminação',
    'circuit board': 'Componentes eletrônicos',
    'printed circuit board': 'Componentes eletrônicos',
    'resistor': 'Componentes eletrônicos',
    'capacitor': 'Componentes eletrônicos',
    'semiconductor': 'Componentes eletrônicos'
}


def map_label_to_category(label):
    label_text = label.lower()
    if label_text in LABEL_TO_CATEGORY:
        return LABEL_TO_CATEGORY[label_text]

    for key, category in LABEL_TO_CATEGORY.items():
        if key in label_text:
            return category
    return None


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            phash TEXT NOT NULL,
            category TEXT,
            explanation TEXT
        )
    ''')
    conn.commit()
    conn.close()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


def compute_phash(path):
    img = Image.open(path).convert('RGB')
    return str(imagehash.phash(img))


def find_similar(phash_hex, threshold=6):
    # Return the closest match within threshold hamming distance
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT id, filename, phash, category, explanation FROM images')
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return None

    new_hash = imagehash.hex_to_hash(phash_hex)
    best = None
    best_dist = None
    for r in rows:
        try:
            existing = imagehash.hex_to_hash(r['phash'])
        except Exception:
            continue
        dist = new_hash - existing
        if best is None or dist < best_dist:
            best = r
            best_dist = dist

    if best_dist is not None and best_dist <= threshold:
        return dict(id=best['id'], filename=best['filename'], category=best['category'], explanation=best['explanation'], distance=int(best_dist))
    return None


def find_nearest_k(phash_hex, k=3):
    """Return up to k nearest rows sorted by hamming distance (no threshold)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT id, filename, phash, category, explanation FROM images')
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return []

    new_hash = imagehash.hex_to_hash(phash_hex)
    neighbors = []
    for r in rows:
        try:
            existing = imagehash.hex_to_hash(r['phash'])
        except Exception:
            continue
        dist = new_hash - existing
        neighbors.append((int(dist), dict(id=r['id'], filename=r['filename'], category=r['category'], explanation=r['explanation'])))

    neighbors.sort(key=lambda x: x[0])
    return [{'distance': d, **info} for d, info in neighbors[:k]]


def try_classify(image_path):
    """Optional ML classification using TensorFlow MobileNetV2 if available.
    Returns a dict with category, explanation, label and confidence, or None if TF not available."""
    try:
        from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
        from tensorflow.keras.preprocessing import image
        import numpy as np
    except Exception:
        return None

    try:
        model = MobileNetV2(weights='imagenet')
        img = image.load_img(image_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = model.predict(x)
        decoded = decode_predictions(preds, top=3)[0]

        best_label = decoded[0][1]
        confidence = float(decoded[0][2])
        category = map_label_to_category(best_label)
        explanation = CATEGORY_EXPLANATIONS.get(category)

        result = {
            'label': best_label,
            'confidence': round(confidence, 3),
            'category': category,
            'explanation': explanation
        }

        if category is None and len(decoded) > 1:
            for item in decoded[1:]:
                candidate = map_label_to_category(item[1])
                if candidate:
                    result['category'] = candidate
                    result['explanation'] = CATEGORY_EXPLANATIONS.get(candidate)
                    break

        return result
    except Exception:
        return None


@app.route('/')
def index():
    return render_template('index.html', is_admin=session.get('admin', False))


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/catalogs')
def catalogs():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT id, filename, phash, category, explanation FROM images ORDER BY id DESC')
    rows = cur.fetchall()
    conn.close()
    return render_template('catalogs.html', items=rows, explanations=CATEGORY_EXPLANATIONS, is_admin=session.get('admin', False))


def admin_required(fn):
    def wrapper(*a, **kw):
        if not session.get('admin'):
            flash('Acesso restrito. Faça login como administrador.','warning')
            return redirect(url_for('login'))
        return fn(*a, **kw)
    wrapper.__name__ = fn.__name__
    return wrapper


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['admin'] = True
            flash('Login realizado com sucesso.','success')
            return redirect(url_for('admin'))
        flash('Credenciais inválidas.','danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash('Logout efetuado.','info')
    return redirect(url_for('index'))


@app.route('/admin')
@admin_required
def admin():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT id, filename, phash, category, explanation FROM images ORDER BY id DESC')
    rows = cur.fetchall()
    conn.close()
    return render_template('admin.html', items=rows)


@app.route('/admin/delete/<int:id>', methods=['POST'])
@admin_required
def admin_delete(id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT filename FROM images WHERE id = ?', (id,))
    row = cur.fetchone()
    if row:
        filename = row[0]
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        except Exception:
            pass
    cur.execute('DELETE FROM images WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Item removido do catálogo.','success')
    return redirect(url_for('admin'))


@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'no file part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'no selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # ensure unique filename
        base, ext = os.path.splitext(filename)
        i = 1
        while os.path.exists(save_path):
            filename = f"{base}_{i}{ext}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            i += 1
        file.save(save_path)

        phash = compute_phash(save_path)
        similar = find_similar(phash)
        if similar:
            return jsonify({'matched': True, 'match': similar, 'filename': filename})
        # not matched — prepare suggestions from nearest neighbors
        neighbors = find_nearest_k(phash, k=5)
        suggested = None
        if neighbors:
            # pick majority category among neighbors (if any)
            from collections import Counter
            cats = [n['category'] for n in neighbors if n.get('category')]
            if cats:
                most = Counter(cats).most_common(1)[0]
                # compute a simple confidence from the best neighbor distance
                best_dist = neighbors[0]['distance']
                confidence = max(0.0, 1.0 - (best_dist / 16.0))
                suggested = {'category': most[0], 'confidence': round(confidence, 2), 'neighbors': neighbors}

            # optional ML classification
            ml = try_classify(save_path)
            return jsonify({'matched': False, 'phash': phash, 'filename': filename, 'suggested': suggested, 'ml_suggestion': ml})
    return jsonify({'error': 'invalid file type'}), 400


@app.route('/catalog', methods=['POST'])
def catalog():
    data = request.json or request.form
    filename = data.get('filename')
    category = data.get('category')
    explanation = data.get('explanation', '')
    phash = data.get('phash')
    if not filename or not category or not phash:
        return jsonify({'error': 'missing fields (filename, category, phash required)'}), 400

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('INSERT INTO images (filename, phash, category, explanation) VALUES (?, ?, ?, ?)', (filename, phash, category, explanation))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return jsonify({'ok': True, 'id': new_id})


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000, debug=True)

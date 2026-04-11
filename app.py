from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, send_from_directory
from database import init_database, generate_unique_key, create_connection, get_connection_name, save_or_update_share, get_share_data
import os
import random
import secrets
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
ALLOWED_FILE_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'zip', 'rar'}
CIMG_DIR = os.path.join(os.path.dirname(__file__), 'static', 'cimg')
FILE_DIR = os.path.join(os.path.dirname(__file__), 'static', 'files')

os.makedirs(CIMG_DIR, exist_ok=True)
os.makedirs(FILE_DIR, exist_ok=True)

with app.app_context():
    init_database()


def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENSIONS


def generate_random_filename(extension='jpg'):
    while True:
        random_num = random.randint(100000, 999999)
        filename = f'{random_num}.{extension}'
        if not os.path.exists(os.path.join(CIMG_DIR, filename)) and not os.path.exists(os.path.join(FILE_DIR, filename)):
            return filename


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/teacher')
def teacher():
    key = request.args.get('key')
    connection_name = request.args.get('name')
    error = request.args.get('error')
    return render_template('teacher.html', key=key, connection_name=connection_name, error=error)


@app.route('/class')
def class_room():
    return render_template('class.html')


@app.route('/teacher/img')
def editor():
    return render_template('editor.html')


@app.route('/api/create-connection', methods=['POST'])
def api_create_connection():
    name = request.form.get('name')
    if not name:
        return redirect(url_for('teacher', error='请输入连接名称'))
    
    try:
        key = generate_unique_key()
        create_connection(key, name)
        return redirect(url_for('teacher', key=key, name=name))
    except Exception as e:
        return redirect(url_for('teacher', error=f'创建连接失败：{str(e)}'))


@app.route('/api/get-connection-name', methods=['GET'])
def api_get_connection_name():
    key = request.args.get('key')
    if not key:
        return jsonify({'name': None})
    name = get_connection_name(key)
    return jsonify({'name': name})


@app.route('/api/get-share', methods=['GET'])
def api_get_share():
    key = request.args.get('key')
    if not key:
        return jsonify({'share': None})
    share = get_share_data(key)
    return jsonify({'share': share})


@app.route('/api/upload', methods=['POST'])
def api_upload():
    try:
        key = request.form.get('key')
        if not key:
            return jsonify({'success': False, 'error': '缺少连接密钥'})
        
        if not get_connection_name(key):
            return jsonify({'success': False, 'error': '连接密钥无效'})
        
        text = request.form.get('text', '')
        img_list = []
        file_list = []
        
        if 'images' in request.files:
            files = request.files.getlist('images')
            for file in files:
                if file and file.filename:
                    if allowed_image(file.filename):
                        ext = file.filename.rsplit('.', 1)[1].lower()
                        filename = generate_random_filename(ext)
                        file.save(os.path.join(CIMG_DIR, filename))
                        img_list.append(filename)
        
        if 'files' in request.files:
            files = request.files.getlist('files')
            for file in files:
                if file and file.filename:
                    if allowed_file(file.filename):
                        ext = file.filename.rsplit('.', 1)[1].lower()
                        original_name = file.filename
                        filename = generate_random_filename(ext)
                        file.save(os.path.join(FILE_DIR, filename))
                        file_list.append({'filename': filename, 'original_name': original_name})
        
        share_data = {'img': ','.join(img_list), 'text': text, 'files': file_list}
        import json
        save_or_update_share(key, json.dumps(share_data, ensure_ascii=False))
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/download/<filename>')
def download_file(filename):
    try:
        return send_from_directory(FILE_DIR, filename, as_attachment=True)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404


if __name__ == '__main__':
    import os
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=5000, debug=debug)

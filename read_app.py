import os
import hashlib
import mdformat
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ================= CẤU HÌNH =================
# Đường dẫn tới thư mục gốc chứa các file MD trên Windows
BASE_DIR = r"D:\Novel\Chapters" 

# Mật khẩu để lưu file (Đã được băm SHA-256) - Mặc định là băm của: 123456
PASSWORD_HASH = "dd4051c8a4aeab8583d53926365de7e5f96f5cc1fd4a2f3df5882b2223618426"
# ============================================

# Template cho trang Danh sách File/Thư mục
LIST_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Danh sách: {{ current_dir }}</title>
    <style>
        :root { --bg-color: #fdfbf7; --text-color: #333; --primary: #4f46e5; }
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background: var(--bg-color); color: var(--text-color); padding: 20px; font-size: 18px; margin: 0; }
        .container { max-width: 800px; margin: auto; }
        h2 { border-bottom: 2px solid var(--primary); padding-bottom: 10px; word-break: break-all; }
        .list-group { display: flex; flex-direction: column; gap: 12px; margin-top: 20px; }
        .list-item { background: #fff; padding: 18px; border-radius: 8px; text-decoration: none; color: #333; box-shadow: 0 2px 5px rgba(0,0,0,0.05); font-weight: bold; border: 1px solid #eee; display: flex; align-items: center; }
        .list-item:active { background: #f0f0f0; }
        .back-link { display: inline-block; padding: 10px 15px; background: #e5e7eb; border-radius: 5px; text-decoration: none; color: #333; font-weight: bold; margin-bottom: 10px; }
        .icon { font-size: 24px; margin-right: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>📂 {{ current_dir }}</h2>
        
        {% if parent_dir is not none %}
            <a href="/{{ parent_dir }}" class="back-link">🔙 Quay lại</a>
        {% endif %}
        
        <div class="list-group">
            {% if not items %}
                <p>Thư mục này đang trống.</p>
            {% endif %}
            {% for item in items %}
                <a href="/{{ item.path }}" class="list-item">
                    <span class="icon">{{ item.icon }}</span>
                    {{ item.name }}
                </a>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

# Template cho trang Đọc/Sửa file
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Đọc & Sửa: {{ path }}</title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        :root { --bg-color: #fdfbf7; --text-color: #333; --primary: #4f46e5; }
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background: var(--bg-color); color: var(--text-color); line-height: 1.6; padding: 20px; font-size: 18px; margin: 0; }
        .container { max-width: 800px; margin: auto; padding-bottom: 80px; }
        .nav-link { display: inline-block; margin-bottom: 15px; text-decoration: none; color: var(--primary); font-weight: bold; font-size: 16px; background: #e0e7ff; padding: 8px 15px; border-radius: 20px; }
        #viewer { padding: 10px 0; text-align: justify; }
        #editor { width: 100%; height: 70vh; padding: 15px; font-family: monospace; font-size: 16px; border: 1px solid #ccc; border-radius: 8px; display: none; box-sizing: border-box; resize: none; background: #fff;}
        .toolbar { position: fixed; bottom: 0; left: 0; right: 0; background: #fff; padding: 10px 20px; box-shadow: 0 -2px 10px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center; }
        button { background: var(--primary); color: white; border: none; padding: 10px 20px; border-radius: 5px; font-size: 16px; font-weight: bold; cursor: pointer;}
        input[type="password"] { padding: 10px; border: 1px solid #ccc; border-radius: 5px; display: none; }
        .editing input[type="password"] { display: inline-block; width: 40%; }
        .editing #btn-edit { background: #dc2626; }
    </style>
</head>
<body>
    <div class="container">
        <a href="/{{ parent_dir }}" class="nav-link">🏠 Quay lại danh mục</a>
        <div id="viewer"></div>
        <textarea id="editor"></textarea>
    </div>

    <div class="toolbar" id="toolbar">
        <button id="btn-edit" onclick="toggleEdit()">Sửa</button>
        <input type="password" id="pass-input" placeholder="Mật khẩu lưu...">
        <button id="btn-save" style="display:none;" onclick="saveDoc()">Lưu lại</button>
    </div>

    <script>
        let rawMd = `{{ content | safe }}`;
        const currentPath = "{{ path }}";
        const viewer = document.getElementById('viewer');
        const editor = document.getElementById('editor');
        const btnEdit = document.getElementById('btn-edit');
        const btnSave = document.getElementById('btn-save');
        const passInput = document.getElementById('pass-input');
        const toolbar = document.getElementById('toolbar');

        let isEditing = false;

        viewer.innerHTML = marked.parse(rawMd);
        editor.value = rawMd;

        function toggleEdit() {
            isEditing = !isEditing;
            if (isEditing) {
                viewer.style.display = 'none';
                editor.style.display = 'block';
                btnSave.style.display = 'inline-block';
                toolbar.classList.add('editing');
                btnEdit.innerText = 'Hủy';
            } else {
                viewer.innerHTML = marked.parse(editor.value);
                viewer.style.display = 'block';
                editor.style.display = 'none';
                btnSave.style.display = 'none';
                toolbar.classList.remove('editing');
                btnEdit.innerText = 'Sửa';
            }
        }

        async function saveDoc() {
            const password = passInput.value;
            if(!password) return alert("Vui lòng nhập mật khẩu!");
            
            btnSave.innerText = 'Đang lưu...';
            try {
                const res = await fetch('/api/save', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ path: currentPath, content: editor.value, password: password })
                });
                
                if (res.ok) {
                    alert('Đã lưu thành công! Cú pháp Markdown đã được tự động chuẩn hóa.');
                    location.reload(); 
                } else {
                    const data = await res.json();
                    alert('Lỗi: ' + (data.error || 'Sai mật khẩu!'));
                }
            } catch (e) {
                alert('Lỗi kết nối tới máy chủ!');
            }
            btnSave.innerText = 'Lưu lại';
        }
    </script>
</body>
</html>
"""

# Gộp chung định tuyến (Route) cho cả Trang chủ và File
@app.route('/', defaults={'req_path': ''}, methods=['GET'])
@app.route('/<path:req_path>', methods=['GET'])
def handle_request(req_path):
    if '..' in req_path:
        return "Đường dẫn không hợp lệ", 400
        
    full_path = os.path.join(BASE_DIR, req_path)
    
    # Tự động tạo thư mục gốc nếu chưa có
    os.makedirs(BASE_DIR, exist_ok=True)

    # 1. NẾU LÀ THƯ MỤC -> HIỂN THỊ DANH SÁCH FILE/FOLDER
    if os.path.isdir(full_path):
        items = []
        try:
            # Liệt kê và sắp xếp file/folder
            for f in sorted(os.listdir(full_path)):
                item_full_path = os.path.join(full_path, f)
                # Dùng '/' cho URL thay vì '\' của Windows
                rel_path = os.path.relpath(item_full_path, BASE_DIR).replace('\\', '/')
                
                if os.path.isdir(item_full_path):
                    items.append({'name': f, 'path': rel_path, 'icon': '📁'})
                elif f.endswith('.md'):
                    items.append({'name': f[:-3], 'path': rel_path[:-3], 'icon': '📄'})
        except Exception as e:
            pass
            
        # Xác định thư mục cha để tạo nút "Quay lại"
        parent_dir = None
        if req_path:
            parent_dir = os.path.dirname(req_path).replace('\\', '/')
            if parent_dir == req_path: 
                parent_dir = ''
                
        display_name = req_path if req_path else "Thư viện Tiểu thuyết"
        return render_template_string(LIST_TEMPLATE, current_dir=display_name, items=items, parent_dir=parent_dir)

    # 2. NẾU KHÔNG PHẢI THƯ MỤC -> CHẠY GIAO DIỆN ĐỌC/SỬA FILE
    if not full_path.endswith('.md'):
        full_path += '.md'
        
    if not os.path.exists(full_path):
        content = f"# {req_path}\n\nChương này chưa có nội dung. Nhấn 'Sửa' để bắt đầu viết."
    else:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
    safe_content = content.replace("`", "\\`").replace("${", "\\${")
    
    # Lấy tên thư mục chứa file để làm nút "Quay lại danh mục"
    parent_dir = os.path.dirname(req_path).replace('\\', '/')
    if parent_dir == req_path:
        parent_dir = ''
        
    return render_template_string(HTML_TEMPLATE, path=req_path, content=safe_content, parent_dir=parent_dir)

@app.route('/api/save', methods=['POST'])
def save_file():
    data = request.json
    filepath = data.get('path')
    content = data.get('content')
    password = data.get('password')
    
    if not filepath or content is None or not password:
        return jsonify({"error": "Thiếu dữ liệu"}), 400
        
    hashed_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
    if hashed_pw != PASSWORD_HASH:
        return jsonify({"error": "Sai mật khẩu"}), 401
        
    if '..' in filepath:
        return jsonify({"error": "Đường dẫn không hợp lệ"}), 400
        
    full_path = os.path.join(BASE_DIR, filepath)
    if not full_path.endswith('.md'):
        full_path += '.md'
        
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    try:
        formatted_content = mdformat.text(content)
    except Exception as e:
        formatted_content = content

    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(formatted_content)
        
    return jsonify({"success": True}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
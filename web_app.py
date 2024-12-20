import os
import logging
from logging_config import *

logger = logging.getLogger(__name__)

# 在导入其他库之前设置环境变量
os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'

from flask import Flask, request, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from image_search import ImageSearchEngine

# 修改 Flask 应用初始化，添加静态文件夹配置
app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制上传文件大小为16MB

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 初始化图像搜索引擎
search_engine = ImageSearchEngine()

@app.route('/')
def home():
    return render_template('index.html')

# 添加静态文件路由
@app.route('/images/<path:filename>')
def serve_image(filename):
    # 确保路径分隔符正确
    filename = filename.replace('\\', '/')
    return send_from_directory('images', filename)

@app.route('/search', methods=['POST'])
def search():
    logger.info('Received search request')
    if 'image' not in request.files:
        return jsonify({'error': '没有上传图片'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        # 使用正斜杠的路径
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')
        file.save(filepath)
        
        # 执行图像搜索
        results = search_engine.search_similar_images(filepath)
        
        # 确保返回结果中的路径使用正斜杠
        for result in results:
            result['image_path'] = result['image_path'].replace('\\', '/')
        
        # 清理上传的临时文件
        os.remove(filepath)
        
        return jsonify({'results': results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 
from flask import Flask, send_from_directory
import os

# 创建 Flask 应用实例
app = Flask(__name__, static_folder='../', static_url_path='')

@app.route('/')
def index():
    """
    定义根路由，用于提供 index.html 文件。
    它会从项目根目录（即 backend 目录的上一级）查找 index.html。
    """
    # 使用 send_from_directory 从项目根目录提供 index.html
    # os.path.abspath(os.path.join(app.static_folder)) 获取项目根目录的绝对路径
    return send_from_directory(os.path.abspath(app.static_folder), 'index.html')

if __name__ == '__main__':
    # 启动 Flask 开发服务器
    # host='0.0.0.0' 使服务器可以从本地网络访问
    # debug=True 开启调试模式，方便开发
    app.run(host='0.0.0.0', port=5000, debug=True) 
#!/bin/bash

echo "开始设置后端虚拟环境..."

# 创建Python虚拟环境
if [ -d "venv" ]; then
    echo "发现已存在的虚拟环境，将重建..."
    rm -rf venv
fi

echo "正在创建新的虚拟环境..."
python3 -m venv venv

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo "更新pip到最新版本..."
pip install --upgrade pip

# 安装依赖
echo "安装项目依赖..."
pip install -r requirements.txt

# 检查数据库是否存在，如不存在则初始化数据库
if [ ! -f "app.db" ]; then
    echo "正在初始化数据库..."
    flask db init
    flask db migrate -m "初始数据库结构"
    flask db upgrade
    echo "数据库初始化完成"
else
    echo "数据库已存在，跳过初始化步骤"
fi

echo "虚拟环境设置完成！"
echo "使用以下命令激活虚拟环境："
echo "  source venv/bin/activate"
echo ""
echo "启动Flask服务器："
echo "  flask run --host=0.0.0.0" 
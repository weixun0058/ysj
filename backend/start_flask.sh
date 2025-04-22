#!/bin/bash

# 如果当前不在后端目录，切换到后端目录
if [ "$(basename "$(pwd)")" != "backend" ]; then
    cd "$(dirname "$0")" || { echo "无法切换到后端目录"; exit 1; }
fi

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "错误：虚拟环境不存在，请先运行 ./setup_venv.sh"
    exit 1
fi

# 激活虚拟环境
source venv/bin/activate

# 检查是否需要更新依赖
if [ "$1" == "update" ]; then
    echo "更新依赖..."
    pip install -r requirements.txt
fi

# 显示当前环境信息
echo "============================================="
echo "Flask 后端服务启动"
echo "Python版本: $(python --version)"
echo "虚拟环境: $(which python)"
echo "============================================="

# 启动Flask服务器
echo "启动Flask服务器..."
flask run --host=0.0.0.0 "$@" 
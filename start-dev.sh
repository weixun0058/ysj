#!/bin/bash

# 定义项目根目录 (根据你的环境调整，如果需要)
PROJECT_ROOT="/home/wx/code/ysj"
BACKEND_PID="" # 初始化 PID 变量

# 定义清理函数
cleanup() {
    echo "Caught signal or exiting script..."
    if [ ! -z "$BACKEND_PID" ]; then # 检查 PID 是否非空
        echo "Attempting to stop backend server (PID: $BACKEND_PID)..."
        kill $BACKEND_PID # 尝试正常终止
        # 可以加一个短暂等待和强制杀死选项
        # sleep 1
        # kill -0 $BACKEND_PID 2>/dev/null && kill -9 $BACKEND_PID
        echo "Kill command sent."
    else
        echo "Backend PID not set, nothing to kill."
    fi
}

# 设置陷阱：在脚本退出(EXIT)、收到 SIGINT(Ctrl+C) 或 SIGTERM 时执行 cleanup 函数
trap cleanup EXIT SIGINT SIGTERM

echo "Starting Backend Server..."
# 进入根目录，启动后端并在后台运行
cd "$PROJECT_ROOT"
"$PROJECT_ROOT/backend/venv/bin/python" "$PROJECT_ROOT/backend/app.py" &
BACKEND_PID=$! # 获取后台进程 ID
echo "Backend PID: $BACKEND_PID"

# 检查后端是否真的启动了（可选但推荐）
sleep 2 # 等待一小段时间让服务器有机会启动或失败
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "Error: Backend server failed to start."
    exit 1 # 退出脚本，trap 会被触发执行 cleanup
fi

echo "Starting Frontend Development Server..."
# 直接在根目录启动前端（因为我们已经将前端配置移到根目录）
cd "$PROJECT_ROOT"
npm run dev

# 当 npm run dev 退出时 (例如按 Ctrl+C)，尝试结束后台的后端进程
echo "Frontend server stopped. Stopping backend server (PID: $BACKEND_PID)..."
kill $BACKEND_PID
echo "Done." 
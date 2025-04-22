@echo off
setlocal

REM 如果不在后端目录，切换到后端目录
for %%I in (.) do set CUR_DIR=%%~nxI
if not "%CUR_DIR%"=="backend" (
    cd /d "%~dp0" || (
        echo 无法切换到后端目录
        exit /b 1
    )
)

REM 检查虚拟环境是否存在
if not exist venv (
    echo 错误：虚拟环境不存在，请先运行 setup_venv.bat
    exit /b 1
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 检查是否需要更新依赖
if "%1"=="update" (
    echo 更新依赖...
    pip install -r requirements.txt
)

REM 显示当前环境信息
echo =============================================
echo Flask 后端服务启动
python --version
echo 虚拟环境: %VIRTUAL_ENV%
echo =============================================

REM 启动Flask服务器
echo 启动Flask服务器...
flask run --host=0.0.0.0 %*

endlocal 
#!/bin/bash

# 清理项目结构脚本
echo "开始清理项目结构..."

# 备份重要文件
echo "1. 备份重要文件..."
mkdir -p backup
cp package.json backup/package.json.bak
cp vue-ysj/package.json backup/vue-ysj-package.json.bak

# 删除冗余HTML文件
echo "2. 替换当前的HTML文件..."
mv index.html index.html.original
mv index.html.new index.html

# 清理node_modules (这会花一些时间)
echo "3. 清理vue-ysj目录下的node_modules..."
rm -rf vue-ysj/node_modules
rm -rf vue-ysj/package-lock.json

# 复制其他必要文件
echo "4. 确保配置文件存在于根目录..."
if [ ! -f "postcss.config.cjs" ]; then
  cp vue-ysj/postcss.config.cjs ./
fi
if [ ! -f "tailwind.config.js" ]; then
  cp vue-ysj/tailwind.config.js ./
fi

# 安装依赖
echo "5. 重新安装依赖 (这可能需要几分钟)..."
npm install

# 确保项目能运行
echo "6. 设置权限..."
chmod +x start-dev.sh

echo "清理完成！现在您可以使用以下命令运行项目："
echo "npm run dev            # 仅运行前端"
echo "./start-dev.sh         # 同时运行前端和后端"
echo ""
echo "注意: 如果发现任何问题，备份文件位于 backup/ 目录下" 
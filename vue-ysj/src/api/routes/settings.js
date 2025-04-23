// 网站设置API路由
const express = require('express');
const router = express.Router();
const settingsModel = require('../models/settings');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { authenticateToken } = require('../middleware/auth');

// 配置文件上传
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    const uploadPath = path.join(__dirname, '../../public/uploads/logo');
    
    // 确保目录存在
    if (!fs.existsSync(uploadPath)) {
      fs.mkdirSync(uploadPath, { recursive: true });
    }
    
    cb(null, uploadPath);
  },
  filename: function (req, file, cb) {
    // 使用时间戳+原始扩展名生成文件名
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    const ext = path.extname(file.originalname);
    cb(null, 'logo-' + uniqueSuffix + ext);
  }
});

const upload = multer({
  storage: storage,
  limits: { fileSize: 5 * 1024 * 1024 }, // 限制5MB
  fileFilter: function (req, file, cb) {
    // 只允许图像格式
    const allowedTypes = /jpeg|jpg|png|gif|svg/;
    const ext = allowedTypes.test(path.extname(file.originalname).toLowerCase());
    const mimetype = allowedTypes.test(file.mimetype);
    
    if (ext && mimetype) {
      return cb(null, true);
    } else {
      cb(new Error('只允许上传JPEG、PNG、GIF或SVG格式的图片！'));
    }
  }
});

// 获取所有设置
router.get('/', async (req, res) => {
  try {
    const settings = await settingsModel.getAllSettings();
    res.json({ success: true, data: settings });
  } catch (error) {
    console.error('获取设置失败:', error);
    res.status(500).json({ success: false, message: '获取设置失败', error: error.message });
  }
});

// 更新设置 (需要管理员权限)
router.put('/', authenticateToken, async (req, res) => {
  try {
    // 确保用户是管理员
    if (req.user.role !== 'admin') {
      return res.status(403).json({ success: false, message: '权限不足' });
    }
    
    const settings = req.body;
    const updatedSettings = await settingsModel.updateSettings(settings);
    
    res.json({ success: true, data: updatedSettings, message: '设置已更新' });
  } catch (error) {
    console.error('更新设置失败:', error);
    res.status(500).json({ success: false, message: '更新设置失败', error: error.message });
  }
});

// 上传Logo (需要管理员权限)
router.post('/logo', authenticateToken, upload.single('logo'), async (req, res) => {
  try {
    // 确保用户是管理员
    if (req.user.role !== 'admin') {
      return res.status(403).json({ success: false, message: '权限不足' });
    }
    
    if (!req.file) {
      return res.status(400).json({ success: false, message: '未提供文件' });
    }
    
    // 生成URL路径 (相对路径，方便前端使用)
    const logoUrl = `/uploads/logo/${req.file.filename}`;
    
    // 更新logo设置
    const settings = { logo: logoUrl };
    await settingsModel.updateSettings(settings);
    
    res.json({ 
      success: true, 
      data: { logo: logoUrl }, 
      message: 'Logo上传成功'
    });
  } catch (error) {
    console.error('上传Logo失败:', error);
    res.status(500).json({ success: false, message: '上传Logo失败', error: error.message });
  }
});

module.exports = router; 
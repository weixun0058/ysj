// 网站设置模型
const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('./database.sqlite');

// 确保settings表存在
db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS settings (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      key TEXT UNIQUE NOT NULL,
      value TEXT,
      description TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
  `);
});

// 默认设置项列表
const defaultSettings = [
  { key: 'siteName', value: '塞外本草 - 壹世健', description: '网站名称' },
  { key: 'siteSlogan', value: '源自天山脚下，纯净自然', description: '网站口号' },
  { key: 'siteDescription', value: '源自天山脚下喀什河畔唐布拉大草原、由独特新疆黑蜂采集酿造的高品质蜂蜜', description: '网站描述' },
  { key: 'siteKeywords', value: '塞外本草,壹世健,新疆蜂蜜,天山蜂蜜,黑蜂蜜,唐布拉', description: '网站关键词' },
  { key: 'icp', value: '新ICP备XXXXXXXX号', description: 'ICP备案号' },
  { key: 'logo', value: '', description: '网站Logo' },
  { key: 'companyName', value: '塞外本草（新疆）生物科技有限公司', description: '公司名称' },
  { key: 'address', value: '新疆伊犁哈萨克自治州尼勒克县', description: '公司地址' },
  { key: 'phone', value: '400-123-4567', description: '联系电话' },
  { key: 'email', value: 'contact@saiwaibencao.com', description: '联系邮箱' },
  { key: 'workingHours', value: '周一至周五: 9:00-18:00', description: '工作时间' },
  { key: 'wechat', value: '@saiwaibencao', description: '微信公众号' },
  { key: 'weibo', value: '@塞外本草', description: '微博' },
  { key: 'douyin', value: '@塞外本草', description: '抖音' },
  { key: 'latitude', value: '43.789', description: '公司地址纬度' },
  { key: 'longitude', value: '82.512', description: '公司地址经度' }
];

// 初始化默认设置
const initDefaultSettings = () => {
  const stmt = db.prepare('INSERT OR IGNORE INTO settings (key, value, description) VALUES (?, ?, ?)');
  
  defaultSettings.forEach(setting => {
    stmt.run(setting.key, setting.value, setting.description);
  });
  
  stmt.finalize();
};

// 调用初始化默认设置
initDefaultSettings();

// 获取所有设置
const getAllSettings = () => {
  return new Promise((resolve, reject) => {
    db.all('SELECT key, value FROM settings', (err, rows) => {
      if (err) {
        return reject(err);
      }
      
      // 转换成对象格式
      const settings = {};
      rows.forEach(row => {
        settings[row.key] = row.value;
      });
      
      resolve(settings);
    });
  });
};

// 更新设置
const updateSettings = (settings) => {
  return new Promise((resolve, reject) => {
    // 开始事务
    db.serialize(() => {
      db.run('BEGIN TRANSACTION');
      
      const stmt = db.prepare(`
        UPDATE settings 
        SET value = ?, updated_at = CURRENT_TIMESTAMP 
        WHERE key = ?
      `);
      
      // 处理每个设置项
      Object.entries(settings).forEach(([key, value]) => {
        stmt.run(value, key);
      });
      
      stmt.finalize();
      
      db.run('COMMIT', (err) => {
        if (err) {
          db.run('ROLLBACK');
          return reject(err);
        }
        resolve(settings);
      });
    });
  });
};

// 保存Logo文件并更新设置
const updateLogoAndSettings = async (logoFile, settings) => {
  // 这里处理Logo文件的保存，可以使用fs模块保存到本地
  // 或者将Base64存储到数据库中
  // 为简化实现，这里假设logoFile已经是Base64格式的字符串
  
  // 合并设置并更新
  return await updateSettings(settings);
};

module.exports = {
  getAllSettings,
  updateSettings,
  updateLogoAndSettings
}; 
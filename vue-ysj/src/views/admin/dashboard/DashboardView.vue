<!-- 管理后台仪表盘 -->
<template>
  <div class="dashboard">
    <!-- 数据概览卡片 -->
    <div class="overview-cards">
      <div class="card">
        <div class="card-icon users-icon">
          <i class="fas fa-users"></i>
        </div>
        <div class="card-content">
          <h3>用户总数</h3>
          <p class="card-value">{{ userCount }}</p>
          <p class="card-trend">
            <span class="trend-up"><i class="fas fa-arrow-up"></i> 12%</span> 较上月
          </p>
        </div>
      </div>
      
      <div class="card">
        <div class="card-icon orders-icon">
          <i class="fas fa-shopping-cart"></i>
        </div>
        <div class="card-content">
          <h3>订单总数</h3>
          <p class="card-value">{{ orderCount }}</p>
          <p class="card-trend">
            <span class="trend-up"><i class="fas fa-arrow-up"></i> 8%</span> 较上月
          </p>
        </div>
      </div>
      
      <div class="card">
        <div class="card-icon revenue-icon">
          <i class="fas fa-yuan-sign"></i>
        </div>
        <div class="card-content">
          <h3>销售额 (元)</h3>
          <p class="card-value">{{ revenue }}</p>
          <p class="card-trend">
            <span class="trend-up"><i class="fas fa-arrow-up"></i> 15%</span> 较上月
          </p>
        </div>
      </div>
      
      <div class="card">
        <div class="card-icon products-icon">
          <i class="fas fa-box"></i>
        </div>
        <div class="card-content">
          <h3>产品总数</h3>
          <p class="card-value">{{ productCount }}</p>
          <p class="card-trend">
            <span class="trend-up"><i class="fas fa-arrow-up"></i> 5%</span> 较上月
          </p>
        </div>
      </div>
    </div>
    
    <!-- 图表区域 -->
    <div class="chart-section">
      <div class="chart-container">
        <h3>销售趋势</h3>
        <div class="chart-placeholder">
          <p>这里将显示销售趋势图表</p>
        </div>
      </div>
      
      <div class="chart-container">
        <h3>热销商品</h3>
        <div class="chart-placeholder">
          <p>这里将显示热销商品图表</p>
        </div>
      </div>
    </div>
    
    <!-- 最新订单 -->
    <div class="recent-orders">
      <div class="section-header">
        <h3>最新订单</h3>
        <router-link to="/admin/orders" class="view-all">查看全部</router-link>
      </div>
      
      <div class="order-table-container">
        <table class="order-table">
          <thead>
            <tr>
              <th>订单号</th>
              <th>客户</th>
              <th>日期</th>
              <th>金额</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in recentOrders" :key="order.id">
              <td>{{ order.id }}</td>
              <td>{{ order.customer }}</td>
              <td>{{ order.date }}</td>
              <td>¥{{ order.amount }}</td>
              <td>
                <span :class="'status-badge ' + order.statusClass">
                  {{ order.status }}
                </span>
              </td>
              <td>
                <router-link :to="`/admin/orders/${order.id}`" class="action-btn">
                  <i class="fas fa-eye"></i>
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// 模拟数据（实际应从API获取）
const userCount = ref(0);
const orderCount = ref(0);
const revenue = ref(0);
const productCount = ref(0);
const recentOrders = ref([]);

// 获取仪表盘数据
const fetchDashboardData = () => {
  // 模拟API请求延迟
  setTimeout(() => {
    userCount.value = 1248;
    orderCount.value = 856;
    revenue.value = '198,356.00';
    productCount.value = 64;
    
    // 模拟最近订单数据
    recentOrders.value = [
      { 
        id: 'ORD20250001', 
        customer: '李明', 
        date: '2025-05-01', 
        amount: '1,299.00', 
        status: '已发货', 
        statusClass: 'shipped' 
      },
      { 
        id: 'ORD20250002', 
        customer: '张华', 
        date: '2025-05-01', 
        amount: '459.00', 
        status: '待付款', 
        statusClass: 'pending' 
      },
      { 
        id: 'ORD20250003', 
        customer: '王芳', 
        date: '2025-04-30', 
        amount: '2,158.00', 
        status: '已完成', 
        statusClass: 'completed' 
      },
      { 
        id: 'ORD20250004', 
        customer: '赵雷', 
        date: '2025-04-30', 
        amount: '899.00', 
        status: '已发货', 
        statusClass: 'shipped' 
      },
      { 
        id: 'ORD20250005', 
        customer: '刘青', 
        date: '2025-04-29', 
        amount: '3,499.00', 
        status: '已完成', 
        statusClass: 'completed' 
      }
    ];
  }, 500);
};

onMounted(() => {
  fetchDashboardData();
});
</script>

<style scoped>
.dashboard {
  padding: 1rem 0;
}

/* 数据概览卡片样式 */
.overview-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.card {
  background-color: var(--card-background, #1a1a1a);
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  color: var(--text-color-light, #f0f0f0);
}

.card-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  font-size: 1.5rem;
  color: #fff;
}

.users-icon {
  background-color: #3498db;
}

.orders-icon {
  background-color: #e74c3c;
}

.revenue-icon {
  background-color: #2ecc71;
}

.products-icon {
  background-color: #f39c12;
}

.card-content {
  flex-grow: 1;
}

.card-content h3 {
  font-size: 0.875rem;
  color: var(--text-color-light, #f0f0f0);
  opacity: 0.7;
  margin: 0 0 0.5rem;
}

.card-value {
  font-size: 1.75rem;
  font-weight: 600;
  margin: 0 0 0.5rem;
  color: var(--text-color-light, #f0f0f0);
}

.card-trend {
  font-size: 0.75rem;
  color: var(--text-color-light, #f0f0f0);
  opacity: 0.7;
  margin: 0;
}

.trend-up {
  color: #2ecc71;
}

.trend-down {
  color: #e74c3c;
}

/* 图表区域样式 */
.chart-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.chart-container {
  background-color: var(--card-background, #1a1a1a);
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.chart-container h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1rem;
  color: var(--text-color-light, #f0f0f0);
}

.chart-placeholder {
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
  color: var(--text-color-light, #f0f0f0);
  opacity: 0.6;
}

/* 最新订单样式 */
.recent-orders {
  background-color: var(--card-background, #1a1a1a);
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h3 {
  margin: 0;
  font-size: 1rem;
  color: var(--text-color-light, #f0f0f0);
}

.view-all {
  color: var(--primary-color, #fa964b);
  text-decoration: none;
  font-size: 0.875rem;
}

.order-table-container {
  overflow-x: auto;
}

.order-table {
  width: 100%;
  border-collapse: collapse;
}

.order-table th,
.order-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color, #444);
  color: var(--text-color-light, #f0f0f0);
}

.order-table th {
  font-weight: 500;
  color: var(--text-color-light, #f0f0f0);
  opacity: 0.7;
  font-size: 0.875rem;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-badge.completed {
  background-color: rgba(46, 204, 113, 0.2);
  color: #2ecc71;
}

.status-badge.pending {
  background-color: rgba(243, 156, 18, 0.2);
  color: #f39c12;
}

.status-badge.shipped {
  background-color: rgba(52, 152, 219, 0.2);
  color: #3498db;
}

.status-badge.cancelled {
  background-color: rgba(231, 76, 60, 0.2);
  color: #e74c3c;
}

.action-btn {
  color: var(--primary-color, #fa964b);
  text-decoration: none;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .overview-cards {
    grid-template-columns: repeat(auto-fit, minmax(100%, 1fr));
  }
  
  .chart-section {
    grid-template-columns: 1fr;
  }
}
</style> 
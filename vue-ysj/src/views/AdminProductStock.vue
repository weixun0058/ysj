<template>
  <div class="admin-stock-page">
    <h1>产品库存管理</h1>
    
    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="输入产品名称搜索"
        prefix-icon="el-icon-search"
        clearable
        @keyup.enter.native="handleSearch"
      />
      <el-button type="primary" @click="handleSearch">搜索</el-button>
      <el-button @click="resetSearch">重置</el-button>
    </div>
    
    <el-table
      :data="filteredProducts"
      border
      stripe
      style="width: 100%; margin-top: 20px;"
      v-loading="loading"
    >
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column label="产品图片" width="120">
        <template #default="scope">
          <el-image
            style="width: 80px; height: 80px"
            :src="scope.row.main_image"
            fit="cover"
            :preview-src-list="[scope.row.main_image]"
          >
            <template #error>
              <div class="image-placeholder">暂无图片</div>
            </template>
          </el-image>
        </template>
      </el-table-column>
      <el-table-column prop="name" label="产品名称" min-width="200" />
      <el-table-column label="价格" width="120">
        <template #default="scope">
          <span>¥ {{ scope.row.price.toFixed(2) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="库存信息" width="300">
        <template #default="scope">
          <div class="stock-info">
            <div class="stock-item">
              <span class="stock-label">总库存:</span>
              <span class="stock-value">{{ getStockInfo(scope.row).total_stock }}</span>
            </div>
            <div class="stock-item">
              <span class="stock-label">可用库存:</span>
              <span class="stock-value">{{ getStockInfo(scope.row).available_stock }}</span>
            </div>
            <div class="stock-item">
              <span class="stock-label">预扣库存:</span>
              <span class="stock-value">{{ getStockInfo(scope.row).prelock_stock }}</span>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="库存状态" width="120">
        <template #default="scope">
          <el-tag v-if="getStockInfo(scope.row).total_stock <= 0" type="danger">缺货</el-tag>
          <el-tag v-else-if="getStockInfo(scope.row).total_stock <= 10" type="warning">库存低</el-tag>
          <el-tag v-else type="success">库存充足</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="220">
        <template #default="scope">
          <el-button 
            size="small" 
            type="primary" 
            @click="openAdjustStockDialog(scope.row)"
          >
            调整库存
          </el-button>
          <el-button 
            size="small" 
            type="info" 
            @click="viewStockLogs(scope.row.id)"
          >
            查看记录
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <el-pagination
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-size="pageSize"
      layout="total, prev, pager, next, jumper"
      :total="totalProducts"
      style="margin-top: 20px; text-align: center;"
    />
    
    <!-- 调整库存弹窗 -->
    <el-dialog
      title="调整产品库存"
      :visible.sync="adjustStockDialogVisible"
      width="500px"
    >
      <div v-if="selectedProduct" class="adjust-stock-dialog">
        <div class="product-info">
          <h3>{{ selectedProduct.name }}</h3>
          <div class="current-stock-info">
            <p><strong>当前总库存:</strong> {{ getStockInfo(selectedProduct).total_stock }}</p>
            <p><strong>当前可用库存:</strong> {{ getStockInfo(selectedProduct).available_stock }}</p>
            <p><strong>当前预扣库存:</strong> {{ getStockInfo(selectedProduct).prelock_stock }}</p>
          </div>
        </div>
        
        <el-form :model="adjustForm" :rules="adjustRules" ref="adjustForm" label-width="100px">
          <el-form-item label="调整数量" prop="adjustTotal">
            <el-input-number 
              v-model="adjustForm.adjustTotal" 
              :step="1"
              controls-position="right"
            />
            <span class="adjust-tip">正数增加，负数减少</span>
          </el-form-item>
          
          <el-form-item label="调整后库存">
            <span class="preview-value">{{ getStockInfo(selectedProduct).total_stock + adjustForm.adjustTotal }}</span>
          </el-form-item>
          
          <el-form-item label="调整原因" prop="remark">
            <el-input
              type="textarea"
              v-model="adjustForm.remark"
              placeholder="请输入库存调整原因"
              :rows="3"
            />
          </el-form-item>
        </el-form>
        
        <div slot="footer" class="dialog-footer">
          <el-button @click="adjustStockDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitAdjustStock" :loading="submitting">确认调整</el-button>
        </div>
      </div>
    </el-dialog>
    
    <!-- 库存记录弹窗 -->
    <el-dialog
      title="库存变动记录"
      :visible.sync="stockLogsDialogVisible"
      width="800px"
    >
      <div class="stock-logs-container" v-loading="logsLoading">
        <el-table
          :data="stockLogs"
          border
          stripe
          style="width: 100%"
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column label="变动时间" width="180">
            <template #default="scope">
              {{ formatDateTime(scope.row.created_time) }}
            </template>
          </el-table-column>
          <el-table-column label="变动类型" width="120">
            <template #default="scope">
              <el-tag :type="getChangeTypeTag(scope.row.change_type)">
                {{ getChangeTypeLabel(scope.row.change_type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="变动数量" width="100">
            <template #default="scope">
              <span :class="{'stock-increase': scope.row.change_amount > 0, 'stock-decrease': scope.row.change_amount < 0}">
                {{ scope.row.change_amount > 0 ? '+' : '' }}{{ scope.row.change_amount }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="变动前库存" width="200">
            <template #default="scope">
              <div>总库存: {{ scope.row.before_total }}</div>
              <div>可用: {{ scope.row.before_available }}</div>
              <div>预扣: {{ scope.row.before_prelock }}</div>
            </template>
          </el-table-column>
          <el-table-column label="变动后库存" width="200">
            <template #default="scope">
              <div>总库存: {{ scope.row.before_total + scope.row.change_amount }}</div>
              <div>可用: {{ calculateAfterAvailable(scope.row) }}</div>
              <div>预扣: {{ scope.row.before_prelock }}</div>
            </template>
          </el-table-column>
          <el-table-column prop="remark" label="备注" min-width="200" show-overflow-tooltip />
        </el-table>
        
        <div v-if="stockLogs.length === 0 && !logsLoading" class="no-logs-message">
          暂无库存变动记录
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default {
  name: 'AdminProductStock',
  data() {
    return {
      loading: false,
      products: [],
      filteredProducts: [],
      searchKeyword: '',
      currentPage: 1,
      pageSize: 10,
      totalProducts: 0,
      
      // 调整库存相关
      adjustStockDialogVisible: false,
      selectedProduct: null,
      adjustForm: {
        adjustTotal: 0,
        remark: ''
      },
      adjustRules: {
        adjustTotal: [
          { required: true, message: '请输入调整数量', trigger: 'blur' }
        ],
        remark: [
          { required: true, message: '请输入调整原因', trigger: 'blur' }
        ]
      },
      submitting: false,
      
      // 库存记录相关
      stockLogsDialogVisible: false,
      stockLogs: [],
      logsLoading: false,
      currentProductId: null
    };
  },
  created() {
    this.fetchProducts();
  },
  methods: {
    // 获取产品列表
    async fetchProducts() {
      this.loading = true;
      try {
        const response = await axios.get('/api/products');
        if (response.data.success) {
          this.products = response.data.products;
          this.applyFilters();
          this.totalProducts = this.filteredProducts.length;
        } else {
          ElMessage.error(response.data.message || '获取产品列表失败');
        }
      } catch (error) {
        console.error('获取产品列表出错:', error);
        ElMessage.error('获取产品列表失败: ' + (error.response?.data?.message || error.message));
      } finally {
        this.loading = false;
      }
    },
    
    // 获取产品库存信息
    getStockInfo(product) {
      return {
        total_stock: product.stock?.total_stock || 0,
        available_stock: product.stock?.available_stock || 0,
        prelock_stock: product.stock?.prelock_stock || 0
      };
    },
    
    // 搜索和过滤
    handleSearch() {
      this.currentPage = 1;
      this.applyFilters();
    },
    
    resetSearch() {
      this.searchKeyword = '';
      this.currentPage = 1;
      this.applyFilters();
    },
    
    applyFilters() {
      const keyword = this.searchKeyword.toLowerCase().trim();
      
      if (keyword) {
        this.filteredProducts = this.products.filter(product => 
          product.name.toLowerCase().includes(keyword) || 
          String(product.id) === keyword
        );
      } else {
        this.filteredProducts = [...this.products];
      }
      
      this.totalProducts = this.filteredProducts.length;
      this.updatePagedData();
    },
    
    updatePagedData() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      this.filteredProducts = this.filteredProducts.slice(start, end);
    },
    
    handleCurrentChange(page) {
      this.currentPage = page;
      this.applyFilters();
    },
    
    // 调整库存相关方法
    openAdjustStockDialog(product) {
      this.selectedProduct = {...product};
      this.adjustForm = {
        adjustTotal: 0,
        remark: ''
      };
      this.adjustStockDialogVisible = true;
    },
    
    async submitAdjustStock() {
      this.$refs.adjustForm.validate(async (valid) => {
        if (!valid) return;
        
        // 验证库存调整数量
        const currentTotal = this.getStockInfo(this.selectedProduct).total_stock;
        if (currentTotal + this.adjustForm.adjustTotal < 0) {
          ElMessage.error('调整后的库存不能小于0');
          return;
        }
        
        this.submitting = true;
        try {
          const response = await axios.post(
            `/api/products/${this.selectedProduct.id}/adjust-stock`,
            {
              adjust_total: this.adjustForm.adjustTotal,
              remark: this.adjustForm.remark
            }
          );
          
          if (response.data.success) {
            ElMessage.success('库存调整成功');
            // 更新本地产品库存数据
            const index = this.products.findIndex(p => p.id === this.selectedProduct.id);
            if (index !== -1) {
              // 深拷贝以确保响应式更新
              const updatedProduct = {...this.products[index]};
              
              // 确保stock对象存在
              if (!updatedProduct.stock) {
                updatedProduct.stock = {
                  total_stock: 0,
                  available_stock: 0,
                  prelock_stock: 0
                };
              }
              
              // 更新库存数据
              updatedProduct.stock.total_stock = response.data.data.current_stock.total;
              updatedProduct.stock.available_stock = response.data.data.current_stock.available;
              updatedProduct.stock.prelock_stock = response.data.data.current_stock.prelock;
              
              // 更新本地数据
              this.products.splice(index, 1, updatedProduct);
              
              // 更新选中的产品
              this.selectedProduct = updatedProduct;
            }
            
            // 关闭弹窗
            this.adjustStockDialogVisible = false;
          } else {
            ElMessage.error(response.data.message || '库存调整失败');
          }
        } catch (error) {
          console.error('调整库存出错:', error);
          ElMessage.error('库存调整失败: ' + (error.response?.data?.message || error.message));
        } finally {
          this.submitting = false;
        }
      });
    },
    
    // 库存记录相关方法
    async viewStockLogs(productId) {
      this.currentProductId = productId;
      this.stockLogs = [];
      this.stockLogsDialogVisible = true;
      this.logsLoading = true;
      
      try {
        const response = await axios.get(`/api/products/${productId}/stock-logs`);
        if (response.data.success) {
          this.stockLogs = response.data.logs || [];
        } else {
          ElMessage.error(response.data.message || '获取库存记录失败');
        }
      } catch (error) {
        console.error('获取库存记录出错:', error);
        ElMessage.error('获取库存记录失败: ' + (error.response?.data?.message || error.message));
      } finally {
        this.logsLoading = false;
      }
    },
    
    // 工具方法
    formatDateTime(timestamp) {
      if (!timestamp) return '-';
      const date = new Date(timestamp);
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
    },
    
    getChangeTypeLabel(type) {
      const types = {
        1: '订单创建',
        2: '订单取消',
        3: '订单支付',
        4: '后台调整',
        5: '初始化'
      };
      return types[type] || '未知类型';
    },
    
    getChangeTypeTag(type) {
      const tags = {
        1: 'warning',    // 订单创建 - 警告色
        2: 'info',       // 订单取消 - 信息色
        3: 'success',    // 订单支付 - 成功色
        4: 'primary',    // 后台调整 - 主要色
        5: 'info'        // 初始化 - 信息色
      };
      return tags[type] || '';
    },
    
    calculateAfterAvailable(log) {
      // 根据不同操作类型计算变动后的可用库存
      switch (log.change_type) {
        case 1: // 订单创建 - 减少可用库存
          return log.before_available + log.change_amount;
        case 2: // 订单取消 - 增加可用库存
          return log.before_available + Math.abs(log.change_amount);
        case 4: // 后台调整 - 同时调整总库存和可用库存
          return log.before_available + log.change_amount;
        default:
          return log.before_available;
      }
    }
  }
};
</script>

<style scoped>
.admin-stock-page {
  padding: 20px;
}

.search-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.stock-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.stock-item {
  display: flex;
  justify-content: space-between;
}

.stock-label {
  font-weight: bold;
  margin-right: 5px;
}

.image-placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80px;
  background-color: #f5f7fa;
  color: #909399;
  font-size: 12px;
}

.adjust-stock-dialog {
  padding: 0 20px;
}

.product-info {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.current-stock-info {
  margin-top: 15px;
}

.adjust-tip {
  margin-left: 10px;
  color: #909399;
  font-size: 12px;
}

.preview-value {
  font-size: 16px;
  font-weight: bold;
  color: #409EFF;
}

.dialog-footer {
  text-align: right;
  margin-top: 20px;
}

.stock-increase {
  color: #67C23A;
  font-weight: bold;
}

.stock-decrease {
  color: #F56C6C;
  font-weight: bold;
}

.no-logs-message {
  text-align: center;
  margin: 30px 0;
  color: #909399;
  font-size: 14px;
}
</style> 
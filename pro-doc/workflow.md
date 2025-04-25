# 塞外本草 / 壹世健 官方网站 - 开发工作流程

## 1. 开发流程

### 1.1 版本控制工作流

本项目采用 **GitHub Flow** 简化版本控制工作流:

1. 从 `main` 分支创建特性分支 (命名格式: `feat/<feature-name>`) 或修复分支 (`fix/<issue-description>`)。
2. 在分支上进行开发，定期提交代码，每次提交遵循 **Conventional Commits** 规范。
3. 开发完成后，创建 Pull Request (PR) 向 `main` 分支合并。
4. 至少一名团队成员进行代码审查 (Code Review) 并批准。
5. PR 合并后，分支可以删除。

### 1.2 提交信息规范

提交信息必须遵循 **Conventional Commits** 规范:
```
<type>(<scope>): <subject>
```

- **type**: 
  - `feat`: 新功能
  - `fix`: Bug修复
  - `docs`: 文档更新
  - `style`: 代码风格/格式调整
  - `refactor`: 重构
  - `perf`: 性能优化
  - `test`: 测试相关
  - `chore`: 构建/工具相关

- **scope** (可选): 修改范围，如 `api`, `ui`, `auth` 等。
- **subject**: 简洁描述本次提交的目的。

例如:
```
feat(home): 实现首页轮播图组件
fix(cart): 修复购物车数量不更新的问题
```

## 2. 开发环境搭建

### 2.1 前置要求

- **Python** 3.10+
- **Node.js** 18+ (推荐使用 LTS 版本)
- **SQLite** 本地实例
- **Redis** (可选，用于缓存)
- **Git**

### 2.2 本地开发环境配置

参考 `README.md` 中的环境配置说明。

## 3. 后端开发工作流

1. 在 `flask-app/app/models/` 中定义数据模型。
2. 使用 Flask-Migrate 生成数据库迁移脚本。
3. 在 `flask-app/app/apis/` 下按功能模块实现 API 接口。
4. 编写对应的单元测试和集成测试。
5. 本地测试 API 功能。

### 3.1 数据库迁移流程

当模型发生变化时:
```bash
cd flask-app
flask db migrate -m "描述变更内容"
flask db upgrade
```

## 4. 前端开发工作流

1. 在 `vue-app/src/views/` 下创建页面组件。
2. 在 `vue-app/src/components/` 下创建可复用组件。
3. 在 `vue-app/src/router/` 中配置路由。
4. 在 `vue-app/src/stores/` 中实现状态管理。
5. 在 `vue-app/src/services/` 中封装 API 调用。

### 4.1 响应式设计说明

所有页面必须适配:
- 桌面端 (>= 1200px)
- 平板端 (768px - 1199px)
- 移动端 (<= 767px)

使用 CSS 媒体查询或 UI 框架的响应式布局系统确保适配。

## 5. 测试策略

### 5.1 后端测试

- 单元测试: 使用 `pytest` 测试核心业务逻辑、工具函数和模型方法。
- 集成测试: 测试 API 端点的功能和流程。

### 5.2 前端测试

- 单元测试: 使用 Vitest 测试组件、Composable 函数和 Pinia stores。
- E2E 测试: 使用 Cypress 测试关键用户流程。

## 6. 部署流程

(后续补充生产环境部署流程详情)

## 7. 联调与交互

前后端开发人员通过以下方式进行协作:

1. 先统一定义 API 接口规范，包括:
   - 接口路径
   - 请求方法
   - 请求参数/请求体格式
   - 响应体格式
   - 错误处理

2. 后端可以先提供 Mock 数据，前端据此开发界面。

3. 后端 API 就绪后，前端切换到实际 API 进行联调。

## 8. 问题追踪与解决

使用 GitHub Issues / GitLab Issues 跟踪问题和功能需求。每个 Issue 应包含:

- 清晰的标题
- 详细的描述
- 重现步骤 (适用于 Bug)
- 截图或录屏 (如果适用)
- 标签/优先级标记

## 9. 文档更新

随着项目进展，及时更新以下文档:

- `README.md`: 项目概览与基本说明
- `workflow.md` (本文档): 开发流程
- API 文档: 后端 API 说明
- 组件文档: 前端可复用组件说明 (可选) 
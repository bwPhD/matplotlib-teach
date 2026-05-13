# Streamlit 应用自动唤醒系统

本项目实现了使用 GitHub Actions 自动唤醒 Streamlit Cloud 应用的方案，解决免费层应用休眠的问题。

## 🎯 方案概述

Streamlit Cloud 的免费层应用在无人访问时会自动休眠，只能由应用所有者手动唤醒。本方案使用 GitHub Actions 创建定时任务，每 4 小时自动访问应用进行唤醒。

## 📋 设置步骤

### 1. 配置 GitHub Secrets

在你的 GitHub 仓库中设置以下 Secret：

1. 进入仓库的 **Settings** 页面
2. 点击左侧菜单的 **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加以下 Secret：

| Name | Value | Description |
|------|-------|-------------|
| `STREAMLIT_URL` | `https://your-app-name.streamlit.app` | 你的 Streamlit 应用 URL |

### 2. 推送代码到 GitHub

确保以下文件已推送到 GitHub：

```
.github/
├── workflows/
│   └── wake_up_app.yml          # GitHub Actions 工作流
├── scripts/
│   └── wake_up_app.py           # 唤醒脚本
└── logs/
    └── .gitkeep                 # 日志目录占位符
```

### 3. 启用工作流

1. 进入仓库的 **Actions** 标签页
2. 启用 workflows（如果被禁用）
3. 工作流会自动按计划运行

## ⚙️ 工作流配置

### 定时计划

工作流配置为每 4 小时运行一次：
- 运行时间：00:00, 04:00, 08:00, 12:00, 16:00, 20:00 (UTC)

```yaml
schedule:
  - cron: '0 */4 * * *'
```

### 手动触发

你也可以手动触发工作流：
1. 进入 **Actions** 标签页
2. 选择 **Wake Up Streamlit App** 工作流
3. 点击 **Run workflow**

## 🔍 监控和日志

### 查看运行日志

1. 进入仓库的 **Actions** 标签页
2. 点击最新的工作流运行
3. 查看运行日志和结果

### 日志文件

唤醒脚本会在本地生成日志文件：
- `.github/logs/wake_up.log`

注意：GitHub Actions 的日志文件不会自动推送到仓库。

## 🛠️ 自定义配置

### 修改唤醒频率

编辑 `.github/workflows/wake_up_app.yml` 中的 cron 表达式：

```yaml
schedule:
  - cron: '0 */6 * * *'  # 每6小时
  - cron: '0 */2 * * *'  # 每2小时
  - cron: '0 9 * * *'    # 每天早上9点
```

### 修改重试次数

编辑 `wake_up_app.py` 中的 `max_retries` 参数：

```python
success = wake_up_streamlit_app(app_url, max_retries=5)  # 增加到5次重试
```

## 🚨 故障排除

### 常见问题

1. **工作流运行失败**
   - 检查 `STREAMLIT_URL` Secret 是否正确设置
   - 确认应用 URL 可以公开访问

2. **Selenium 无法加载页面**
   - Streamlit Cloud 可能有反爬虫机制
   - 尝试增加等待时间或修改用户代理

3. **应用仍然休眠**
   - 检查应用 URL 是否正确
   - 确认应用没有其他访问限制

### 调试技巧

1. **本地测试**
   ```bash
   export STREAMLIT_URL="https://your-app.streamlit.app"
   python .github/scripts/wake_up_app.py
   ```

2. **查看详细日志**
   - 在 GitHub Actions 日志中查看详细输出
   - 检查 `.github/logs/wake_up.log` 文件

## 💡 优化建议

### 1. 智能唤醒

可以根据应用的使用模式调整唤醒时间：
- 如果用户主要在工作时间使用，可以只在工作时间唤醒
- 如果用户主要在周末使用，可以增加周末的唤醒频率

### 2. 多应用支持

如果有多个 Streamlit 应用，可以：
- 为每个应用创建单独的工作流
- 或者修改脚本支持多个 URL

### 3. 错误通知

添加邮件或 Slack 通知，当唤醒失败时及时提醒：
```yaml
- name: Send notification
  if: failure()
  run: curl -X POST -H 'Content-type: application/json' --data '{"text":"Streamlit app wake up failed"}' $SLACK_WEBHOOK_URL
```

## 🔒 安全注意事项

1. **不要泄露应用 URL**：确保应用 URL 不会在日志或错误信息中泄露
2. **定期检查**：定期检查 GitHub Actions 的使用情况，避免超出免费额度
3. **监控成本**：GitHub Actions 有一定的免费额度，监控使用情况

## 📊 资源使用

- **GitHub Actions 免费额度**：每月 2000 分钟
- **每次运行时间**：约 1-2 分钟
- **每月可用次数**：约 1000-2000 次

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个自动唤醒系统！

## 📄 许可证

本项目遵循与主项目相同的许可证。

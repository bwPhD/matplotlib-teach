# Phase 3 & 4: Color / Text / Axes / Figure 类 - 实施总结

## ✅ 已完成的工作

### Phase 3: Color 类参数 ✅

#### 1. 创建 `catalogs/color.py` 模块（约 400 行）

**color 参数目录**：
- **动态提取**：
  - CSS4 颜色：148 个（从 `matplotlib.colors.CSS4_COLORS`）
  - Base 颜色：8 个（`'r'`, `'g'`, `'b'` 等）
  - Tab10 颜色：10 个
  - CN 颜色：C0-C9（10 个）
- **预览画廊**：
  - Base 颜色：8 个单字符颜色预览
  - CN 颜色：C0-C9 网格预览（2×5）
  - CSS4 颜色：24 个常用颜色预览（4 列布局）
  - 颜色形式对比：7 种不同形式（名称/单字符/CN/HEX/RGB/RGBA/灰度）
- **交互式预览**：可选择颜色形式并实时预览
- **常见坑**：6 条重要注意事项

**cmap 参数目录**：
- **动态提取**：从 `plt.colormaps()` 获取所有 180 个 colormap
- **分类展示**：按类别组织（Perceptually Uniform Sequential、Sequential、Diverging、Cyclic、Qualitative、Miscellaneous）
- **预览画廊**：
  - 常用 Colormap：12 个（3 列布局）
  - 按类别展示：每个类别独立 Tab，显示前 30 个
- **交互式预览**：可选择 colormap 和数据类型（2D 图像/散点图/等高线）
- **常见坑**：6 条重要注意事项

### Phase 4: Text / Axes / Figure 类参数 ✅

#### 2. 创建 `catalogs/text.py` 模块（约 300 行）

**fontsize 参数目录**：
- **选项提取**：数值（1-100）和字符串（xx-small 到 xx-large）
- **预览画廊**：常用数值大小（6-30）和字符串大小对比
- **交互式预览**：可选择数值或字符串大小
- **常见坑**：4 条注意事项

**fontweight 参数目录**：
- **选项提取**：从 API 获取所有 fontweight 选项（19 个）
- **预览画廊**：常用 fontweight（9 个）对比
- **常见坑**：3 条注意事项

**fontstyle 参数目录**：
- **选项提取**：`'normal'`, `'italic'`, `'oblique'`（3 个）
- **预览画廊**：3 种样式对比
- **常见坑**：2 条注意事项

**fontfamily 参数目录**：
- **选项提取**：
  - 通用字体族：5 个（serif, sans-serif, monospace, cursive, fantasy）
  - 系统可用字体：最多 50 个（从 `font_manager` 获取）
- **预览画廊**：通用字体族预览
- **常见坑**：3 条注意事项

#### 3. 创建 `catalogs/axes.py` 模块（约 250 行）

**xlim/ylim 参数目录**：
- **预览画廊**：不同范围设置对比（自动/自定义/仅 X/仅 Y）
- **交互式预览**：可调整 X 和 Y 的范围
- **常见坑**：3 条注意事项

**grid 参数目录**：
- **预览画廊**：7 种不同 grid 设置（无网格/默认/虚线/半透明/彩色/仅 X/仅 Y）
- **常见坑**：3 条注意事项

**spines 参数目录**：
- **预览画廊**：6 种不同 spines 设置（默认/隐藏上/隐藏右/隐藏上下/仅下左/彩色边框）
- **代码示例**：spines 操作代码
- **常见坑**：3 条注意事项

#### 4. 创建 `catalogs/figure.py` 模块（约 200 行）

**figsize 参数目录**：
- **预览画廊**：6 种常用尺寸（小图/标准/宽图/高图/大图）
- **交互式预览**：可调整宽度和高度
- **常见坑**：4 条注意事项

**dpi 参数目录**：
- **说明表格**：5 种常用 DPI 值（72/100/150/300/600）
- **常见坑**：3 条注意事项

**facecolor/edgecolor 参数目录**：
- **预览画廊**：4 种不同背景颜色（白色/浅灰色/黑色/浅蓝色）
- **代码示例**：设置背景和边框颜色
- **常见坑**：3 条注意事项

### 5. 主应用集成 ✅

**app.py 修改**：
- 在章节 4 "布局与美学 (Layout & Style)" 中添加模式切换
- 用户可选择：
  - **交互式调整**：原有功能（保留）
  - **参数百科 (Catalog)**：新增的百科全书功能
- 类别选择：Text (文本) / Axes (坐标轴) / Figure (画布) / Color (颜色)
- 每个类别下可选择具体参数

## 📊 统计数据

### Phase 3: Color 类
- **color 选项数**：148 (CSS4) + 8 (Base) + 10 (CN) = 166+ 个
- **cmap 选项数**：180 个
- **代码行数**：约 400 行

### Phase 4: Text / Axes / Figure 类
- **Text 参数**：4 个（fontsize, fontweight, fontstyle, fontfamily）
- **Axes 参数**：3 个（xlim/ylim, grid, spines）
- **Figure 参数**：3 个（figsize, dpi, facecolor/edgecolor）
- **代码行数**：约 750 行（text: 300, axes: 250, figure: 200）

## 🎯 使用方法

### Color 类参数
1. 侧边栏 → "4. 布局与美学 (Layout & Style)"
2. 选择 "参数百科 (Catalog)"
3. 选择类别 "Color (颜色)"
4. 选择参数（`color` 或 `cmap`）

### Text / Axes / Figure 类参数
1. 侧边栏 → "4. 布局与美学 (Layout & Style)"
2. 选择 "参数百科 (Catalog)"
3. 选择类别（Text / Axes / Figure）
4. 选择具体参数

## 🔍 技术实现细节

### Color 类
- **动态提取**：
  - `matplotlib.colors.CSS4_COLORS` → CSS4 颜色
  - `matplotlib.colors.BASE_COLORS` → Base 颜色
  - `plt.colormaps()` → 所有 colormap（180 个）
- **分类策略**：colormap 按名称特征自动分类

### Text 类
- **动态提取**：
  - fontsize：硬编码常用值 + 字符串映射
  - fontweight：从 API 获取（19 个）
  - fontstyle：硬编码（3 个）
  - fontfamily：从 `font_manager` 获取系统字体

### Axes / Figure 类
- **参数说明**：基于文档和常见用法
- **预览画廊**：展示不同设置的效果对比

## 📝 代码示例

### Color 使用示例
```python
# 颜色名称
ax.plot(x, y, color='red')

# CN 颜色
ax.plot(x, y, color='C0')

# HEX
ax.plot(x, y, color='#FF5733')

# RGB
ax.plot(x, y, color=(1.0, 0.34, 0.2))

# Colormap
ax.scatter(x, y, c=values, cmap='viridis')
```

### Text 使用示例
```python
ax.set_title("Title", fontsize=16, fontweight='bold', fontfamily='serif')
ax.set_xlabel("X Label", fontsize=12, fontstyle='italic')
```

### Axes 使用示例
```python
ax.set_xlim(0, 10)
ax.set_ylim(-1, 1)
ax.grid(True, alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```

### Figure 使用示例
```python
fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
fig.set_facecolor('lightgray')
fig.set_edgecolor('blue')
```

## ⚠️ 注意事项

1. **Color**：
   - RGB 值范围是 0-1，不是 0-255
   - 灰度值必须是字符串，不是浮点数
   - CN 颜色会自动循环（C10 = C0）

2. **Text**：
   - fontsize 单位是"点"（points）
   - 不是所有字体都支持所有粗细级别

3. **Axes**：
   - xlim/ylim 不会裁剪数据，只改变显示范围
   - spines 有四个位置：top, bottom, left, right

4. **Figure**：
   - figsize 单位是英寸，不是像素
   - DPI 主要影响保存图像的质量

## 🚀 完成情况

### 已实现参数（总计 20+ 个）

**Line 类**（4 个）：linestyle, drawstyle, capstyle, joinstyle ✅
**Marker 类**（2 个）：marker, fillstyle ✅
**Color 类**（2 个）：color, cmap ✅
**Text 类**（4 个）：fontsize, fontweight, fontstyle, fontfamily ✅
**Axes 类**（3 个）：xlim/ylim, grid, spines ✅
**Figure 类**（3 个）：figsize, dpi, facecolor/edgecolor ✅

### 待扩展参数（可选）

- **Line 类**：linewidth, dashes, alpha, zorder
- **Marker 类**：markersize, markeredgewidth, markeredgecolor, markeredgecoloralt
- **Color 类**：norm
- **Text 类**：rotation, ha, va
- **Axes 类**：xlabel, ylabel, xticks, yticks, tick_params
- **Figure 类**：tight_layout, constrained_layout

---

**版本信息**：Matplotlib 3.10.7 | 可能随版本变化


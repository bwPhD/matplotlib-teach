"""
Marker（标记点）相关参数的完整选项目录
"""
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.lines
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from catalogs.utils import get_matplotlib_version, generate_sample_data, ensure_chinese_font

@st.cache_data
def get_marker_options() -> Dict:
    """获取所有 marker 选项"""
    line = matplotlib.lines.Line2D([0,1], [0,1])
    markers = dict(line.markers)
    
    # 分类整理
    categories = {
        '基本形状': [],
        '三角形': [],
        '多边形': [],
        '特殊符号': [],
        '数字标记': [],
        '空值': []
    }
    
    for key, value in markers.items():
        name = str(value)
        if name in ['point', 'pixel', 'circle']:
            categories['基本形状'].append((key, value))
        elif 'triangle' in name or 'tri_' in name or 'caret' in name:
            categories['三角形'].append((key, value))
        elif name in ['square', 'pentagon', 'hexagon', 'octagon', 'diamond', 'thin_diamond', 'star']:
            categories['多边形'].append((key, value))
        elif name in ['plus', 'x', 'vline', 'hline', 'plus_filled', 'x_filled']:
            categories['特殊符号'].append((key, value))
        elif isinstance(key, int) or (isinstance(key, str) and key.isdigit()):
            categories['数字标记'].append((key, value))
        elif name == 'nothing':
            categories['空值'].append((key, value))
        else:
            categories['特殊符号'].append((key, value))
    
    return {
        'all_markers': markers,
        'categories': categories
    }

@st.cache_data
def get_fillstyle_options() -> Tuple:
    """获取 fillstyle 选项"""
    line = matplotlib.lines.Line2D([0,1], [0,1])
    return line.fillStyles

def render_marker_gallery():
    """渲染 marker 全量画廊"""
    ensure_chinese_font()
    st.title("标记符号 (Marker) 参数百科")
    st.caption(f"Matplotlib {get_matplotlib_version()} | 可能随版本变化")
    
    # 参数说明
    st.markdown("### 📖 参数说明")
    st.info("""
    **作用**：控制数据点的标记符号样式
    
    **适用范围**：`ax.plot()`, `ax.scatter()`, `Line2D` 对象
    
    **默认值**：`None`（无标记）
    
    **支持形式**：
    - 字符串：`'.'`, `'o'`, `'s'`, `'^'`, `'*'` 等
    - 数字：`0`, `1`, `2`, ... `11`（tick/caret 标记）
    - 特殊值：`None`, `'None'`, `' '`, `''`（无标记）
    
    **注意**：某些标记（如 `'o'`, `'s'`）支持 `fillstyle` 参数控制填充样式
    """)
    
    options = get_marker_options()
    x, y = generate_sample_data(10)  # 较少点数便于看清标记
    
    # === 按类别展示 ===
    categories = options['categories']
    
    for category_name, markers_list in categories.items():
        if not markers_list:
            continue
            
        st.markdown(f"### 🎨 {category_name}")
        
        # 计算布局
        n_markers = len(markers_list)
        cols = 4
        rows = (n_markers + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=(3*cols, 2.5*rows))
        if rows == 1:
            axes = axes if isinstance(axes, np.ndarray) else [axes]
        else:
            axes = axes.flatten()
        
        for idx, (key, value) in enumerate(markers_list):
            if idx >= len(axes):
                break
            ax = axes[idx]
            
            # 绘制标记
            marker_str = key if isinstance(key, str) else str(key)
            ax.plot(x, y, marker=key, linestyle='None', markersize=12, 
                   markerfacecolor='#2c3e50', markeredgecolor='#e74c3c', 
                   markeredgewidth=1.5, label=f"'{marker_str}'")
            
            # 设置标题
            title = f"marker='{marker_str}'\n({value})"
            ax.set_title(title, fontsize=9, fontweight='bold')
            ax.set_xlim(-0.5, 9.5)
            ax.set_ylim(-1.5, 1.5)
            ax.grid(True, alpha=0.3)
            ax.axis('on')
        
        # 隐藏多余的子图
        for idx in range(n_markers, len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    # === 合法值表格（部分重要标记）===
    st.markdown("### 📋 常用标记表格")
    table_data = []
    
    important_markers = [
        ('.', 'point', '点，最小标记'),
        (',', 'pixel', '像素，1像素大小'),
        ('o', 'circle', '圆圈，最常用'),
        ('s', 'square', '正方形'),
        ('^', 'triangle_up', '向上三角形'),
        ('v', 'triangle_down', '向下三角形'),
        ('<', 'triangle_left', '向左三角形'),
        ('>', 'triangle_right', '向右三角形'),
        ('*', 'star', '星形'),
        ('+', 'plus', '加号'),
        ('x', 'x', 'X符号'),
        ('D', 'diamond', '菱形'),
        ('d', 'thin_diamond', '细菱形'),
        ('p', 'pentagon', '五边形'),
        ('h', 'hexagon1', '六边形1'),
        ('H', 'hexagon2', '六边形2'),
        ('8', 'octagon', '八边形'),
        ('P', 'plus_filled', '填充加号'),
        ('X', 'x_filled', '填充X'),
        ('|', 'vline', '竖线'),
        ('_', 'hline', '横线'),
    ]
    
    for key, name, desc in important_markers:
        code = f"marker='{key}'"
        table_data.append({
            '参数值': f"'{key}'",
            '名称': name,
            '最小代码': code,
            '说明': desc
        })
    
    # 添加数字标记
    for i in range(12):
        code = f"marker={i}"
        name_map = {
            0: 'tickleft', 1: 'tickright', 2: 'tickup', 3: 'tickdown',
            4: 'caretleft', 5: 'caretright', 6: 'caretup', 7: 'caretdown',
            8: 'caretleftbase', 9: 'caretrightbase', 10: 'caretupbase', 11: 'caretdownbase'
        }
        name = name_map.get(i, f'tick{i}')
        table_data.append({
            '参数值': str(i),
            '名称': name,
            '最小代码': code,
            '说明': f'刻度/箭头标记 {i}'
        })
    
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # === 交互式示例 ===
    st.markdown("### 🎛️ 交互式标记预览")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        marker_choice = st.selectbox(
            "选择标记",
            ['.', ',', 'o', 's', '^', 'v', '<', '>', '*', '+', 'x', 'D', 'd', 'p', 'h', 'H', '8', 'P', 'X', '|', '_', None],
            format_func=lambda x: f"'{x}'" if x is not None else "None",
            key='marker_interactive'
        )
    with col2:
        marker_size = st.slider("标记大小", min_value=5, max_value=30, value=12, key='marker_size')
    with col3:
        marker_color = st.color_picker("标记颜色", "#2c3e50", key='marker_color')
    
    fig_custom, ax_custom = plt.subplots(figsize=(10, 4))
    x_custom, y_custom = generate_sample_data(10)
    
    if marker_choice is not None:
        ax_custom.plot(x_custom, y_custom, marker=marker_choice, linestyle='-', 
                      markersize=marker_size, color=marker_color, linewidth=2,
                      markerfacecolor=marker_color, markeredgecolor='white', 
                      markeredgewidth=1.5, label=f"marker='{marker_choice}'")
    else:
        ax_custom.plot(x_custom, y_custom, linestyle='-', linewidth=2, 
                      color=marker_color, label='No marker')
    
    ax_custom.set_title(f"Interactive Marker Preview", fontsize=11, fontweight='bold')
    ax_custom.grid(True, alpha=0.3)
    ax_custom.legend()
    st.pyplot(fig_custom)
    
    marker_code = f"marker='{marker_choice}'" if marker_choice is not None else "marker=None"
    st.code(f"""
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 10)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y, {marker_code}, markersize={marker_size}, 
        markerfacecolor='{marker_color}', markeredgecolor='white', 
        markeredgewidth=1.5, linewidth=2)
ax.set_title("Marker Example")
ax.grid(True, alpha=0.3)
plt.show()
    """, language='python')
    
    # === 常见坑 ===
    st.markdown("### ⚠️ 常见坑")
    st.warning("""
    1. **大小写敏感**：`'o'`（圆圈）和 `'O'`（无效）不同，注意使用小写
    
    2. **数字 vs 字符串**：`marker=0` 和 `marker='0'` 不同
       - `marker=0` → tickleft（刻度标记）
       - `marker='0'` → 无效（会报错或显示为默认）
    
    3. **空值等价**：`None`, `'None'`, `' '`, `''` 都表示无标记，但推荐使用 `None`
    
    4. **标记大小单位**：`markersize` 的单位是"点"（points），不是像素
       - 默认值通常是 6
       - 1 point ≈ 1/72 英寸
    
    5. **填充样式**：某些标记（如 `'o'`, `'s'`）支持 `fillstyle` 参数
       - `fillstyle='full'`：完全填充（默认）
       - `fillstyle='none'`：仅边框
       - `fillstyle='left'/'right'/'top'/'bottom'`：部分填充
    
    6. **标记边缘**：使用 `markeredgecolor` 和 `markeredgewidth` 控制边框
       - 如果 `markeredgewidth=0`，边框不可见
    
    7. **性能注意**：大量标记点（>1000）可能影响渲染性能
       - 考虑使用 `markevery` 参数减少标记数量
    """)

def render_fillstyle_gallery():
    """渲染 fillstyle 全量画廊"""
    ensure_chinese_font()
    st.title("填充样式 (Fillstyle) 参数百科")
    st.caption(f"Matplotlib {get_matplotlib_version()} | 可能随版本变化")
    
    # 参数说明
    st.markdown("### 📖 参数说明")
    st.info("""
    **作用**：控制标记符号的填充样式（仅对可填充的标记有效）
    
    **适用范围**：`ax.plot()`, `Line2D` 对象（配合 `marker` 使用）
    
    **默认值**：`'full'`（完全填充）
    
    **适用标记**：主要适用于封闭形状的标记，如：
    - `'o'` (circle)
    - `'s'` (square)
    - `'^'`, `'v'`, `'<'`, `'>'` (triangles)
    - `'D'`, `'d'` (diamonds)
    - `'p'` (pentagon)
    - `'h'`, `'H'` (hexagons)
    - `'8'` (octagon)
    - `'*'` (star)
    
    **注意**：对 `'+'`, `'x'`, `'|'`, `'_'` 等非封闭标记无效
    """)
    
    fillstyles = get_fillstyle_options()
    x, y = generate_sample_data(8)  # 较少点数便于看清填充效果
    
    # === 预览画廊 ===
    st.markdown("### 🎨 填充样式预览")
    
    # 使用多个标记类型展示 fillstyle 效果
    test_markers = ['o', 's', '^', 'D', 'p', 'h', '*']
    
    n_fillstyles = len(fillstyles)
    n_markers = len(test_markers)
    
    fig, axes = plt.subplots(n_fillstyles, n_markers, figsize=(2.5*n_markers, 2.5*n_fillstyles))
    if n_fillstyles == 1:
        axes = axes.reshape(1, -1)
    if n_markers == 1:
        axes = axes.reshape(-1, 1)
    
    descriptions = {
        'full': '完全填充（默认）',
        'left': '左半部分填充',
        'right': '右半部分填充',
        'bottom': '下半部分填充',
        'top': '上半部分填充',
        'none': '不填充（仅边框）',
    }
    
    for fs_idx, fs in enumerate(fillstyles):
        for m_idx, marker in enumerate(test_markers):
            ax = axes[fs_idx, m_idx]
            
            # 绘制标记
            ax.plot(x, y, marker=marker, linestyle='None', markersize=15,
                   markerfacecolor='#2c3e50', markeredgecolor='#e74c3c',
                   markeredgewidth=2, fillstyle=fs)
            
            # 设置标题
            if fs_idx == 0:
                ax.set_title(f"marker='{marker}'", fontsize=9, fontweight='bold')
            if m_idx == 0:
                ax.set_ylabel(f"fillstyle='{fs}'\n{descriptions.get(fs, '')}", 
                             fontsize=9, rotation=0, labelpad=30, va='center')
            
            ax.set_xlim(-0.5, 7.5)
            ax.set_ylim(-1.5, 1.5)
            ax.axis('off')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # === 单个标记详细对比 ===
    st.markdown("### 🔍 单个标记详细对比（圆圈 'o'）")
    fig2, axes2 = plt.subplots(1, n_fillstyles, figsize=(3*n_fillstyles, 3))
    if n_fillstyles == 1:
        axes2 = [axes2]
    
    for idx, fs in enumerate(fillstyles):
        ax = axes2[idx]
        ax.plot(x[:5], y[:5], marker='o', linestyle='None', markersize=20,
               markerfacecolor='#3498db', markeredgecolor='#2c3e50',
               markeredgewidth=2.5, fillstyle=fs)
        ax.set_title(f"fillstyle='{fs}'\n{descriptions.get(fs, '')}", fontsize=10)
        ax.set_xlim(-0.5, 4.5)
        ax.set_ylim(-1.5, 1.5)
        ax.grid(True, alpha=0.3)
        ax.axis('on')
    
    plt.tight_layout()
    st.pyplot(fig2)
    
    # === 合法值表格 ===
    st.markdown("### 📋 合法值表格")
    table_data = []
    for fs in fillstyles:
        code = f"fillstyle='{fs}'"
        desc = descriptions.get(fs, '')
        table_data.append({
            '参数值': f"'{fs}'",
            '最小代码': code,
            '说明': desc
        })
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # === 交互式示例 ===
    st.markdown("### 🎛️ 交互式填充样式预览")
    col1, col2 = st.columns(2)
    
    with col1:
        marker_choice = st.selectbox(
            "选择标记",
            ['o', 's', '^', 'v', '<', '>', 'D', 'd', 'p', 'h', 'H', '8', '*'],
            key='fillstyle_marker'
        )
    with col2:
        fillstyle_choice = st.selectbox(
            "选择填充样式",
            fillstyles,
            key='fillstyle_choice'
        )
    
    fig_custom, ax_custom = plt.subplots(figsize=(10, 4))
    x_custom, y_custom = generate_sample_data(8)
    
    ax_custom.plot(x_custom, y_custom, marker=marker_choice, linestyle='-', 
                  markersize=15, markerfacecolor='#3498db', 
                  markeredgecolor='#2c3e50', markeredgewidth=2.5,
                  fillstyle=fillstyle_choice, linewidth=2, label=f"fillstyle='{fillstyle_choice}'")
    
    ax_custom.set_title(f"Marker '{marker_choice}' with fillstyle='{fillstyle_choice}'", 
                       fontsize=11, fontweight='bold')
    ax_custom.grid(True, alpha=0.3)
    ax_custom.legend()
    st.pyplot(fig_custom)
    
    st.code(f"""
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 8)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y, marker='{marker_choice}', fillstyle='{fillstyle_choice}',
        markersize=15, markerfacecolor='#3498db', 
        markeredgecolor='#2c3e50', markeredgewidth=2.5, linewidth=2)
ax.set_title("Fillstyle Example")
ax.grid(True, alpha=0.3)
plt.show()
    """, language='python')
    
    # === 常见坑 ===
    st.markdown("### ⚠️ 常见坑")
    st.warning("""
    1. **仅对封闭标记有效**：`fillstyle` 只对可填充的标记有效
       - ✅ 有效：`'o'`, `'s'`, `'^'`, `'D'`, `'p'`, `'h'`, `'*'` 等
       - ❌ 无效：`'+'`, `'x'`, `'|'`, `'_'`（这些标记本身就是线条）
    
    2. **部分填充方向**：
       - `'left'` / `'right'`：相对于标记的左右（不是坐标轴的左右）
       - `'top'` / `'bottom'`：相对于标记的上下（不是坐标轴的上下）
       - 对于旋转的标记（如 `'<'`, `'>'`），方向可能不符合预期
    
    3. **边框颜色**：`fillstyle='none'` 时，标记仅显示边框
       - 需要设置 `markeredgecolor` 和 `markeredgewidth` 才能看到标记
    
    4. **与 markerfacecolor 配合**：
       - `markerfacecolor` 控制填充颜色
       - `markeredgecolor` 控制边框颜色
       - `fillstyle` 控制填充区域
    
    5. **性能注意**：部分填充的计算可能略慢于完全填充，但差异很小
    """)

def render_catalog_page(param_name: str):
    """根据参数名渲染对应的目录页面"""
    if param_name == 'marker':
        render_marker_gallery()
    elif param_name == 'fillstyle':
        render_fillstyle_gallery()
    else:
        st.error(f"参数 '{param_name}' 的目录页面尚未实现")


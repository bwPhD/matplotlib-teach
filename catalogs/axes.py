"""
Axes（坐标轴）相关参数的完整选项目录
"""
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from catalogs.utils import get_matplotlib_version, generate_sample_data, ensure_chinese_font

def render_xlim_ylim_gallery():
    """渲染 xlim/ylim 全量画廊"""
    ensure_chinese_font()
    st.title("坐标范围 (xlim/ylim) 参数百科")
    st.caption(f"Matplotlib {get_matplotlib_version()} | 可能随版本变化")
    
    st.markdown("### 📖 参数说明")
    st.info("""
    **作用**：设置坐标轴的范围（最小值和最大值）
    
    **适用范围**：`ax.set_xlim()`, `ax.set_ylim()`, `ax.set_xlim()`, `plt.xlim()`, `plt.ylim()`
    
    **支持形式**：
    - **元组**：`(min, max)` 如 `(0, 10)`
    - **列表**：`[min, max]` 如 `[0, 10]`
    - **单独设置**：`ax.set_xlim(left=0, right=10)`
    
    **默认值**：自动根据数据范围调整
    """)
    
    x, y = generate_sample_data(50)
    
    # === 不同范围对比 ===
    st.markdown("### 🎨 不同范围设置预览")
    
    ranges = [
        ("自动范围", None, None),
        ("自定义范围", (0, 8), (-1, 1)),
        ("仅设置 X", (2, 8), None),
        ("仅设置 Y", None, (-0.5, 0.5)),
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()
    
    for idx, (title, xlim_val, ylim_val) in enumerate(ranges):
        ax = axes[idx]
        ax.plot(x, y, linewidth=2, color='#2c3e50')
        if xlim_val:
            ax.set_xlim(xlim_val)
        if ylim_val:
            ax.set_ylim(ylim_val)
        ax.set_title(f"{title}\nxlim={xlim_val}, ylim={ylim_val}", fontsize=10, fontweight='bold')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # === 交互式预览 ===
    st.markdown("### 🎛️ 交互式范围设置")
    col1, col2 = st.columns(2)
    
    with col1:
        x_min = st.number_input("X 最小值", value=0.0, key='xlim_min')
        x_max = st.number_input("X 最大值", value=10.0, key='xlim_max')
    with col2:
        y_min = st.number_input("Y 最小值", value=-1.5, key='ylim_min')
        y_max = st.number_input("Y 最大值", value=1.5, key='ylim_max')
    
    fig_custom, ax_custom = plt.subplots(figsize=(10, 4))
    ax_custom.plot(x, y, linewidth=2, color='#2c3e50')
    ax_custom.set_xlim(x_min, x_max)
    ax_custom.set_ylim(y_min, y_max)
    ax_custom.set_title(f"xlim=({x_min}, {x_max}), ylim=({y_min}, {y_max})", fontsize=11, fontweight='bold')
    ax_custom.grid(True, alpha=0.3)
    st.pyplot(fig_custom)
    
    st.code(f"""
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 50)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y, linewidth=2)
ax.set_xlim({x_min}, {x_max})
ax.set_ylim({y_min}, {y_max})
ax.grid(True, alpha=0.3)
plt.show()
    """, language='python')
    
    st.markdown("### ⚠️ 常见坑")
    st.warning("""
    1. **元组顺序**：`(min, max)` 顺序不能颠倒，min 必须小于 max
    
    2. **数据裁剪**：设置范围不会裁剪数据，只是改变显示范围
    
    3. **自动调整**：如果不设置，Matplotlib 会自动根据数据范围调整
    """)

def render_grid_gallery():
    """渲染 grid 全量画廊"""
    ensure_chinese_font()
    st.title("网格 (Grid) 参数百科")
    st.caption(f"Matplotlib {get_matplotlib_version()} | 可能随版本变化")
    
    st.markdown("### 📖 参数说明")
    st.info("""
    **作用**：控制坐标轴网格的显示
    
    **适用范围**：`ax.grid()`, `ax.set_xgrid()`, `ax.set_ygrid()`
    
    **支持形式**：
    - **布尔值**：`True` / `False`
    - **字典**：`{'alpha': 0.5, 'linestyle': '--', 'color': 'gray'}`
    - **关键字参数**：`ax.grid(True, alpha=0.5, linestyle='--')`
    
    **默认值**：`False`（不显示网格）
    """)
    
    x, y = generate_sample_data(50)
    
    # === 不同 grid 设置 ===
    st.markdown("### 🎨 不同 Grid 设置预览")
    
    grid_configs = [
        ("无网格", False, {}),
        ("默认网格", True, {}),
        ("虚线网格", True, {'linestyle': '--'}),
        ("半透明网格", True, {'alpha': 0.3}),
        ("彩色网格", True, {'color': 'red', 'alpha': 0.5}),
        ("仅 X 轴网格", True, {'axis': 'x'}),
        ("仅 Y 轴网格", True, {'axis': 'y'}),
    ]
    
    n_configs = len(grid_configs)
    cols = 2
    rows = (n_configs + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(6*cols, 3*rows))
    if rows == 1:
        axes = axes if isinstance(axes, np.ndarray) else [axes]
    else:
        axes = axes.flatten()
    
    for idx, (title, grid_val, grid_kwargs) in enumerate(grid_configs):
        if idx >= len(axes):
            break
        ax = axes[idx]
        ax.plot(x, y, linewidth=2, color='#2c3e50')
        ax.grid(grid_val, **grid_kwargs)
        ax.set_title(title, fontsize=10, fontweight='bold')
    
    for idx in range(n_configs, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.markdown("### ⚠️ 常见坑")
    st.warning("""
    1. **全局设置**：可以通过 `plt.rcParams['axes.grid']` 设置全局默认网格
    
    2. **网格样式**：可以单独设置 X 轴或 Y 轴的网格样式
    
    3. **透明度**：使用 `alpha` 参数控制网格透明度，避免遮挡数据
    """)

def render_spines_gallery():
    """渲染 spines 全量画廊"""
    ensure_chinese_font()
    st.title("边框 (Spines) 参数百科")
    st.caption(f"Matplotlib {get_matplotlib_version()} | 可能随版本变化")
    
    st.markdown("### 📖 参数说明")
    st.info("""
    **作用**：控制坐标轴边框（spines）的显示和样式
    
    **适用范围**：`ax.spines['top'].set_visible()`, `ax.spines['bottom'].set_color()` 等
    
    **边框位置**：`'top'`, `'bottom'`, `'left'`, `'right'`
    
    **常用操作**：
    - 隐藏边框：`ax.spines['top'].set_visible(False)`
    - 设置颜色：`ax.spines['bottom'].set_color('red')`
    - 设置位置：`ax.spines['left'].set_position(('outward', 10))`
    """)
    
    x, y = generate_sample_data(50)
    
    # === 不同 spines 设置 ===
    st.markdown("### 🎨 不同 Spines 设置预览")
    
    spine_configs = [
        ("默认（四边都有）", {}),
        ("隐藏上边框", {'top': False}),
        ("隐藏右边框", {'right': False}),
        ("隐藏上下边框", {'top': False, 'bottom': False}),
        ("仅显示下和左", {'top': False, 'right': False}),
        ("彩色边框", {'color': {'bottom': 'red', 'left': 'blue'}}),
    ]
    
    n_configs = len(spine_configs)
    cols = 2
    rows = (n_configs + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(6*cols, 3*rows))
    if rows == 1:
        axes = axes if isinstance(axes, np.ndarray) else [axes]
    else:
        axes = axes.flatten()
    
    for idx, (title, config) in enumerate(spine_configs):
        if idx >= len(axes):
            break
        ax = axes[idx]
        ax.plot(x, y, linewidth=2, color='#2c3e50')
        
        if 'top' in config and config['top'] == False:
            ax.spines['top'].set_visible(False)
        if 'bottom' in config and config['bottom'] == False:
            ax.spines['bottom'].set_visible(False)
        if 'left' in config and config['left'] == False:
            ax.spines['left'].set_visible(False)
        if 'right' in config and config['right'] == False:
            ax.spines['right'].set_visible(False)
        
        if 'color' in config:
            for spine_name, color_val in config['color'].items():
                ax.spines[spine_name].set_color(color_val)
        
        ax.set_title(title, fontsize=10, fontweight='bold')
        ax.grid(True, alpha=0.3)
    
    for idx in range(n_configs, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.code("""
# 隐藏上边框和右边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 设置边框颜色
ax.spines['bottom'].set_color('red')
ax.spines['left'].set_color('blue')
    """, language='python')
    
    st.markdown("### ⚠️ 常见坑")
    st.warning("""
    1. **边框位置**：spines 有四个位置：top, bottom, left, right
    
    2. **隐藏 vs 删除**：`set_visible(False)` 隐藏边框，不会删除
    
    3. **常用组合**：科学图表常用 `ax.spines['top'].set_visible(False)` 和 `ax.spines['right'].set_visible(False)`
    """)

def render_catalog_page(param_name: str):
    """根据参数名渲染对应的目录页面"""
    if param_name == 'xlim' or param_name == 'ylim':
        render_xlim_ylim_gallery()
    elif param_name == 'grid':
        render_grid_gallery()
    elif param_name == 'spines':
        render_spines_gallery()
    else:
        st.error(f"参数 '{param_name}' 的目录页面尚未实现")


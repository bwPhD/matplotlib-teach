"""
Color（颜色）相关参数的完整选项目录
"""
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from catalogs.utils import get_matplotlib_version, generate_sample_data, ensure_chinese_font

@st.cache_data
def get_color_options() -> Dict:
    """获取所有 color 选项"""
    # CSS4 颜色（148个）
    css4_colors = dict(mcolors.CSS4_COLORS)
    
    # Base 颜色（8个）
    base_colors = dict(mcolors.BASE_COLORS)
    
    # Tab10 颜色（10个）- 从 colormap 获取
    try:
        # 直接从 colormap 生成 tab10 颜色
        cmap = plt.get_cmap('tab10')
        tab10_colors = {f'tab10_{i}': mcolors.to_hex(cmap(i)) for i in range(10)}
    except Exception:
        # 如果失败，使用空字典
        tab10_colors = {}
    
    # CN 颜色（C0-C9）
    cn_colors = {f'C{i}': f'CN颜色{i}' for i in range(10)}
    
    return {
        'css4_colors': css4_colors,
        'base_colors': base_colors,
        'tab10_colors': tab10_colors,
        'cn_colors': cn_colors,
    }

@st.cache_data
def get_colormap_options() -> Dict:
    """获取所有 colormap 选项并分类"""
    cmaps = sorted(plt.colormaps())
    
    # 分类
    categories = {
        'Perceptually Uniform Sequential': [],
        'Sequential': [],
        'Sequential (2)': [],
        'Diverging': [],
        'Cyclic': [],
        'Qualitative': [],
        'Miscellaneous': [],
    }
    
    # 根据名称分类（简化分类）
    for cmap in cmaps:
        cmap_lower = cmap.lower()
        if 'perceptually' in cmap_lower or cmap in ['viridis', 'plasma', 'inferno', 'magma', 'cividis']:
            categories['Perceptually Uniform Sequential'].append(cmap)
        elif 'diverging' in cmap_lower or cmap in ['RdBu', 'RdYlBu', 'Spectral', 'coolwarm']:
            categories['Diverging'].append(cmap)
        elif 'qualitative' in cmap_lower or cmap.startswith('tab') or cmap.startswith('Set'):
            categories['Qualitative'].append(cmap)
        elif 'cyclic' in cmap_lower or cmap in ['hsv', 'twilight', 'twilight_shifted']:
            categories['Cyclic'].append(cmap)
        elif cmap.endswith('_r'):
            # 反向 colormap，归入原类别
            base = cmap[:-2]
            if base in categories['Sequential']:
                categories['Sequential'].append(cmap)
            else:
                categories['Miscellaneous'].append(cmap)
        else:
            categories['Sequential'].append(cmap)
    
    return {
        'all_cmaps': cmaps,
        'categories': categories
    }

def render_color_gallery():
    """渲染 color 全量画廊"""
    ensure_chinese_font()
    st.title("颜色 (Color) 参数百科")
    st.caption(f"Matplotlib {get_matplotlib_version()} | 可能随版本变化")
    
    # 参数说明
    st.markdown("### 📖 参数说明")
    st.info("""
    **作用**：控制图形元素的颜色
    
    **适用范围**：几乎所有 Matplotlib 绘图函数（`ax.plot()`, `ax.scatter()`, `ax.bar()` 等）
    
    **支持形式**：
    - **颜色名称**：`'red'`, `'blue'`, `'green'` 等（CSS4 颜色，148个）
    - **单字符**：`'r'`, `'g'`, `'b'`, `'c'`, `'m'`, `'y'`, `'k'`, `'w'`（Base 颜色，8个）
    - **CN 颜色**：`'C0'`, `'C1'`, ... `'C9'`（循环使用，10个）
    - **HEX**：`'#FF5733'`, `'#RRGGBB'` 或 `'#RRGGBBAA'`
    - **RGB/RGBA**：`(0.1, 0.2, 0.5)` 或 `(0.1, 0.2, 0.5, 0.8)`（值范围 0-1）
    - **灰度**：`'0.5'`（字符串，0-1之间的浮点数）
    
    **默认值**：`'C0'`（第一个 CN 颜色，通常是蓝色）
    """)
    
    options = get_color_options()
    x, y = generate_sample_data(50)
    
    # === Base 颜色预览 ===
    st.markdown("### 🎨 Base 颜色（单字符，8个）")
    base_colors = options['base_colors']
    
    fig1, axes1 = plt.subplots(1, len(base_colors), figsize=(2*len(base_colors), 2))
    for idx, (key, rgb) in enumerate(base_colors.items()):
        ax = axes1[idx]
        ax.plot(x, y, color=key, linewidth=3, label=f"'{key}'")
        ax.fill_between(x, y, alpha=0.3, color=key)
        ax.set_title(f"'{key}'\n{rgb}", fontsize=9, fontweight='bold')
        ax.set_xlim(0, 10)
        ax.set_ylim(-1.5, 1.5)
        ax.axis('off')
    
    plt.tight_layout()
    st.pyplot(fig1)
    
    # === CN 颜色预览 ===
    st.markdown("### 🎨 CN 颜色（C0-C9，10个）")
    cn_colors = options['cn_colors']
    
    fig2, axes2 = plt.subplots(2, 5, figsize=(12, 4))
    axes2 = axes2.flatten()
    
    for idx, (key, desc) in enumerate(cn_colors.items()):
        ax = axes2[idx]
        ax.plot(x, y, color=key, linewidth=3, label=f"'{key}'")
        ax.fill_between(x, y, alpha=0.3, color=key)
        ax.set_title(f"'{key}'", fontsize=10, fontweight='bold')
        ax.set_xlim(0, 10)
        ax.set_ylim(-1.5, 1.5)
        ax.axis('off')
    
    plt.tight_layout()
    st.pyplot(fig2)
    
    # === CSS4 颜色预览（部分）===
    st.markdown("### 🎨 CSS4 颜色（部分常用，共148个）")
    css4_colors = options['css4_colors']
    
    # 选择常用颜色
    common_colors = [
        'red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray',
        'black', 'white', 'yellow', 'cyan', 'magenta', 'lime', 'navy', 'maroon',
        'olive', 'teal', 'aqua', 'silver', 'gold', 'coral', 'salmon', 'khaki'
    ]
    
    n_common = len(common_colors)
    cols = 4
    rows = (n_common + cols - 1) // cols
    
    fig3, axes3 = plt.subplots(rows, cols, figsize=(3*cols, 2*rows))
    if rows == 1:
        axes3 = axes3 if isinstance(axes3, np.ndarray) else [axes3]
    else:
        axes3 = axes3.flatten()
    
    for idx, color_name in enumerate(common_colors):
        if idx >= len(axes3):
            break
        if color_name in css4_colors:
            ax = axes3[idx]
            ax.plot(x, y, color=color_name, linewidth=3)
            ax.fill_between(x, y, alpha=0.3, color=color_name)
            ax.set_title(f"'{color_name}'", fontsize=9, fontweight='bold')
            ax.set_xlim(0, 10)
            ax.set_ylim(-1.5, 1.5)
            ax.axis('off')
    
    for idx in range(n_common, len(axes3)):
        axes3[idx].axis('off')
    
    plt.tight_layout()
    st.pyplot(fig3)
    
    # === 颜色形式对比 ===
    st.markdown("### 🔍 不同颜色形式对比")
    fig4, ax4 = plt.subplots(figsize=(10, 3))
    
    color_examples = [
        ("颜色名称", "'red'", 'red'),
        ("单字符", "'r'", 'r'),
        ("CN颜色", "'C0'", 'C0'),
        ("HEX", "'#FF5733'", '#FF5733'),
        ("RGB", "(1.0, 0.34, 0.2)", (1.0, 0.34, 0.2)),
        ("RGBA", "(1.0, 0.34, 0.2, 0.8)", (1.0, 0.34, 0.2, 0.8)),
        ("灰度", "'0.5'", '0.5'),
    ]
    
    x_ex = np.linspace(0, 10, 50)
    y_ex = np.sin(x_ex)
    
    for idx, (form, code, color_val) in enumerate(color_examples):
        offset = idx * 1.5
        ax4.plot(x_ex + offset, y_ex, color=color_val, linewidth=2.5, label=code)
        ax4.text(offset + 5, 1.2, form, ha='center', fontsize=8)
    
    ax4.set_xlim(-1, 12)
    ax4.set_ylim(-1.5, 1.8)
    ax4.legend(loc='upper right', fontsize=8, ncol=2)
    ax4.set_title("Color Format Examples", fontsize=11, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    st.pyplot(fig4)
    
    # === 合法值表格 ===
    st.markdown("### 📋 颜色形式表格")
    table_data = []
    for form, code, _ in color_examples:
        table_data.append({
            '形式': form,
            '示例代码': code,
            '说明': {
                '颜色名称': 'CSS4标准颜色名称，如 red, blue',
                '单字符': 'Base颜色，r/g/b/c/m/y/k/w',
                'CN颜色': 'C0-C9，自动循环使用',
                'HEX': '十六进制，如 #FF5733',
                'RGB': '元组 (r,g,b)，值范围 0-1',
                'RGBA': '元组 (r,g,b,a)，值范围 0-1',
                '灰度': '字符串形式的浮点数，0-1',
            }.get(form, '')
        })
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # === 交互式颜色选择 ===
    st.markdown("### 🎛️ 交互式颜色预览")
    col1, col2 = st.columns(2)
    
    with col1:
        color_type = st.selectbox(
            "颜色形式",
            ["颜色名称", "单字符", "CN颜色", "HEX", "RGB"],
            key='color_type'
        )
    
    with col2:
        if color_type == "颜色名称":
            color_value = st.selectbox("选择颜色", list(common_colors), key='color_name')
        elif color_type == "单字符":
            color_value = st.selectbox("选择颜色", list(base_colors.keys()), key='color_char')
        elif color_type == "CN颜色":
            color_value = st.selectbox("选择颜色", list(cn_colors.keys()), key='color_cn')
        elif color_type == "HEX":
            color_value = st.color_picker("选择颜色", "#FF5733", key='color_hex')
        else:  # RGB
            col_r, col_g, col_b = st.columns(3)
            with col_r:
                r = st.slider("R", 0.0, 1.0, 1.0, key='rgb_r')
            with col_g:
                g = st.slider("G", 0.0, 1.0, 0.34, key='rgb_g')
            with col_b:
                b = st.slider("B", 0.0, 1.0, 0.2, key='rgb_b')
            color_value = (r, g, b)
    
    fig_custom, ax_custom = plt.subplots(figsize=(10, 4))
    x_custom, y_custom = generate_sample_data(50)
    ax_custom.plot(x_custom, y_custom, color=color_value, linewidth=3, label=f"color={color_value}")
    ax_custom.fill_between(x_custom, y_custom, alpha=0.3, color=color_value)
    ax_custom.set_title(f"Color Preview: {color_value}", fontsize=11, fontweight='bold')
    ax_custom.grid(True, alpha=0.3)
    ax_custom.legend()
    st.pyplot(fig_custom)
    
    color_code = f"'{color_value}'" if isinstance(color_value, str) else str(color_value)
    st.code(f"""
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 50)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y, color={color_code}, linewidth=3)
ax.fill_between(x, y, alpha=0.3, color={color_code})
ax.set_title("Color Example")
ax.grid(True, alpha=0.3)
plt.show()
    """, language='python')
    
    # === 常见坑 ===
    st.markdown("### ⚠️ 常见坑")
    st.warning("""
    1. **RGB 值范围**：RGB/RGBA 元组的值必须在 0-1 之间，不是 0-255
       - ❌ 错误：`color=(255, 0, 0)` → ✅ 正确：`color=(1.0, 0.0, 0.0)` 或 `color='red'`
    
    2. **灰度字符串**：灰度值必须是字符串，不是浮点数
       - ❌ 错误：`color=0.5` → ✅ 正确：`color='0.5'`
    
    3. **CN 颜色循环**：`'C0'` 到 `'C9'` 会自动循环，`'C10'` 等同于 `'C0'`
    
    4. **颜色名称大小写**：颜色名称不区分大小写，`'Red'` 和 `'red'` 相同
    
    5. **HEX 格式**：HEX 颜色可以是 `#RRGGBB` 或 `#RRGGBBAA`（带透明度）
    
    6. **无效颜色**：如果颜色名称不存在，Matplotlib 会抛出异常或使用默认颜色
    """)

def render_colormap_gallery():
    """渲染 cmap 全量画廊"""
    ensure_chinese_font()
    st.title("颜色映射 (Colormap) 参数百科")
    st.caption(f"Matplotlib {get_matplotlib_version()} | 可能随版本变化")
    
    # 参数说明
    st.markdown("### 📖 参数说明")
    st.info("""
    **作用**：将数值映射到颜色的颜色映射表
    
    **适用范围**：`ax.scatter()`, `ax.imshow()`, `ax.contourf()`, `ax.pcolormesh()` 等需要颜色映射的函数
    
    **默认值**：`'viridis'`（感知均匀的连续颜色映射）
    
    **分类**：
    - **Perceptually Uniform Sequential**：感知均匀的连续映射（推荐用于科学可视化）
    - **Sequential**：连续映射（适用于有序数据）
    - **Diverging**：发散映射（适用于有中心值的数据）
    - **Cyclic**：循环映射（适用于周期性数据）
    - **Qualitative**：定性映射（适用于分类数据）
    
    **注意**：所有 colormap 都可以添加 `'_r'` 后缀来反转（如 `'viridis_r'`）
    """)
    
    options = get_colormap_options()
    cmaps = options['all_cmaps']
    categories = options['categories']
    
    # === 常用 Colormap 预览 ===
    st.markdown("### 🎨 常用 Colormap 预览")
    
    popular_cmaps = [
        'viridis', 'plasma', 'inferno', 'magma', 'cividis',  # Perceptually uniform
        'coolwarm', 'RdBu', 'Spectral',  # Diverging
        'tab10', 'Set1', 'Set2',  # Qualitative
        'hsv', 'twilight',  # Cyclic
    ]
    
    n_popular = len(popular_cmaps)
    cols = 3
    rows = (n_popular + cols - 1) // cols
    
    fig1, axes1 = plt.subplots(rows, cols, figsize=(4*cols, 2*rows))
    if rows == 1:
        axes1 = axes1 if isinstance(axes1, np.ndarray) else [axes1]
    else:
        axes1 = axes1.flatten()
    
    # 生成测试数据
    data = np.random.rand(10, 10)
    
    for idx, cmap_name in enumerate(popular_cmaps):
        if idx >= len(axes1):
            break
        if cmap_name in cmaps:
            ax = axes1[idx]
            im = ax.imshow(data, cmap=cmap_name, aspect='auto')
            ax.set_title(f"'{cmap_name}'", fontsize=10, fontweight='bold')
            ax.axis('off')
            plt.colorbar(im, ax=ax, fraction=0.046)
    
    for idx in range(n_popular, len(axes1)):
        axes1[idx].axis('off')
    
    plt.tight_layout()
    st.pyplot(fig1)
    
    # === 按类别展示 ===
    st.markdown("### 📊 按类别展示 Colormap")
    
    category_tabs = st.tabs(list(categories.keys()))
    
    for tab_idx, (category_name, cmap_list) in enumerate(categories.items()):
        if not cmap_list:
            with category_tabs[tab_idx]:
                st.info(f"该类别暂无 colormap")
            continue
        
        with category_tabs[tab_idx]:
            st.markdown(f"**{category_name}** ({len(cmap_list)} 个)")
            
            # 限制显示数量，避免页面过长
            display_cmaps = cmap_list[:30]  # 每类最多显示30个
            
            n_display = len(display_cmaps)
            cols_cat = 4
            rows_cat = (n_display + cols_cat - 1) // cols_cat
            
            fig_cat, axes_cat = plt.subplots(rows_cat, cols_cat, figsize=(2.5*cols_cat, 1.5*rows_cat))
            if rows_cat == 1:
                axes_cat = axes_cat if isinstance(axes_cat, np.ndarray) else [axes_cat]
            else:
                axes_cat = axes_cat.flatten()
            
            gradient = np.linspace(0, 1, 100).reshape(1, -1)
            
            for idx, cmap_name in enumerate(display_cmaps):
                if idx >= len(axes_cat):
                    break
                ax = axes_cat[idx]
                ax.imshow(gradient, cmap=cmap_name, aspect='auto')
                ax.set_title(f"'{cmap_name}'", fontsize=8)
                ax.set_xticks([])
                ax.set_yticks([])
            
            for idx in range(n_display, len(axes_cat)):
                axes_cat[idx].axis('off')
            
            plt.tight_layout()
            st.pyplot(fig_cat)
            
            if len(cmap_list) > 30:
                st.caption(f"*仅显示前 30 个，共 {len(cmap_list)} 个 colormap*")
    
    # === 交互式 Colormap 预览 ===
    st.markdown("### 🎛️ 交互式 Colormap 预览")
    
    col1, col2 = st.columns(2)
    with col1:
        cmap_choice = st.selectbox("选择 Colormap", cmaps, index=cmaps.index('viridis') if 'viridis' in cmaps else 0, key='cmap_choice')
    
    with col2:
        data_type = st.selectbox("数据类型", ["2D 图像", "散点图", "等高线"], key='cmap_data_type')
    
    fig_custom, ax_custom = plt.subplots(figsize=(10, 6))
    
    if data_type == "2D 图像":
        data_2d = np.random.rand(20, 20)
        im = ax_custom.imshow(data_2d, cmap=cmap_choice, aspect='auto')
        plt.colorbar(im, ax=ax_custom)
        ax_custom.set_title(f"imshow with cmap='{cmap_choice}'", fontsize=11, fontweight='bold')
    elif data_type == "散点图":
        x_scatter = np.random.rand(100)
        y_scatter = np.random.rand(100)
        c_scatter = np.random.rand(100)
        sc = ax_custom.scatter(x_scatter, y_scatter, c=c_scatter, cmap=cmap_choice, s=50)
        plt.colorbar(sc, ax=ax_custom)
        ax_custom.set_title(f"scatter with cmap='{cmap_choice}'", fontsize=11, fontweight='bold')
    else:  # 等高线
        x_contour = np.linspace(-3, 3, 100)
        y_contour = np.linspace(-3, 3, 100)
        X, Y = np.meshgrid(x_contour, y_contour)
        Z = np.exp(-(X**2 + Y**2))
        cf = ax_custom.contourf(X, Y, Z, levels=20, cmap=cmap_choice)
        plt.colorbar(cf, ax=ax_custom)
        ax_custom.set_title(f"contourf with cmap='{cmap_choice}'", fontsize=11, fontweight='bold')
    
    st.pyplot(fig_custom)
    
    st.code(f"""
import matplotlib.pyplot as plt
import numpy as np

# 生成数据
data = np.random.rand(20, 20)

fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(data, cmap='{cmap_choice}')
plt.colorbar(im, ax=ax)
ax.set_title("Colormap Example")
plt.show()
    """, language='python')
    
    # === 常见坑 ===
    st.markdown("### ⚠️ 常见坑")
    st.warning("""
    1. **反转 Colormap**：添加 `'_r'` 后缀可以反转 colormap
       - `'viridis'` → `'viridis_r'`
       - 适用于需要反向映射的场景
    
    2. **选择合适的 Colormap**：
       - **连续数据**：使用 Sequential colormap（如 `'viridis'`, `'plasma'`）
       - **有中心值的数据**：使用 Diverging colormap（如 `'coolwarm'`, `'RdBu'`）
       - **分类数据**：使用 Qualitative colormap（如 `'tab10'`, `'Set1'`）
       - **周期性数据**：使用 Cyclic colormap（如 `'hsv'`, `'twilight'`）
    
    3. **感知均匀性**：`'viridis'`, `'plasma'`, `'inferno'`, `'magma'` 是感知均匀的，适合科学可视化
    
    4. **颜色盲友好**：避免使用 `'jet'`（虽然常见但不推荐），推荐使用 `'viridis'` 等
    
    5. **Colorbar**：使用 `plt.colorbar()` 或 `fig.colorbar()` 显示颜色映射条
    
    6. **数据归一化**：colormap 会自动将数据归一化到 0-1 范围，也可以使用 `norm` 参数自定义
    """)

def render_catalog_page(param_name: str):
    """根据参数名渲染对应的目录页面"""
    if param_name == 'color':
        render_color_gallery()
    elif param_name == 'cmap':
        render_colormap_gallery()
    else:
        st.error(f"参数 '{param_name}' 的目录页面尚未实现")


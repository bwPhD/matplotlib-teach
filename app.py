import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.ticker as ticker
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import altair as alt
from mpl_toolkits.mplot3d import Axes3D

# --- 页面配置 ---
st.set_page_config(page_title="计算社会学可视化教学", layout="wide", page_icon="🎨")

# --- CSSHack: 强制调整代码块字体大小为 12pt (约16px) ---
st.markdown("""
<style>
    /* 调整 streamlit 代码块的字体大小 */
    code {
        font-size: 16px !important;
        font-family: 'Consolas', 'Courier New', monospace !important;
    }
    /* 优化侧边栏显示 */
    section[data-testid="stSidebar"] .stMarkdown h1 {
        font-size: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 侧边栏导航 ---
st.sidebar.title("计算社会学可视化教学")
st.sidebar.info("Code & Visuals Interactive Learning")

menu = st.sidebar.radio(
    "课程章节",
    [
        "1. 生态全景 (The Landscape)",
        "2. Matplotlib 核心解构 (The Core)",
        "3. 基础笔触 (The Brushes)",
        "4. 布局与美学 (Layout & Style)",
        "5. 进阶画廊 (Advanced Gallery)",
        "6. 其他库实战 (Modern Libs)",
        "7. 进阶挑战：大师之路 (Master Class) 🚀"
    ]
)

# --- 辅助函数：生成数据 ---
@st.cache_data
def get_random_data(points=100):
    return pd.DataFrame({
        'x': np.random.randn(points),
        'y': np.random.randn(points),
        'category': np.random.choice(['A', 'B', 'C'], points),
        'value': np.random.rand(points) * 100
    })

# --- 章节 1: 生态全景 ---
if menu == "1. 生态全景 (The Landscape)":
    st.title("Python 数据可视化生态全景")
    st.markdown("### “到底该用哪个库？”—— 从小白到专家的第一步")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🛠️ Matplotlib: 基石与控制")
        st.info("**核心特征：Control (控制)**\n\nPython可视化的底层引擎。只要你肯花时间，几乎可以实现任何效果。适合出版级绘图。")
        
        st.subheader("💅 Seaborn: 统计之美")
        st.success("**核心特征：Beauty (美观)**\n\n基于Matplotlib的高级封装。适合快速探索性数据分析(EDA)，默认样式优雅。")

    with col2:
        st.subheader("🖱️ Plotly: 交互为王")
        st.warning("**核心特征：Interaction (交互)**\n\n独立的库，专为Web设计。支持悬停、缩放。适合仪表盘和网页报告。")
        
        st.subheader("📜 Altair: 声明式语法")
        st.error("**核心特征：Grammar (语法)**\n\n描述“通过什么数据映射到什么视觉元素”。代码极简，适合快速构建图表逻辑。")

    st.markdown("---")
    st.image(caption="我们将重点攻克 Matplotlib，它是所有可视化的基础。")

# --- 章节 2: Matplotlib 核心解构 ---
elif menu == "2. Matplotlib 核心解构 (The Core)":
    st.title("Matplotlib 从零到精通")
    
    st.markdown("### 1. 两种创作风格：Pyplot vs 面向对象 (OO)")
    st.write("课件中强调：**坚持使用面向对象（OO）模式**，实现对图表的完全掌控。")
    
    col_demo, col_code = st.columns([1, 1])
    
    style_choice = st.radio("选择代码风格进行对比：", ["Pyplot (快捷模式)", "OO (面向对象模式 - 推荐)"], horizontal=True)
    
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    # 预先定义代码字符串，方便展示
    code_pyplot = """
plt.figure(figsize=(6, 4))
plt.plot(x, y, label='Sine Wave', color='blue')
plt.title("Pyplot Style")
plt.xlabel("X Axis")
plt.ylabel("Y Axis")
plt.legend()
plt.grid(True)
"""
    code_oo = """
# 1. 创建 Figure 和 Axes (画布与坐标系)
fig, ax = plt.subplots(figsize=(6, 4))

# 2. 在 ax 对象上调用方法 (set_title, set_xlabel...)
ax.plot(x, y, label='Sine Wave', color='green')
ax.set_title("OO Style (Recommended)")
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.legend()
ax.grid(True)
"""

    with col_demo:
        if style_choice == "Pyplot (快捷模式)":
            fig = plt.figure(figsize=(6, 4))
            plt.plot(x, y, label='Sine Wave', color='blue')
            plt.title("Pyplot Style")
            plt.xlabel("X Axis")
            plt.ylabel("Y Axis")
            plt.legend()
            plt.grid(True)
        else:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(x, y, label='Sine Wave', color='green')
            ax.set_title("OO Style (Recommended)")
            ax.set_xlabel("X Axis")
            ax.set_ylabel("Y Axis")
            ax.legend()
            ax.grid(True)
        st.pyplot(fig)

    with col_code:
        st.markdown("#### 对应代码")
        st.code(code_pyplot if style_choice == "Pyplot (快捷模式)" else code_oo, language='python')
        
    st.markdown("---")
    st.markdown("### 2. 解构画布：Figure vs Axes")
    st.info("""
    * **Figure (画布)**: 整个图像的容器，可以包含多个子图。
    * **Axes (坐标系)**: 实际绘图的区域（包含坐标轴、线条、标签等）。
    * **Axis (坐标轴)**: 处理刻度和范围。
    * **Artist**: 既然可见，皆为 Artist。
    """)

# --- 章节 3: 基础笔触 ---
elif menu == "3. 基础笔触 (The Brushes)":
    st.title("掌握笔触：Matplotlib 的核心绘图元素")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Line2D (线条)", "Patches (形状)", "Collections (散点)", "Images (图像)"])
    
    with tab1:
        st.subheader("线条的艺术 (Line2D)")
        col_ctrl, col_view = st.columns([1, 2])
        with col_ctrl:
            line_style = st.selectbox("线型 (linestyle)", ['-', '--', '-.', ':'])
            line_width = st.slider("线宽 (linewidth)", 1, 10, 2)
            color = st.color_picker("颜色 (color)", "#FF5733")
            marker = st.selectbox("标记 (marker)", [None, 'o', 's', '^', '*'])
        
        with col_view:
            x = np.linspace(0, 10, 50)
            y = np.cos(x)
            fig, ax = plt.subplots(figsize=(6,4))
            ax.plot(x, y, linestyle=line_style, linewidth=line_width, color=color, marker=marker)
            ax.set_title(f"Line Plot")
            st.pyplot(fig)
            
        st.markdown("**生成代码：**")
        st.code(f"""
fig, ax = plt.subplots()
ax.plot(x, y, 
    linestyle='{line_style}', 
    linewidth={line_width}, 
    color='{color}', 
    marker='{marker}'
)
        """, language='python')

    with tab2:
        st.subheader("塑造形态 (Patches: Bar & Hist)")
        chart_type = st.radio("选择图表类型", ["Bar Chart (条形图)", "Histogram (直方图)", "Pie Chart (饼图)"], horizontal=True)
        
        col_view, col_code = st.columns([1, 1])
        
        fig, ax = plt.subplots(figsize=(6,4))
        code_str = ""
        
        if chart_type == "Bar Chart (条形图)":
            categories = ['A', 'B', 'C', 'D']
            values = [23, 45, 56, 78]
            ax.bar(categories, values, color='skyblue', edgecolor='black')
            ax.set_title("Bar Chart")
            code_str = "ax.bar(categories, values, color='skyblue', edgecolor='black')"
            
        elif chart_type == "Histogram (直方图)":
            data = np.random.randn(1000)
            bins = 20
            ax.hist(data, bins=bins, color='lightgreen', edgecolor='black', alpha=0.7)
            ax.set_title("Histogram")
            code_str = "ax.hist(data, bins=20, color='lightgreen', edgecolor='black', alpha=0.7)"
            
        else:
            labels = ['Frogs', 'Hogs', 'Dogs', 'Logs']
            sizes = [15, 30, 45, 10]
            explode = (0, 0.1, 0, 0) 
            ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
            ax.set_title("Pie Chart")
            code_str = "ax.pie(sizes, explode=(0, 0.1, 0, 0), labels=labels, autopct='%1.1f%%')"
            
        with col_view:
            st.pyplot(fig)
        with col_code:
            st.markdown("**核心代码：**")
            st.code(code_str, language='python')

    with tab3:
        st.subheader("点绘星空 (Collections: Scatter)")
        n_points = st.slider("点数量", 50, 500, 200)
        
        x = np.random.rand(n_points)
        y = np.random.rand(n_points)
        colors = np.random.rand(n_points)
        area = (30 * np.random.rand(n_points))**2 
        
        fig, ax = plt.subplots(figsize=(8,4))
        sc = ax.scatter(x, y, s=area, c=colors, alpha=0.5, cmap='viridis')
        fig.colorbar(sc, ax=ax, label="Color Scale")
        
        st.pyplot(fig)
        st.code(f"""
# 散点图高效绘制 (Collections)
# s=大小数组, c=颜色数组, cmap=色谱
sc = ax.scatter(x, y, s=area, c=colors, alpha=0.5, cmap='viridis')
fig.colorbar(sc, ax=ax)
        """, language='python')

    with tab4:
        st.subheader("渲染像素 (Images: imshow)")
        col1, col2 = st.columns([1,2])
        with col1:
            interpolation = st.selectbox("插值方式", ['nearest', 'bilinear', 'bicubic'])
            cmap = st.selectbox("色图", ['viridis', 'plasma', 'gray'])
        
        data = np.random.rand(30, 30)
        fig, ax = plt.subplots(figsize=(6,5))
        im = ax.imshow(data, interpolation=interpolation, cmap=cmap)
        fig.colorbar(im, ax=ax)
        
        with col2:
            st.pyplot(fig)
            
        st.code(f"ax.imshow(data, interpolation='{interpolation}', cmap='{cmap}')", language='python')

# --- 章节 4: 布局与美学 ---
elif menu == "4. 布局与美学 (Layout & Style)":
    st.title("谋篇布局与画龙点睛")
    
    st.subheader("1. 子图 (Subplots) 与 代码对照")
    st.caption("调整下方的滑块，查看代码如何动态变化以适应不同的子图布局。")
    
    # 增加自由设置行列的功能
    c1, c2 = st.columns(2)
    rows = c1.number_input("行数 (Rows)", min_value=1, max_value=5, value=2)
    cols = c2.number_input("列数 (Columns)", min_value=1, max_value=5, value=2)

    col_img, col_code = st.columns([3, 2])
    
    with col_img:
        fig, axes = plt.subplots(rows, cols, figsize=(8, 6), constrained_layout=True)
        
        # 统一处理 axes，因为当 rows=1, cols=1 时，axes 不是数组
        if rows == 1 and cols == 1:
            axes_flat = [axes]
        else:
            axes_flat = axes.flatten()
            
        for i, ax in enumerate(axes_flat):
            ax.plot(np.random.rand(10), label=f"Line {i}")
            ax.set_title(f"Subplot {i+1}")
            ax.legend(loc='upper right', fontsize='small')
        st.pyplot(fig)
        
    with col_code:
        st.markdown("**实现代码：**")
        code_str = f"""
# {rows}行{cols}列布局，自动调整间距
fig, axes = plt.subplots({rows}, {cols}, 
    constrained_layout=True)

# 注意：当行列数变化时，axes 的形状会变化
# 推荐统一展平处理：
if {rows} * {cols} > 1:
    axes_flat = axes.flatten()
else:
    axes_flat = [axes]

for i, ax in enumerate(axes_flat):
    ax.plot(data)
    ax.set_title(f"Subplot {{i+1}}")
"""
        st.code(code_str, language='python')

    st.markdown("---")
    st.subheader("2. 全局样式 (Style Sheets)")
    
    style_select = st.selectbox("选择样式 (rcParams预设)", plt.style.available, index=plt.style.available.index('ggplot') if 'ggplot' in plt.style.available else 0)
    
    col1, col2 = st.columns([1,1])
    with col1:
        with plt.style.context(style_select):
            fig, ax = plt.subplots(figsize=(6,4))
            x = np.linspace(0, 10, 100)
            for i in range(1, 4):
                ax.plot(x, np.sin(x + i * .5) * (7 - i), label=f"Wave {i}")
            ax.set_title(f"Style: {style_select}")
            ax.legend()
            st.pyplot(fig)
    with col2:
        st.markdown("**上下文管理器代码：**")
        st.code(f"""
# 临时应用样式，不影响全局
with plt.style.context('{style_select}'):
    fig, ax = plt.subplots()
    ax.plot(x, y)
        """, language='python')
            
    st.markdown("### 3. 注解 (Annotations)")
    st.code("""
ax.annotate('Maximum', 
            xy=(2, 1),             # 箭头指向的点
            xytext=(3, 1.5),       # 文字位置
            arrowprops=dict(facecolor='black', shrink=0.05))
    """, language='python')

# --- 章节 5: 进阶画廊 ---
elif menu == "5. 进阶画廊 (Advanced Gallery)":
    st.title("Matplotlib 官方画廊复刻 (Advanced)")
    
    gallery_type = st.selectbox("选择画廊类别", ["3D Plotting", "Polar Coordinates", "Vector Fields (Quiver)", "Fill Between"])
    
    col_viz, col_code = st.columns([3, 2])
    
    fig = plt.figure(figsize=(8, 6))
    code_display = ""
    
    if gallery_type == "3D Plotting":
        ax = fig.add_subplot(111, projection='3d')
        n = 100
        theta = np.linspace(-4 * np.pi, 4 * np.pi, n)
        z = np.linspace(-2, 2, n)
        r = z**2 + 1
        x = r * np.sin(theta)
        y = r * np.cos(theta)
        ax.plot(x, y, z, label='3D Curve')
        ax.legend()
        code_display = """
from mpl_toolkits.mplot3d import Axes3D
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z)
"""

    elif gallery_type == "Polar Coordinates":
        ax = fig.add_subplot(111, projection='polar')
        theta = np.linspace(0, 2*np.pi, 100)
        r = 2 * np.sin(4*theta)
        ax.plot(theta, r, color='crimson', linewidth=2)
        ax.set_title("Polar Plot (Rose Curve)")
        code_display = """
ax = fig.add_subplot(111, projection='polar')
ax.plot(theta, r) # 极坐标绘图
"""
        
    elif gallery_type == "Vector Fields (Quiver)":
        ax = fig.add_subplot(111)
        x, y = np.meshgrid(np.arange(0, 2 * np.pi, .2), np.arange(0, 2 * np.pi, .2))
        u = np.cos(x)
        v = np.sin(y)
        q = ax.quiver(x, y, u, v)
        ax.set_title("Quiver Plot")
        code_display = "ax.quiver(x, y, u, v) # 矢量场"

    elif gallery_type == "Fill Between":
        ax = fig.add_subplot(111)
        x = np.linspace(0, 2, 100)
        y1 = np.sin(2 * np.pi * x)
        y2 = 0.8 * np.sin(4 * np.pi * x)
        ax.plot(x, y1, color='black')
        ax.fill_between(x, y1, y2, where=(y1 > y2), interpolate=True, color='green', alpha=0.3)
        ax.fill_between(x, y1, y2, where=(y1 <= y2), interpolate=True, color='red', alpha=0.3)
        code_display = """
ax.fill_between(x, y1, y2, 
    where=(y1 > y2), 
    color='green', alpha=0.3)
"""

    with col_viz:
        st.pyplot(fig)
    with col_code:
        st.code(code_display, language='python')

# --- 章节 6: 其他库实战 ---
elif menu == "6. 其他库实战 (Modern Libs)":
    st.title("超越 Matplotlib：现代库体验")
    
    lib_choice = st.selectbox("选择可视化库", ["Seaborn (统计)", "Plotly (交互)", "Altair (声明式)"])
    df = px.data.iris() 
    
    if lib_choice == "Seaborn (统计)":
        st.subheader("Seaborn: 极简统计图")
        col_x = st.selectbox("X 轴", df.columns[:-2])
        col_y = st.selectbox("Y 轴", df.columns[:-2], index=1)
        
        fig = sns.jointplot(data=df, x=col_x, y=col_y, hue="species", kind="scatter")
        st.pyplot(fig)
        st.code(f"sns.jointplot(data=df, x='{col_x}', y='{col_y}', hue='species')", language='python')

    elif lib_choice == "Plotly (交互)":
        st.subheader("Plotly: 网页原生交互")
        fig = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width',
                      color='species', size='petal_length', opacity=0.7)
        st.plotly_chart(fig, use_container_width=True)
        st.code("px.scatter_3d(df, x=..., y=..., z=..., color='species')", language='python')

    elif lib_choice == "Altair (声明式)":
        st.subheader("Altair: 语法驱动")
        brush = alt.selection_interval()
        points = alt.Chart(df).mark_point().encode(
            x='sepal_length', y='sepal_width',
            color=alt.condition(brush, 'species', alt.value('lightgray'))
        ).add_params(brush)
        bars = alt.Chart(df).mark_bar().encode(
            y='species', color='species', x='count(species)'
        ).transform_filter(brush)
        
        st.altair_chart(points & bars, use_container_width=True)
        st.code("""
# 交互式联动：散点图筛选影响柱状图
brush = alt.selection_interval()
chart = points.add_params(brush) & bars.transform_filter(brush)
""", language='python')

# --- 章节 7: 进阶挑战 (大师之路) ---
elif menu == "7. 进阶挑战：大师之路 (Master Class) 🚀":
    st.title("🏆 Matplotlib 大神进阶之路")
    st.markdown("本章节复刻了专业数据分析中**最高频、最难**的三个场景。请点击 Tab 切换学习。")
    
    tab_layout, tab_dual, tab_fmt = st.tabs([
        "1. 复杂仪表盘 (Mosaic Layout)", 
        "2. 双轴帕累托图 (Dual Axis)", 
        "3. 专业格式化 (Formatter)"
    ])
    
    # --- 挑战 1: 语义化布局 ---
    with tab_layout:
        st.header("利用 subplot_mosaic 进行语义化布局")
        st.markdown("放弃 `GridSpec` 的复杂索引，使用 ASCII 字符画来定义你的仪表盘布局。")
        
        col_viz, col_code = st.columns([1.5, 1])
        
        # 修正：移除空格，确保 contiguous 连续性
        layout_str = """
        AAB
        AAC
        DDD
        """
        
        with col_viz:
            fig, axd = plt.subplot_mosaic(layout_str, figsize=(10, 6), constrained_layout=True)
            
            # 模拟绘图
            axd['A'].plot(np.cumsum(np.random.randn(100)), color='#2c3e50')
            axd['A'].set_title("Main Trend (A)")
            
            axd['B'].hist(np.random.randn(100), color='#e74c3c')
            axd['B'].set_title("Dist (B)")
            
            axd['C'].scatter(np.random.rand(20), np.random.rand(20), color='#f1c40f')
            axd['C'].set_title("Scatter (C)")
            
            axd['D'].bar(['Q1','Q2','Q3','Q4'], [10,20,15,25], color='#3498db')
            axd['D'].set_title("Quarterly (D)")
            
            st.pyplot(fig)
            
        with col_code:
            st.code("""
# 1. 定义布局 (ASCII Art)
# 修正：移除中间空格，确保D是连续的
layout = \"\"\"
AAB
AAC
DDD
\"\"\"

# 2. 生成 Axes 字典 (axd)
fig, axd = plt.subplot_mosaic(layout, 
    figsize=(10, 6), 
    constrained_layout=True)

# 3. 像字典一样访问
axd['A'].plot(data)
axd['B'].hist(data)
            """, language='python')
            
    # --- 挑战 2: 双轴图 ---
    with tab_dual:
        st.header("双轴图 (Twin Axis) 与 帕累托图")
        st.markdown("在同一个 X 轴上展示两个不同量纲的数据（例如：销售额 vs 累计百分比）。")
        
        col_viz, col_code = st.columns([1.5, 1])
        
        data = pd.DataFrame({'Sales': [100, 80, 50, 30, 10]}, index=['Product A', 'B', 'C', 'D', 'E'])
        data['CumPct'] = data['Sales'].cumsum() / data['Sales'].sum() * 100
        
        with col_viz:
            fig, ax1 = plt.subplots(figsize=(10, 5))
            
            # 轴1：柱状图
            color = 'tab:blue'
            ax1.set_xlabel('Product')
            ax1.set_ylabel('Sales Volume', color=color)
            ax1.bar(data.index, data['Sales'], color=color, alpha=0.6)
            ax1.tick_params(axis='y', labelcolor=color)
            
            # 轴2：共享 X 轴
            ax2 = ax1.twinx()  
            color = 'tab:red'
            ax2.set_ylabel('Cumulative %', color=color)
            ax2.plot(data.index, data['CumPct'], color=color, marker='o', linewidth=2)
            ax2.tick_params(axis='y', labelcolor=color)
            ax2.set_ylim(0, 110)
            
            st.pyplot(fig)
            
        with col_code:
            st.code("""
fig, ax1 = plt.subplots()

# 绘制左轴
ax1.bar(x, sales, color='blue')
ax1.set_ylabel('Sales', color='blue')

# 关键：实例化共享 X 轴的第二个轴
ax2 = ax1.twinx()

# 绘制右轴
ax2.plot(x, pct, color='red')
ax2.set_ylabel('Percentage', color='red')
            """, language='python')

    # --- 挑战 3: 格式化 ---
    with tab_fmt:
        st.header("专业格式化 (FuncFormatter)")
        st.markdown("将丑陋的科学计数法（1e6）转换为可读性强的商业格式（$1M）。")
        
        col_viz, col_code = st.columns([1.5, 1])
        
        with col_viz:
            money = [1500000, 2500000, 3800000]
            names = ['A Corp', 'B Corp', 'C Corp']
            
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.barh(names, money, color='#16a085')
            
            # 定义格式化函数
            def currency(x, pos):
                if x >= 1e6:
                    return f'${x*1e-6:.1f}M'
                return f'${x:.0f}'
            
            # 应用 Formatter
            formatter = FuncFormatter(currency)
            ax.xaxis.set_major_formatter(formatter)
            ax.set_title("Revenue (Formatted)")
            
            st.pyplot(fig)
            
        with col_code:
            st.code("""
from matplotlib.ticker import FuncFormatter

def currency(x, pos):
    if x >= 1e6:
        return f'${x*1e-6:.1f}M'
    return f'${x:.0f}'

formatter = FuncFormatter(currency)
ax.xaxis.set_major_formatter(formatter)
            """, language='python')

# --- 页脚 ---
st.sidebar.markdown("---")
st.sidebar.caption("Bin Wang, SEU")
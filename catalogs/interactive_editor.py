"""
交互式图表编辑器 - 在一个页面内调整所有matplotlib参数
"""
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.lines
import matplotlib.colors as mcolors
import numpy as np
from typing import Dict, Tuple, Optional, List
from catalogs.utils import ensure_chinese_font, generate_sample_data
from catalogs.line import get_drawstyle_options, get_capstyle_options, get_joinstyle_options
from catalogs.text import get_fontweight_options, get_fontstyle_options, get_fontfamily_options

@st.cache_data
def get_all_available_styles() -> List[str]:
    """
    获取所有可用的样式表，包括matplotlib内置的和第三方库的样式表
    
    支持的第三方库：
    - matplotlib-stylelib: 提供更多样式表
    - seaborn: 提供seaborn样式（如果已安装）
    """
    styles = []
    
    # 1. 添加matplotlib内置样式
    try:
        builtin_styles = list(plt.style.available)
        styles.extend(builtin_styles)
    except Exception:
        pass
    
    # 2. 尝试导入matplotlib-stylelib
    # matplotlib-stylelib有多种导入方式
    stylelib_imported = False
    try:
        import stylelib
        stylelib_imported = True
    except ImportError:
        try:
            import matplotlib_stylelib as stylelib
            stylelib_imported = True
        except ImportError:
            pass
    
    if stylelib_imported:
        # stylelib会自动注册样式到matplotlib
        # 重新获取可用样式（可能已包含stylelib的样式）
        try:
            updated_styles = list(plt.style.available)
            styles = list(set(styles + updated_styles))  # 去重
        except Exception:
            pass
    
    # 3. 尝试导入seaborn样式（seaborn已安装但样式可能需要单独注册）
    try:
        import seaborn as sns
        # seaborn样式通常已经通过seaborn导入自动注册到plt.style.available
        # 重新获取可用样式（可能已包含seaborn的样式）
        updated_styles = list(plt.style.available)
        styles = list(set(styles + updated_styles))  # 去重
    except ImportError:
        pass
    except Exception:
        pass
    
    # 4. 去重并排序
    styles = sorted(list(set(styles)))
    
    # 6. 确保'default'在第一位
    if 'default' in styles:
        styles.remove('default')
        styles.insert(0, 'default')
    else:
        styles.insert(0, 'default')
    
    return styles

def generate_code(params: Dict) -> str:
    """根据参数生成完整的matplotlib代码"""
    code_lines = [
        "import matplotlib.pyplot as plt",
        "import numpy as np",
        "",
    ]
    
    # 样式表
    style_sheet = params.get('style_sheet', 'default')
    if style_sheet != 'default':
        code_lines.append(f"# 应用样式表")
        # 检查是否是第三方样式库的样式
        third_party_styles = ['seaborn', 'stylelib']
        is_third_party = any(style in style_sheet.lower() for style in third_party_styles)
        
        if is_third_party:
            # 添加第三方库导入提示
            if 'seaborn' in style_sheet.lower():
                code_lines.append("# 注意：此样式需要安装 seaborn 库")
                code_lines.append("# pip install seaborn")
                code_lines.append("import seaborn as sns  # 导入seaborn会自动注册样式")
            elif 'stylelib' in style_sheet.lower() or style_sheet not in plt.style.available:
                code_lines.append("# 注意：此样式可能需要安装 matplotlib-stylelib 库")
                code_lines.append("# pip install matplotlib-stylelib")
                code_lines.append("# import stylelib  # 取消注释以使用stylelib样式")
        
        code_lines.append(f"plt.style.use('{style_sheet}')")
        code_lines.append("")
    
    code_lines.append("# 生成示例数据")
    code_lines.append("x = np.linspace(0, 10, 50)")
    code_lines.append("y = np.sin(x)")
    code_lines.append("")
    
    # Figure参数
    figsize = params.get('figsize', (8, 6))
    dpi = params.get('dpi', 100)
    facecolor = params.get('facecolor', 'white')
    
    # 子图布局
    subplot_rows = params.get('subplot_rows', 1)
    subplot_cols = params.get('subplot_cols', 1)
    
    code_lines.append("# 创建图表")
    if subplot_rows > 1 or subplot_cols > 1:
        code_lines.append(f"fig, axes = plt.subplots({subplot_rows}, {subplot_cols}, figsize={figsize}, dpi={dpi}, constrained_layout=True)")
        code_lines.append("")
        code_lines.append("# 统一处理 axes")
        code_lines.append(f"if {subplot_rows} * {subplot_cols} > 1:")
        code_lines.append("    axes_flat = axes.flatten()")
        code_lines.append("else:")
        code_lines.append("    axes_flat = [axes]")
        code_lines.append("")
        code_lines.append("# 为每个子图绘制")
        code_lines.append("for idx, ax in enumerate(axes_flat):")
        code_lines.append("    # 绘制代码（见下方）")
    else:
        code_lines.append(f"fig, ax = plt.subplots(figsize={figsize}, dpi={dpi})")
    # 处理facecolor，如果是hex格式需要引号
    if facecolor != 'white':
        if isinstance(facecolor, str) and facecolor.startswith('#'):
            code_lines.append(f"fig.set_facecolor('{facecolor}')")
        elif isinstance(facecolor, str):
            code_lines.append(f"fig.set_facecolor('{facecolor}')")
        else:
            code_lines.append(f"fig.set_facecolor({facecolor})")
    
    code_lines.append("")
    code_lines.append("# 绘制数据")
    
    # 图表类型
    chart_type = params.get('chart_type', 'plot')
    
    # Line参数
    line_params = []
    if params.get('linewidth', 2) != 2:
        line_params.append(f"linewidth={params['linewidth']}")
    if params.get('linestyle', '-') != '-':
        linestyle = params.get('linestyle', '-')
        if isinstance(linestyle, str):
            line_params.append(f"linestyle='{linestyle}'")
        else:
            line_params.append(f"linestyle={linestyle}")
    color = params.get('color', 'C0')
    # 如果颜色是hex格式，需要特殊处理
    if isinstance(color, str) and color.startswith('#'):
        line_params.append(f"color='{color}'")
    elif color != 'C0':
        if isinstance(color, str):
            line_params.append(f"color='{color}'")
        else:
            line_params.append(f"color={color}")
    if params.get('alpha', 1.0) != 1.0:
        line_params.append(f"alpha={params['alpha']}")
    
    # 添加更多线条参数
    if params.get('drawstyle') and params.get('drawstyle') != 'default':
        line_params.append(f"drawstyle='{params['drawstyle']}'")
    if params.get('capstyle') and params.get('capstyle') != 'butt':
        line_params.append(f"solid_capstyle='{params['capstyle']}'")
    if params.get('joinstyle') and params.get('joinstyle') != 'miter':
        line_params.append(f"solid_joinstyle='{params['joinstyle']}'")
    
    # Marker参数
    marker_params = []
    if params.get('marker') is not None:
        marker = params.get('marker')
        if isinstance(marker, str):
            marker_params.append(f"marker='{marker}'")
        else:
            marker_params.append(f"marker={marker}")
    if params.get('markersize', 6) != 6:
        marker_params.append(f"markersize={params['markersize']}")
    if params.get('markerfacecolor') is not None:
        mfc = params.get('markerfacecolor')
        if isinstance(mfc, str):
            marker_params.append(f"markerfacecolor='{mfc}'")
        else:
            marker_params.append(f"markerfacecolor={mfc}")
    if params.get('markeredgecolor') is not None:
        mec = params.get('markeredgecolor')
        if isinstance(mec, str):
            marker_params.append(f"markeredgecolor='{mec}'")
        else:
            marker_params.append(f"markeredgecolor={mec}")
    if params.get('markeredgewidth', 1) != 1:
        marker_params.append(f"markeredgewidth={params['markeredgewidth']}")
    if params.get('fillstyle', 'full') != 'full':
        marker_params.append(f"fillstyle='{params['fillstyle']}'")
    
    all_params = line_params + marker_params
    param_str = ", ".join(all_params) if all_params else ""
    
    # 根据图表类型生成代码
    if subplot_rows > 1 or subplot_cols > 1:
        indent = "    "
    else:
        indent = ""
    
    if chart_type == 'plot':
        code_lines.append(f"{indent}ax.plot(x, y{', ' + param_str if param_str else ''})")
    elif chart_type == 'scatter':
        # scatter不支持：linestyle, linewidth, drawstyle, solid_capstyle, solid_joinstyle
        # 只保留color, alpha和marker相关参数
        scatter_params = [p for p in all_params if not any(x in p for x in ['linestyle', 'linewidth', 'drawstyle', 'capstyle', 'joinstyle'])]
        scatter_str = ", ".join(scatter_params) if scatter_params else ""
        code_lines.append(f"{indent}ax.scatter(x, y{', ' + scatter_str if scatter_str else ''})")
    elif chart_type == 'bar':
        # bar不支持：所有Line参数（linestyle, linewidth, drawstyle, capstyle, joinstyle）和所有Marker参数
        # 只保留color和alpha
        bar_params = [p for p in all_params if not any(x in p for x in ['linestyle', 'linewidth', 'drawstyle', 'capstyle', 'joinstyle', 'marker'])]
        bar_str = ", ".join(bar_params) if bar_params else ""
        code_lines.append(f"{indent}ax.bar(x[:10], y[:10]{', ' + bar_str if bar_str else ''})")
    elif chart_type == 'hist':
        # hist不支持：所有Line参数和所有Marker参数
        # 只保留color和alpha
        hist_params = [p for p in all_params if not any(x in p for x in ['linestyle', 'linewidth', 'drawstyle', 'capstyle', 'joinstyle', 'marker'])]
        hist_str = ", ".join(hist_params) if hist_params else ""
        code_lines.append(f"{indent}ax.hist(y, bins=20{', ' + hist_str if hist_str else ''})")
    elif chart_type == 'box':
        code_lines.append(f"{indent}ax.boxplot([y])")
    elif chart_type == 'pie':
        code_lines.append(f"{indent}ax.pie(np.abs(y[:5]), labels=[f'Item {{i+1}}' for i in range(5)])")
    
    code_lines.append("")
    
    # Axes参数
    code_lines.append("# 设置坐标轴")
    if params.get('xlim') is not None:
        xlim = params.get('xlim')
        code_lines.append(f"ax.set_xlim({xlim[0]}, {xlim[1]})")
    if params.get('ylim') is not None:
        ylim = params.get('ylim')
        code_lines.append(f"ax.set_ylim({ylim[0]}, {ylim[1]})")
    
    # Grid
    if params.get('grid', False):
        grid_params = []
        if params.get('grid_alpha', 0.3) != 0.3:
            grid_params.append(f"alpha={params['grid_alpha']}")
        if params.get('grid_linestyle', '-') != '-':
            grid_params.append(f"linestyle='{params['grid_linestyle']}'")
        grid_color = params.get('grid_color')
        if grid_color is not None:
            if isinstance(grid_color, str):
                grid_params.append(f"color='{grid_color}'")
            else:
                grid_params.append(f"color={grid_color}")
        grid_str = ", ".join(grid_params) if grid_params else ""
        code_lines.append(f"ax.grid(True{', ' + grid_str if grid_str else ''})")
    
    # Spines
    spines_hidden = []
    if not params.get('spine_top', True):
        spines_hidden.append("'top'")
    if not params.get('spine_right', True):
        spines_hidden.append("'right'")
    if not params.get('spine_bottom', True):
        spines_hidden.append("'bottom'")
    if not params.get('spine_left', True):
        spines_hidden.append("'left'")
    
    for spine in spines_hidden:
        code_lines.append(f"ax.spines[{spine}].set_visible(False)")
    
    # Title和Labels
    code_lines.append("")
    code_lines.append(f"{indent}# 设置标题和标签")
    title = params.get('title', '')
    if title:
        title_params = []
        if params.get('title_fontsize', 14) != 14:
            title_params.append(f"fontsize={params['title_fontsize']}")
        if params.get('title_fontweight', 'normal') != 'normal':
            title_params.append(f"fontweight='{params['title_fontweight']}'")
        if params.get('title_fontstyle', 'normal') != 'normal':
            title_params.append(f"fontstyle='{params['title_fontstyle']}'")
        if params.get('title_fontfamily', 'sans-serif') != 'sans-serif':
            title_params.append(f"fontfamily='{params['title_fontfamily']}'")
        title_color = params.get('title_color')
        if title_color is not None:
            if isinstance(title_color, str):
                title_params.append(f"color='{title_color}'")
            else:
                title_params.append(f"color={title_color}")
        title_param_str = ", ".join(title_params) if title_params else ""
        code_lines.append(f"{indent}ax.set_title('{title}'{', ' + title_param_str if title_param_str else ''})")
    
    xlabel = params.get('xlabel', '')
    if xlabel:
        xlabel_params = []
        if params.get('xlabel_fontsize', 12) != 12:
            xlabel_params.append(f"fontsize={params['xlabel_fontsize']}")
        if params.get('xlabel_fontweight', 'normal') != 'normal':
            xlabel_params.append(f"fontweight='{params['xlabel_fontweight']}'")
        if params.get('xlabel_fontstyle', 'normal') != 'normal':
            xlabel_params.append(f"fontstyle='{params['xlabel_fontstyle']}'")
        if params.get('xlabel_fontfamily', 'sans-serif') != 'sans-serif':
            xlabel_params.append(f"fontfamily='{params['xlabel_fontfamily']}'")
        xlabel_param_str = ", ".join(xlabel_params) if xlabel_params else ""
        code_lines.append(f"{indent}ax.set_xlabel('{xlabel}'{', ' + xlabel_param_str if xlabel_param_str else ''})")
    
    ylabel = params.get('ylabel', '')
    if ylabel:
        ylabel_params = []
        if params.get('ylabel_fontsize', 12) != 12:
            ylabel_params.append(f"fontsize={params['ylabel_fontsize']}")
        if params.get('ylabel_fontweight', 'normal') != 'normal':
            ylabel_params.append(f"fontweight='{params['ylabel_fontweight']}'")
        if params.get('ylabel_fontstyle', 'normal') != 'normal':
            ylabel_params.append(f"fontstyle='{params['ylabel_fontstyle']}'")
        if params.get('ylabel_fontfamily', 'sans-serif') != 'sans-serif':
            ylabel_params.append(f"fontfamily='{params['ylabel_fontfamily']}'")
        ylabel_param_str = ", ".join(ylabel_params) if ylabel_params else ""
        code_lines.append(f"{indent}ax.set_ylabel('{ylabel}'{', ' + ylabel_param_str if ylabel_param_str else ''})")
    
    code_lines.append("")
    if subplot_rows > 1 or subplot_cols > 1:
        code_lines.append("plt.tight_layout()")
    else:
        code_lines.append("plt.tight_layout()")
    code_lines.append("plt.show()")
    
    return "\n".join(code_lines)

def render_plot(params: Dict) -> plt.Figure:
    """根据参数渲染图表"""
    ensure_chinese_font()
    
    # 获取样式表
    style_sheet = params.get('style_sheet', 'default')
    
    # 尝试导入第三方样式库（如果样式需要）
    # 这确保在运行时也能使用第三方样式
    if style_sheet != 'default':
        try:
            # 尝试导入stylelib（如果样式可能需要它）
            if 'stylelib' in style_sheet.lower() or style_sheet not in plt.style.available:
                try:
                    import stylelib
                except ImportError:
                    try:
                        import matplotlib_stylelib as stylelib
                    except ImportError:
                        pass
        except Exception:
            pass
        
        # 尝试导入seaborn（如果样式可能需要它）
        if 'seaborn' in style_sheet.lower():
            try:
                import seaborn as sns
            except ImportError:
                pass
    
    # 使用样式上下文管理器来应用样式
    # 这确保样式在创建figure时生效，并且不会影响全局状态
    if style_sheet != 'default':
        try:
            style_context = plt.style.context(style_sheet)
        except Exception as e:
            # 如果样式不存在，使用默认样式
            st.warning(f"样式 '{style_sheet}' 不可用，使用默认样式。错误: {str(e)}")
            style_context = plt.style.context('default')
    else:
        style_context = plt.style.context('default')
    
    # 在样式上下文中创建和绘制图表
    with style_context:
        # 创建Figure
        figsize = params.get('figsize', (8, 6))
        dpi = params.get('dpi', 100)
        facecolor = params.get('facecolor', 'white')
        
        # 子图布局
        subplot_rows = params.get('subplot_rows', 1)
        subplot_cols = params.get('subplot_cols', 1)
        
        if subplot_rows > 1 or subplot_cols > 1:
            fig, axes = plt.subplots(subplot_rows, subplot_cols, figsize=figsize, dpi=dpi, constrained_layout=True)
            if subplot_rows == 1 and subplot_cols == 1:
                axes_flat = [axes]
            else:
                axes_flat = axes.flatten() if hasattr(axes, 'flatten') else [axes]
        else:
            fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
            axes_flat = [ax]
        
        fig.set_facecolor(facecolor)
        
        # 生成数据
        x, y = generate_sample_data(50)
        
        # 为每个子图绘制
        chart_type = params.get('chart_type', 'plot')
        
        for idx, ax in enumerate(axes_flat):
            # 准备plot参数
            plot_kwargs = {}
            
            # Line参数
            if params.get('linewidth') is not None:
                plot_kwargs['linewidth'] = params['linewidth']
            if params.get('linestyle') is not None:
                plot_kwargs['linestyle'] = params['linestyle']
            if params.get('color') is not None:
                plot_kwargs['color'] = params['color']
            if params.get('alpha') is not None:
                plot_kwargs['alpha'] = params['alpha']
            
            # 添加更多线条参数
            if params.get('drawstyle') is not None and params.get('drawstyle') != 'default':
                plot_kwargs['drawstyle'] = params['drawstyle']
            if params.get('capstyle') is not None:
                plot_kwargs['solid_capstyle'] = params['capstyle']
            if params.get('joinstyle') is not None:
                plot_kwargs['solid_joinstyle'] = params['joinstyle']
            
            # Marker参数
            if params.get('marker') is not None:
                plot_kwargs['marker'] = params['marker']
            if params.get('markersize') is not None:
                plot_kwargs['markersize'] = params['markersize']
            if params.get('markerfacecolor') is not None:
                plot_kwargs['markerfacecolor'] = params['markerfacecolor']
            if params.get('markeredgecolor') is not None:
                plot_kwargs['markeredgecolor'] = params['markeredgecolor']
            if params.get('markeredgewidth') is not None:
                plot_kwargs['markeredgewidth'] = params['markeredgewidth']
            if params.get('fillstyle') is not None:
                plot_kwargs['fillstyle'] = params['fillstyle']
            
            # 根据图表类型绘制，过滤不兼容的参数
            if chart_type == 'plot':
                # plot支持所有参数
                ax.plot(x, y, **plot_kwargs)
            elif chart_type == 'scatter':
                # scatter的参数映射：color -> c, markersize -> s, markerfacecolor -> c (通过c参数)
                # scatter不支持：linestyle, linewidth, drawstyle, solid_capstyle, solid_joinstyle
                scatter_kwargs = {}
                if 'color' in plot_kwargs:
                    scatter_kwargs['c'] = plot_kwargs['color']
                if 'alpha' in plot_kwargs:
                    scatter_kwargs['alpha'] = plot_kwargs['alpha']
                if 'markersize' in plot_kwargs:
                    scatter_kwargs['s'] = plot_kwargs['markersize'] ** 2  # scatter的s是面积，需要平方
                if 'marker' in plot_kwargs:
                    scatter_kwargs['marker'] = plot_kwargs['marker']
                if 'markerfacecolor' in plot_kwargs:
                    scatter_kwargs['c'] = plot_kwargs['markerfacecolor']
                if 'markeredgecolor' in plot_kwargs:
                    scatter_kwargs['edgecolors'] = plot_kwargs['markeredgecolor']
                if 'markeredgewidth' in plot_kwargs:
                    scatter_kwargs['linewidths'] = plot_kwargs['markeredgewidth']
                ax.scatter(x, y, **scatter_kwargs)
            elif chart_type == 'bar':
                # bar不支持：linestyle, marker相关, linewidth, drawstyle, solid_capstyle, solid_joinstyle
                bar_kwargs = {}
                if 'color' in plot_kwargs:
                    bar_kwargs['color'] = plot_kwargs['color']
                if 'alpha' in plot_kwargs:
                    bar_kwargs['alpha'] = plot_kwargs['alpha']
                ax.bar(x[:10], y[:10], **bar_kwargs)
            elif chart_type == 'hist':
                # hist不支持：linestyle, marker相关, linewidth, drawstyle, solid_capstyle, solid_joinstyle
                hist_kwargs = {}
                if 'color' in plot_kwargs:
                    hist_kwargs['color'] = plot_kwargs['color']
                if 'alpha' in plot_kwargs:
                    hist_kwargs['alpha'] = plot_kwargs['alpha']
                ax.hist(y, bins=20, **hist_kwargs)
            elif chart_type == 'box':
                # boxplot不支持color和alpha参数，需要通过patch_artist和boxprops设置
                ax.boxplot([y], patch_artist=True)
                # 设置颜色
                if 'color' in plot_kwargs:
                    for patch in ax.artists:
                        patch.set_facecolor(plot_kwargs['color'])
                        if 'alpha' in plot_kwargs:
                            patch.set_alpha(plot_kwargs['alpha'])
            elif chart_type == 'pie':
                # pie只支持colors参数（需要是列表），不支持alpha
                pie_kwargs = {}
                if 'color' in plot_kwargs:
                    # pie需要colors参数（列表），而不是color
                    pie_kwargs['colors'] = [plot_kwargs['color']] * 5
                ax.pie(np.abs(y[:5]), labels=[f'Item {i+1}' for i in range(5)], **pie_kwargs)
            
            # 设置坐标轴范围
            if params.get('xlim') is not None:
                ax.set_xlim(params['xlim'])
            if params.get('ylim') is not None:
                ax.set_ylim(params['ylim'])
            
            # Grid
            if params.get('grid', False):
                grid_kwargs = {}
                if params.get('grid_alpha') is not None:
                    grid_kwargs['alpha'] = params['grid_alpha']
                if params.get('grid_linestyle') is not None:
                    grid_kwargs['linestyle'] = params['grid_linestyle']
                if params.get('grid_color') is not None:
                    grid_kwargs['color'] = params['grid_color']
                ax.grid(True, **grid_kwargs)
            
            # Spines
            if not params.get('spine_top', True):
                ax.spines['top'].set_visible(False)
            if not params.get('spine_right', True):
                ax.spines['right'].set_visible(False)
            if not params.get('spine_bottom', True):
                ax.spines['bottom'].set_visible(False)
            if not params.get('spine_left', True):
                ax.spines['left'].set_visible(False)
            
            # Title和Labels（仅对第一个子图或单个图）
            if idx == 0:
                title_params = {}
                if params.get('title_fontsize') is not None:
                    title_params['fontsize'] = params['title_fontsize']
                if params.get('title_fontweight') is not None:
                    title_params['fontweight'] = params['title_fontweight']
                if params.get('title_fontstyle') is not None:
                    title_params['fontstyle'] = params['title_fontstyle']
                if params.get('title_fontfamily') is not None:
                    title_params['fontfamily'] = params['title_fontfamily']
                if params.get('title_color') is not None:
                    title_params['color'] = params['title_color']
                
                if params.get('title'):
                    ax.set_title(params['title'], **title_params)
                
                xlabel_params = {}
                if params.get('xlabel_fontsize') is not None:
                    xlabel_params['fontsize'] = params['xlabel_fontsize']
                if params.get('xlabel_fontweight') is not None:
                    xlabel_params['fontweight'] = params['xlabel_fontweight']
                if params.get('xlabel_fontstyle') is not None:
                    xlabel_params['fontstyle'] = params['xlabel_fontstyle']
                if params.get('xlabel_fontfamily') is not None:
                    xlabel_params['fontfamily'] = params['xlabel_fontfamily']
                if params.get('xlabel'):
                    ax.set_xlabel(params['xlabel'], **xlabel_params)
                
                ylabel_params = {}
                if params.get('ylabel_fontsize') is not None:
                    ylabel_params['fontsize'] = params['ylabel_fontsize']
                if params.get('ylabel_fontweight') is not None:
                    ylabel_params['fontweight'] = params['ylabel_fontweight']
                if params.get('ylabel_fontstyle') is not None:
                    ylabel_params['fontstyle'] = params['ylabel_fontstyle']
                if params.get('ylabel_fontfamily') is not None:
                    ylabel_params['fontfamily'] = params['ylabel_fontfamily']
                if params.get('ylabel'):
                    ax.set_ylabel(params['ylabel'], **ylabel_params)
            else:
                # 其他子图显示编号
                ax.set_title(f"Subplot {idx+1}", fontsize=10)
        
        return fig

def render_interactive_editor():
    """渲染交互式图表编辑器主界面"""
    ensure_chinese_font()
    
    st.title("🎨 Matplotlib 交互式图表编辑器")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;'>
        <p style='margin: 0; font-size: 1.1rem;'>在一个页面内调整所有matplotlib参数，实时预览效果并生成代码</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 初始化session state
    if 'plot_params' not in st.session_state:
        st.session_state.plot_params = {
            # Chart Type
            'chart_type': 'plot',
            'subplot_rows': 1,
            'subplot_cols': 1,
            'style_sheet': 'default',
            # Figure
            'figsize': (8.0, 6.0),
            'dpi': 100,
            'facecolor': 'white',
            # Line
            'linewidth': 2.0,
            'linestyle': '-',
            'color': 'C0',
            'alpha': 1.0,
            'drawstyle': 'default',
            'capstyle': 'butt',
            'joinstyle': 'miter',
            # Marker
            'marker': None,
            'markersize': 6,
            'markerfacecolor': None,
            'markeredgecolor': None,
            'markeredgewidth': 1,
            'fillstyle': 'full',
            # Axes
            'xlim': None,
            'ylim': None,
            'grid': False,
            'grid_alpha': 0.3,
            'grid_linestyle': '-',
            'grid_color': None,
            'spine_top': True,
            'spine_right': True,
            'spine_bottom': True,
            'spine_left': True,
            # Text
            'title': '',
            'title_fontsize': 14,
            'title_fontweight': 'normal',
            'title_fontstyle': 'normal',
            'title_fontfamily': 'sans-serif',
            'title_color': None,
            'xlabel': '',
            'xlabel_fontsize': 12,
            'xlabel_fontweight': 'normal',
            'xlabel_fontstyle': 'normal',
            'xlabel_fontfamily': 'sans-serif',
            'ylabel': '',
            'ylabel_fontsize': 12,
            'ylabel_fontweight': 'normal',
            'ylabel_fontstyle': 'normal',
            'ylabel_fontfamily': 'sans-serif',
        }
    
    params = st.session_state.plot_params
    
    # 使用两列布局：左侧参数面板，右侧图表和代码
    col_left, col_right = st.columns([1, 1.5])
    
    with col_left:
        st.markdown("### ⚙️ 参数设置")
        
        # 图表类型和布局
        with st.expander("🎯 图表类型与布局", expanded=True):
            chart_types = ['plot', 'scatter', 'bar', 'hist', 'box', 'pie']
            chart_idx = chart_types.index(params.get('chart_type', 'plot')) if params.get('chart_type', 'plot') in chart_types else 0
            params['chart_type'] = st.selectbox("图表类型", chart_types, index=chart_idx, key='chart_type')
            
            use_subplots = st.checkbox("使用子图布局", value=params.get('subplot_rows', 1) > 1 or params.get('subplot_cols', 1) > 1, key='use_subplots')
            if use_subplots:
                params['subplot_rows'] = st.number_input("行数", 1, 5, params.get('subplot_rows', 1), 1, key='subplot_rows')
                params['subplot_cols'] = st.number_input("列数", 1, 5, params.get('subplot_cols', 1), 1, key='subplot_cols')
            else:
                params['subplot_rows'] = 1
                params['subplot_cols'] = 1
            
            # 样式表 - 使用扩展函数获取所有可用样式
            available_styles = get_all_available_styles()
            
            # 显示样式表信息和安装提示
            with st.expander("ℹ️ 关于样式表", expanded=False):
                st.markdown("""
                **内置样式表**：Matplotlib自带的样式表
                
                **扩展样式表**：通过安装以下库可获得更多样式：
                - `pip install matplotlib-stylelib` - 提供更多专业样式
                - `pip install seaborn` - 提供seaborn系列样式（已包含）
                
                安装后刷新页面即可看到新样式。
                """)
            
            # 检查当前选择的样式是否仍然可用
            current_style = params.get('style_sheet', 'default')
            if current_style not in available_styles:
                current_style = 'default'
                params['style_sheet'] = 'default'
            
            style_idx = available_styles.index(current_style) if current_style in available_styles else 0
            params['style_sheet'] = st.selectbox(
                f"样式表 (Style Sheet) - 共 {len(available_styles)} 个", 
                available_styles, 
                index=style_idx, 
                key='style_sheet',
                help="选择图表样式。安装matplotlib-stylelib可获得更多样式选项。"
            )
        
        # 使用expander组织参数
        with st.expander("📐 Figure (画布)", expanded=True):
            fig_width = st.slider("宽度 (英寸)", 2.0, 20.0, float(params['figsize'][0]), 0.5, key='fig_width')
            fig_height = st.slider("高度 (英寸)", 2.0, 20.0, float(params['figsize'][1]), 0.5, key='fig_height')
            params['figsize'] = (fig_width, fig_height)
            
            params['dpi'] = st.slider("DPI", 50, 300, params['dpi'], 10, key='dpi')
            facecolor = params.get('facecolor', 'white')
            if not isinstance(facecolor, str) or not facecolor.startswith('#'):
                facecolor = '#FFFFFF' if facecolor == 'white' else '#000000' if facecolor == 'black' else '#FFFFFF'
            params['facecolor'] = st.color_picker("背景颜色", facecolor, key='facecolor')
        
        # 根据图表类型决定显示哪些参数
        chart_type = params.get('chart_type', 'plot')
        
        # Line (线条) 参数 - 仅 plot 类型支持
        if chart_type == 'plot':
            with st.expander("📈 Line (线条)", expanded=True):
                params['linewidth'] = st.slider("线宽", 0.5, 10.0, float(params['linewidth']), 0.5, key='linewidth')
                
                linestyle_options = ['-', '--', '-.', ':', 'None']
                linestyle_idx = linestyle_options.index(params['linestyle']) if params['linestyle'] in linestyle_options else 0
                params['linestyle'] = st.selectbox("线型", linestyle_options, index=linestyle_idx, key='linestyle')
                
                # 处理颜色值显示
                current_color = params['color']
                if not isinstance(current_color, str) or not current_color.startswith('#'):
                    current_color = '#1f77b4'  # 默认蓝色
                params['color'] = st.color_picker("线条颜色", current_color, key='line_color')
                
                params['alpha'] = st.slider("透明度", 0.0, 1.0, float(params['alpha']), 0.1, key='alpha')
                
                # 添加更多线条参数
                drawstyles = get_drawstyle_options()
                drawstyle_keys = list(drawstyles.keys())
                drawstyle_idx = drawstyle_keys.index(params.get('drawstyle', 'default')) if params.get('drawstyle', 'default') in drawstyle_keys else 0
                params['drawstyle'] = st.selectbox("绘制样式 (drawstyle)", drawstyle_keys, index=drawstyle_idx, key='drawstyle')
                
                capstyles = get_capstyle_options()
                capstyle_idx = capstyles.index(params.get('capstyle', 'butt')) if params.get('capstyle', 'butt') in capstyles else 0
                params['capstyle'] = st.selectbox("线端样式 (capstyle)", capstyles, index=capstyle_idx, key='capstyle')
                
                joinstyles = get_joinstyle_options()
                joinstyle_idx = joinstyles.index(params.get('joinstyle', 'miter')) if params.get('joinstyle', 'miter') in joinstyles else 0
                params['joinstyle'] = st.selectbox("连接样式 (joinstyle)", joinstyles, index=joinstyle_idx, key='joinstyle')
        else:
            # 对于非 plot 类型，只显示颜色和透明度
            with st.expander("🎨 颜色与透明度", expanded=True):
                current_color = params['color']
                if not isinstance(current_color, str) or not current_color.startswith('#'):
                    current_color = '#1f77b4'  # 默认蓝色
                params['color'] = st.color_picker("颜色", current_color, key='line_color')
                
                # box 和 pie 类型对 alpha 的支持有限，但为了统一性还是显示
                if chart_type not in ['pie']:  # pie 不支持 alpha
                    params['alpha'] = st.slider("透明度", 0.0, 1.0, float(params['alpha']), 0.1, key='alpha')
        
        # Marker (标记点) 参数 - plot 和 scatter 类型支持
        if chart_type in ['plot', 'scatter']:
            with st.expander("🔵 Marker (标记点)", expanded=True):
                show_marker = st.checkbox("显示标记点", value=params['marker'] is not None, key='show_marker')
                
                if show_marker:
                    marker_options = [None, '.', ',', 'o', 's', '^', 'v', '<', '>', '*', '+', 'x', 'D', 'd', 'p', 'h', 'H', '8']
                    marker_idx = marker_options.index(params['marker']) if params['marker'] in marker_options else 2
                    params['marker'] = st.selectbox("标记符号", marker_options, index=marker_idx, key='marker')
                    
                    params['markersize'] = st.slider("标记大小", 3, 30, params['markersize'], 1, key='markersize')
                    
                    # 处理标记颜色
                    mfc = params.get('markerfacecolor')
                    if not mfc or (isinstance(mfc, str) and not mfc.startswith('#')):
                        mfc = '#1f77b4'
                    params['markerfacecolor'] = st.color_picker("填充颜色", mfc, key='markerfacecolor')
                    
                    mec = params.get('markeredgecolor')
                    if not mec or (isinstance(mec, str) and not mec.startswith('#')):
                        mec = '#000000'
                    params['markeredgecolor'] = st.color_picker("边框颜色", mec, key='markeredgecolor')
                    
                    params['markeredgewidth'] = st.slider("边框宽度", 0, 5, params['markeredgewidth'], 1, key='markeredgewidth')
                    
                    fillstyle_options = ['full', 'left', 'right', 'top', 'bottom', 'none']
                    fillstyle_idx = fillstyle_options.index(params['fillstyle']) if params['fillstyle'] in fillstyle_options else 0
                    params['fillstyle'] = st.selectbox("填充样式", fillstyle_options, index=fillstyle_idx, key='fillstyle')
                else:
                    params['marker'] = None
        
        with st.expander("📊 Axes (坐标轴)", expanded=True):
            show_xlim = st.checkbox("设置X轴范围", value=params['xlim'] is not None, key='show_xlim')
            if show_xlim:
                xlim_min = st.number_input("X最小值", value=params['xlim'][0] if params['xlim'] else 0.0, key='xlim_min')
                xlim_max = st.number_input("X最大值", value=params['xlim'][1] if params['xlim'] else 10.0, key='xlim_max')
                params['xlim'] = (xlim_min, xlim_max)
            else:
                params['xlim'] = None
            
            show_ylim = st.checkbox("设置Y轴范围", value=params['ylim'] is not None, key='show_ylim')
            if show_ylim:
                ylim_min = st.number_input("Y最小值", value=params['ylim'][0] if params['ylim'] else -1.5, key='ylim_min')
                ylim_max = st.number_input("Y最大值", value=params['ylim'][1] if params['ylim'] else 1.5, key='ylim_max')
                params['ylim'] = (ylim_min, ylim_max)
            else:
                params['ylim'] = None
            
            params['grid'] = st.checkbox("显示网格", value=params['grid'], key='grid')
            if params['grid']:
                params['grid_alpha'] = st.slider("网格透明度", 0.0, 1.0, float(params['grid_alpha']), 0.1, key='grid_alpha')
                grid_ls_options = ['-', '--', '-.', ':', 'None']
                grid_ls_idx = grid_ls_options.index(params['grid_linestyle']) if params['grid_linestyle'] in grid_ls_options else 0
                params['grid_linestyle'] = st.selectbox("网格线型", grid_ls_options, index=grid_ls_idx, key='grid_linestyle')
                grid_color = params.get('grid_color')
                if not grid_color or (isinstance(grid_color, str) and not grid_color.startswith('#')):
                    grid_color = '#808080'
                params['grid_color'] = st.color_picker("网格颜色", grid_color, key='grid_color')
            
            st.markdown("**边框显示**")
            params['spine_top'] = st.checkbox("上边框", value=params['spine_top'], key='spine_top')
            params['spine_right'] = st.checkbox("右边框", value=params['spine_right'], key='spine_right')
            params['spine_bottom'] = st.checkbox("下边框", value=params['spine_bottom'], key='spine_bottom')
            params['spine_left'] = st.checkbox("左边框", value=params['spine_left'], key='spine_left')
        
        with st.expander("📝 Text (文本)", expanded=True):
            params['title'] = st.text_input("标题", value=params.get('title', ''), key='title')
            if params['title']:
                params['title_fontsize'] = st.slider("标题字体大小", 8, 30, params.get('title_fontsize', 14), 1, key='title_fontsize')
                
                fontweights = get_fontweight_options()
                title_fw_idx = fontweights.index(params.get('title_fontweight', 'normal')) if params.get('title_fontweight', 'normal') in fontweights else 0
                params['title_fontweight'] = st.selectbox("标题字体粗细", fontweights[:10], index=min(title_fw_idx, 9), key='title_fontweight')
                
                fontstyles = get_fontstyle_options()
                title_fs_idx = fontstyles.index(params.get('title_fontstyle', 'normal')) if params.get('title_fontstyle', 'normal') in fontstyles else 0
                params['title_fontstyle'] = st.selectbox("标题字体样式", fontstyles, index=title_fs_idx, key='title_fontstyle')
                
                fontfamilies = get_fontfamily_options()
                title_ff_idx = fontfamilies['generic'].index(params.get('title_fontfamily', 'sans-serif')) if params.get('title_fontfamily', 'sans-serif') in fontfamilies['generic'] else 0
                params['title_fontfamily'] = st.selectbox("标题字体族", fontfamilies['generic'], index=title_ff_idx, key='title_fontfamily')
                
                title_color = params.get('title_color')
                if not title_color or (isinstance(title_color, str) and not title_color.startswith('#')):
                    title_color = '#000000'
                params['title_color'] = st.color_picker("标题颜色", title_color, key='title_color')
            
            params['xlabel'] = st.text_input("X轴标签", value=params.get('xlabel', ''), key='xlabel')
            if params['xlabel']:
                params['xlabel_fontsize'] = st.slider("X轴标签字体大小", 8, 24, params.get('xlabel_fontsize', 12), 1, key='xlabel_fontsize')
                xlabel_fw_idx = fontweights.index(params.get('xlabel_fontweight', 'normal')) if params.get('xlabel_fontweight', 'normal') in fontweights else 0
                params['xlabel_fontweight'] = st.selectbox("X轴标签字体粗细", fontweights[:5], index=min(xlabel_fw_idx, 4), key='xlabel_fontweight')
            
            params['ylabel'] = st.text_input("Y轴标签", value=params.get('ylabel', ''), key='ylabel')
            if params['ylabel']:
                params['ylabel_fontsize'] = st.slider("Y轴标签字体大小", 8, 24, params.get('ylabel_fontsize', 12), 1, key='ylabel_fontsize')
                ylabel_fw_idx = fontweights.index(params.get('ylabel_fontweight', 'normal')) if params.get('ylabel_fontweight', 'normal') in fontweights else 0
                params['ylabel_fontweight'] = st.selectbox("Y轴标签字体粗细", fontweights[:5], index=min(ylabel_fw_idx, 4), key='ylabel_fontweight')
    
    with col_right:
        st.markdown("### 📊 实时预览")
        
        # 渲染图表
        try:
            fig = render_plot(params)
            st.pyplot(fig)
            plt.close(fig)
        except Exception as e:
            st.error(f"渲染错误: {str(e)}")
            st.info("请检查参数设置是否正确")
        
        st.markdown("### 💻 生成代码")
        code = generate_code(params)
        st.code(code, language='python')
        
        # 复制代码按钮
        st.markdown(f"""
        <div style='margin-top: 1rem;'>
            <button onclick="navigator.clipboard.writeText(`{code.replace('`', '\\`').replace('$', '\\$')}`)" 
                    style='background-color: #3b82f6; color: white; border: none; padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer;'>
                复制代码
            </button>
        </div>
        """, unsafe_allow_html=True)


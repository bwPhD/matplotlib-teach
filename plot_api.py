"""
统一的图表绘制 API 模块
参考 FigureForge 的设计理念，提供科学、完整的图表绘制接口

设计原则：
1. 统一的图表类型注册机制
2. 参数验证和默认值管理
3. 科学的代码生成逻辑
4. 可扩展的图表类型支持
5. 完整的参数文档
"""

import matplotlib.pyplot as plt
import matplotlib.axes
import numpy as np
import pandas as pd
import json
import csv
import io
from typing import Dict, List, Tuple, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import inspect
import textwrap


class ChartCategory(Enum):
    """图表类别枚举"""
    LINE = "line"           # 线条类
    PATCH = "patch"         # 形状与统计图
    COLLECTION = "collection"  # 集合类型
    IMAGE = "image"         # 图像处理
    STATISTICAL = "statistical"  # 统计图表


@dataclass
class ParameterDefinition:
    """参数定义"""
    name: str
    type: type
    default: Any = None
    description: str = ""
    valid_values: Optional[List[Any]] = None
    validator: Optional[Callable[[Any], bool]] = None
    required: bool = False
    
    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        """验证参数值"""
        if value is None and self.required:
            return False, f"参数 '{self.name}' 是必需的"
        
        if value is None:
            return True, None
        
        # 类型检查
        if not isinstance(value, self.type):
            # 允许类型转换的情况
            if self.type == float and isinstance(value, (int, float)):
                return True, None
            if self.type == int and isinstance(value, (int, float)) and value == int(value):
                return True, None
            # 处理元组类型定义（支持多种类型）
            if isinstance(self.type, tuple):
                # 检查是否是元组中任一类型
                if any(isinstance(value, t) for t in self.type):
                    return True, None
                # 特殊处理：pandas Series 可以转换为 numpy array
                if pd.Series in self.type and isinstance(value, pd.Series):
                    return True, None
                type_names = [t.__name__ if hasattr(t, '__name__') else str(t) for t in self.type]
                return False, f"参数 '{self.name}' 的类型应为 {', '.join(type_names)} 之一，但得到 {type(value).__name__}"
            return False, f"参数 '{self.name}' 的类型应为 {self.type.__name__}，但得到 {type(value).__name__}"
        
        # 有效值检查
        if self.valid_values is not None and value not in self.valid_values:
            return False, f"参数 '{self.name}' 的值 '{value}' 不在有效值列表中: {self.valid_values}"
        
        # 自定义验证器
        if self.validator is not None and not self.validator(value):
            return False, f"参数 '{self.name}' 的值 '{value}' 未通过验证"
        
        return True, None


@dataclass
class ChartType:
    """图表类型定义"""
    name: str
    display_name: str
    category: ChartCategory
    plot_func: Callable  # matplotlib 绘图函数
    parameters: Dict[str, ParameterDefinition] = field(default_factory=dict)
    data_generator: Optional[Callable] = None  # 示例数据生成器
    code_template: Optional[str] = None  # 代码模板
    description: str = ""
    
    def validate_params(self, params: Dict[str, Any]) -> Tuple[bool, Optional[str], Dict[str, Any]]:
        """验证参数并返回清理后的参数字典"""
        validated_params = {}
        
        for param_name, param_def in self.parameters.items():
            value = params.get(param_name, param_def.default)
            
            # 如果参数未提供且不是必需的，使用默认值
            if value is None and not param_def.required:
                if param_def.default is not None:
                    validated_params[param_name] = param_def.default
                continue
            
            # 验证参数
            is_valid, error_msg = param_def.validate(value)
            if not is_valid:
                return False, error_msg, {}
            
            validated_params[param_name] = value
        
        return True, None, validated_params
    
    def generate_code(self, params: Dict[str, Any], data_code: str = "") -> str:
        """生成代码"""
        if self.code_template:
            try:
                return self.code_template.format(**params, data_code=data_code)
            except KeyError:
                pass  # 如果模板格式错误，使用默认生成
        
        # 科学的代码生成逻辑
        param_strs = []
        
        # 优先处理数据参数（x, y, data 等）
        data_params = ['x', 'y', 'data', 'sizes', 'labels', 'height', 'width']
        other_params = []
        
        for key, value in params.items():
            if value is None or key in data_params:
                continue
            
            # 格式化参数值
            formatted_value = self._format_param_value(value)
            other_params.append(f"{key}={formatted_value}")
        
        # 构建函数调用
        func_name = self._get_function_name()
        
        # 构建参数列表
        all_params = []
        
        # 添加位置参数（数据参数）
        for param_name in data_params:
            if param_name in params and params[param_name] is not None:
                value = params[param_name]
                formatted = self._format_param_value(value)
                all_params.append(formatted)
        
        # 添加关键字参数
        all_params.extend(other_params)
        
        if len(all_params) == 0:
            return f"ax.{func_name}()"
        elif len(all_params) == 1:
            return f"ax.{func_name}({all_params[0]})"
        else:
            # 多行格式，提高可读性
            param_lines = [f"    {param}" for param in all_params]
            return f"ax.{func_name}(\n" + ",\n".join(param_lines) + "\n)"
    
    def _format_param_value(self, value: Any) -> str:
        """格式化参数值为代码字符串"""
        if isinstance(value, str):
            # 转义字符串中的引号
            escaped = value.replace("'", "\\'")
            return f"'{escaped}'"
        elif isinstance(value, (list, tuple)):
            if len(value) == 0:
                return "[]"
            # 检查是否包含字符串
            if any(isinstance(v, str) for v in value):
                items = [f"'{v}'" if isinstance(v, str) else str(v) for v in value]
                return f"[{', '.join(items)}]"
            else:
                return str(list(value))
        elif isinstance(value, np.ndarray):
            # 对于小数组，直接显示值；对于大数组，使用生成代码
            if value.size <= 10:
                return f"np.array({value.tolist()})"
            else:
                return f"data  # 形状: {value.shape}"
        elif isinstance(value, dict):
            items = [f"'{k}': {self._format_param_value(v)}" for k, v in value.items()]
            return "{" + ", ".join(items) + "}"
        elif isinstance(value, bool):
            return "True" if value else "False"
        elif isinstance(value, type(None)):
            return "None"
        else:
            return str(value)
    
    def _get_function_name(self) -> str:
        """获取函数名称"""
        if hasattr(self.plot_func, '__name__'):
            return self.plot_func.__name__
        # 尝试从函数签名推断
        try:
            sig = inspect.signature(self.plot_func)
            # 如果是包装函数，尝试获取原始函数名
            if hasattr(self.plot_func, '__wrapped__'):
                return self.plot_func.__wrapped__.__name__
        except:
            pass
        return 'plot'


class ChartRegistry:
    """图表类型注册表"""
    _registry: Dict[str, ChartType] = {}
    
    @classmethod
    def register(cls, chart_type: ChartType):
        """注册图表类型"""
        cls._registry[chart_type.name] = chart_type
    
    @classmethod
    def get(cls, name: str) -> Optional[ChartType]:
        """获取图表类型"""
        return cls._registry.get(name)
    
    @classmethod
    def list_by_category(cls, category: ChartCategory) -> List[ChartType]:
        """按类别列出图表类型"""
        return [ct for ct in cls._registry.values() if ct.category == category]
    
    @classmethod
    def list_all(cls) -> List[ChartType]:
        """列出所有图表类型"""
        return list(cls._registry.values())


class DataLoader:
    """数据加载器，支持多种数据格式"""
    
    @staticmethod
    def load_csv(file_content: Union[str, bytes, io.StringIO], **kwargs) -> pd.DataFrame:
        """加载 CSV 文件"""
        if isinstance(file_content, bytes):
            file_content = file_content.decode('utf-8')
        if isinstance(file_content, str):
            file_content = io.StringIO(file_content)
        return pd.read_csv(file_content, **kwargs)
    
    @staticmethod
    def load_json(file_content: Union[str, bytes, dict], **kwargs) -> pd.DataFrame:
        """加载 JSON 文件"""
        if isinstance(file_content, bytes):
            file_content = file_content.decode('utf-8')
        if isinstance(file_content, str):
            data = json.loads(file_content)
        else:
            data = file_content
        
        # 如果是列表，转换为 DataFrame
        if isinstance(data, list):
            return pd.DataFrame(data)
        # 如果是字典，尝试转换为 DataFrame
        elif isinstance(data, dict):
            return pd.DataFrame(data)
        else:
            raise ValueError("不支持的 JSON 格式")
    
    @staticmethod
    def load_excel(file_content: bytes, **kwargs) -> pd.DataFrame:
        """加载 Excel 文件"""
        return pd.read_excel(io.BytesIO(file_content), **kwargs)
    
    @staticmethod
    def load_data(file_content: Union[str, bytes, dict, io.StringIO], 
                  file_type: str = 'auto', **kwargs) -> pd.DataFrame:
        """
        自动检测并加载数据文件
        
        Args:
            file_content: 文件内容
            file_type: 文件类型 ('csv', 'json', 'excel', 'auto')
            **kwargs: 传递给 pandas 读取函数的参数
        
        Returns:
            pandas DataFrame
        """
        if file_type == 'auto':
            # 自动检测文件类型
            if isinstance(file_content, dict):
                file_type = 'json'
            elif isinstance(file_content, (str, io.StringIO)):
                # 尝试解析为 JSON
                try:
                    if isinstance(file_content, str):
                        json.loads(file_content)
                        file_type = 'json'
                    else:
                        file_type = 'csv'
                except:
                    file_type = 'csv'
            elif isinstance(file_content, bytes):
                # 检查是否是 Excel 文件
                if file_content[:2] == b'PK':  # Excel 文件以 PK 开头
                    file_type = 'excel'
                else:
                    file_type = 'csv'
            else:
                file_type = 'csv'
        
        if file_type == 'csv':
            return DataLoader.load_csv(file_content, **kwargs)
        elif file_type == 'json':
            return DataLoader.load_json(file_content, **kwargs)
        elif file_type == 'excel':
            return DataLoader.load_excel(file_content, **kwargs)
        else:
            raise ValueError(f"不支持的文件类型: {file_type}")


class PlotAPI:
    """统一的图表绘制 API"""
    
    def __init__(self, figsize: Tuple[float, float] = (8, 5)):
        """初始化绘图 API"""
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.charts: List[Dict[str, Any]] = []  # 存储已绘制的图表信息
        self.data: Dict[str, pd.DataFrame] = {}  # 存储上传的数据
    
    def plot(self, chart_type: str, **params) -> Any:
        """
        绘制图表
        
        Args:
            chart_type: 图表类型名称
            **params: 图表参数
        
        Returns:
            绘图函数的返回值
        """
        chart_def = ChartRegistry.get(chart_type)
        if chart_def is None:
            raise ValueError(f"未知的图表类型: {chart_type}")
        
        # 验证参数
        is_valid, error_msg, validated_params = chart_def.validate_params(params)
        if not is_valid:
            raise ValueError(f"参数验证失败: {error_msg}")
        
        # 生成示例数据（如果需要）
        if chart_def.data_generator:
            data = chart_def.data_generator(**validated_params)
            validated_params.update(data)
        
        # 转换 pandas Series 为 numpy array（如果需要）
        for key, value in validated_params.items():
            if isinstance(value, pd.Series):
                validated_params[key] = value.values
            elif isinstance(value, pd.DataFrame):
                validated_params[key] = value.values
        
        # 调用绘图函数
        try:
            result = chart_def.plot_func(self.ax, **validated_params)
            
            # 记录图表信息
            self.charts.append({
                'type': chart_type,
                'params': validated_params,
                'result': result
            })
            
            return result
        except Exception as e:
            raise RuntimeError(f"绘图失败: {str(e)}")
    
    def generate_code(self, include_imports: bool = True, include_setup: bool = True) -> str:
        """生成完整的代码"""
        lines = []
        
        if include_imports:
            lines.append("import matplotlib.pyplot as plt")
            lines.append("import numpy as np")
            lines.append("")
        
        if include_setup:
            lines.append("fig, ax = plt.subplots(figsize=(8, 5))")
            lines.append("")
        
        # 收集数据定义
        data_lines = []
        seen_data = set()
        
        # 为每个图表生成代码
        for chart_info in self.charts:
            chart_type = chart_info['type']
            params = chart_info['params']
            
            # 生成数据代码
            data_code = self._generate_data_code(chart_type, params)
            if data_code and data_code not in seen_data:
                data_lines.append(data_code)
                seen_data.add(data_code)
            
            chart_def = ChartRegistry.get(chart_type)
            if chart_def:
                code = chart_def.generate_code(params)
                lines.append(code)
        
        # 在 setup 之后插入数据定义
        if data_lines and include_setup:
            setup_idx = lines.index("fig, ax = plt.subplots(figsize=(8, 5))") + 2
            for data_line in reversed(data_lines):
                lines.insert(setup_idx, data_line)
            if data_lines:
                lines.insert(setup_idx, "")
        
        if include_setup:
            lines.append("")
            lines.append("ax.set_title('Chart', fontsize=14, fontweight='bold')")
            lines.append("ax.set_xlabel('X Axis', fontsize=12)")
            lines.append("ax.set_ylabel('Y Axis', fontsize=12)")
            lines.append("ax.grid(True, alpha=0.3)")
            lines.append("plt.show()")
        
        return "\n".join(lines)
    
    def _generate_data_code(self, chart_type: str, params: Dict[str, Any]) -> str:
        """生成数据定义代码"""
        if chart_type == "line":
            if 'x' not in params or 'y' not in params:
                return "x = np.linspace(0, 10, 50)\ny = np.sin(x)"
        elif chart_type == "bar":
            if 'x' not in params or 'height' not in params:
                return "categories = ['A', 'B', 'C', 'D', 'E']\nvalues = [23, 45, 56, 78, 32]"
        elif chart_type == "barh":
            if 'y' not in params or 'width' not in params:
                return "categories = ['A', 'B', 'C', 'D', 'E']\nvalues = [23, 45, 56, 78, 32]"
        elif chart_type == "hist":
            if 'data' not in params:
                return "data = np.random.randn(1000)"
        elif chart_type == "pie":
            if 'sizes' not in params or 'labels' not in params:
                return "labels = ['类别A', '类别B', '类别C', '类别D']\nsizes = [15, 30, 45, 10]"
        elif chart_type == "scatter":
            if 'x' not in params or 'y' not in params:
                return "n_points = 200\nx = np.random.rand(n_points)\ny = np.random.rand(n_points)"
        return ""
    
    def show(self):
        """显示图表"""
        return self.fig
    
    def save(self, filename: str, **kwargs):
        """保存图表"""
        self.fig.savefig(filename, **kwargs)
    
    def load_data(self, file_content: Union[str, bytes, dict, io.StringIO], 
                  name: str = 'data', file_type: str = 'auto', **kwargs) -> pd.DataFrame:
        """
        加载数据文件
        
        Args:
            file_content: 文件内容
            name: 数据名称（用于后续引用）
            file_type: 文件类型 ('csv', 'json', 'excel', 'auto')
            **kwargs: 传递给 pandas 读取函数的参数
        
        Returns:
            pandas DataFrame
        """
        df = DataLoader.load_data(file_content, file_type, **kwargs)
        self.data[name] = df
        return df
    
    def get_data(self, name: str = 'data') -> Optional[pd.DataFrame]:
        """获取已加载的数据"""
        return self.data.get(name)
    
    def list_data(self) -> List[str]:
        """列出所有已加载的数据名称"""
        return list(self.data.keys())
    
    def plot_from_data(self, chart_type: str, data_name: str = 'data', 
                      x_col: Optional[str] = None, y_col: Optional[str] = None,
                      **params) -> Any:
        """
        从已加载的数据绘制图表
        
        Args:
            chart_type: 图表类型
            data_name: 数据名称
            x_col: X 轴列名
            y_col: Y 轴列名
            **params: 其他图表参数
        
        Returns:
            绘图函数的返回值
        """
        if data_name not in self.data:
            raise ValueError(f"数据 '{data_name}' 不存在。请先使用 load_data() 加载数据。")
        
        df = self.data[data_name]
        
        # 根据图表类型自动提取数据
        if chart_type == 'line':
            if x_col is None:
                x_col = df.columns[0]
            if y_col is None:
                y_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
            params['x'] = df[x_col].values
            params['y'] = df[y_col].values
        elif chart_type == 'bar':
            if x_col is None:
                x_col = df.columns[0]
            if y_col is None:
                y_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
            params['x'] = df[x_col].values
            params['height'] = df[y_col].values
        elif chart_type == 'scatter':
            if x_col is None:
                x_col = df.columns[0]
            if y_col is None:
                y_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
            params['x'] = df[x_col].values
            params['y'] = df[y_col].values
        elif chart_type == 'hist':
            if y_col is None:
                y_col = df.columns[0]
            params['data'] = df[y_col].values
        elif chart_type == 'pie':
            if x_col is None:
                x_col = df.columns[0] if len(df.columns) > 1 else None
            if y_col is None:
                y_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
            if x_col:
                params['labels'] = df[x_col].values
            params['sizes'] = df[y_col].values
        
        return self.plot(chart_type, **params)


# ========== 图表类型定义和注册 ==========

def _register_line_charts():
    """注册线条类图表"""
    
    # Line Plot
    def plot_line(ax: matplotlib.axes.Axes, x=None, y=None, **kwargs):
        if x is None or y is None:
            x = np.linspace(0, 10, 50)
            y = np.sin(x)
        return ax.plot(x, y, **kwargs)
    
    ChartRegistry.register(ChartType(
        name="line",
        display_name="Line Plot (折线图)",
        category=ChartCategory.LINE,
        plot_func=plot_line,
        parameters={
            'x': ParameterDefinition('x', (list, tuple, np.ndarray, pd.Series), None, "X 轴数据"),
            'y': ParameterDefinition('y', (list, tuple, np.ndarray, pd.Series), None, "Y 轴数据"),
            'linestyle': ParameterDefinition('linestyle', (str, tuple), '-', "线型", 
                                            valid_values=['-', '--', '-.', ':', 'None', ' ', '']),
            'linewidth': ParameterDefinition('linewidth', (int, float), 1.5, "线宽"),
            'color': ParameterDefinition('color', str, '#2c3e50', "颜色"),
            'marker': ParameterDefinition('marker', str, None, "标记符号"),
            'markersize': ParameterDefinition('markersize', (int, float), 6, "标记大小"),
            'markeredgecolor': ParameterDefinition('markeredgecolor', str, None, "标记边缘颜色"),
            'markeredgewidth': ParameterDefinition('markeredgewidth', (int, float), 1, "标记边缘宽度"),
            'markerfacecolor': ParameterDefinition('markerfacecolor', str, None, "标记填充颜色"),
            'markerfacecoloralt': ParameterDefinition('markerfacecoloralt', str, None, "标记交替填充颜色"),
            'fillstyle': ParameterDefinition('fillstyle', str, 'full', "填充样式",
                                            valid_values=['full', 'left', 'right', 'bottom', 'top', 'none']),
            'alpha': ParameterDefinition('alpha', float, 1.0, "透明度", validator=lambda v: 0 <= v <= 1),
            'label': ParameterDefinition('label', str, None, "标签"),
            'drawstyle': ParameterDefinition('drawstyle', str, 'default', "绘制样式",
                                            valid_values=['default', 'steps', 'steps-pre', 'steps-mid', 'steps-post']),
            'solid_capstyle': ParameterDefinition('solid_capstyle', str, 'butt', "实线端点样式",
                                                 valid_values=['butt', 'round', 'projecting']),
            'solid_joinstyle': ParameterDefinition('solid_joinstyle', str, 'miter', "实线连接样式",
                                                  valid_values=['miter', 'round', 'bevel']),
            'dash_capstyle': ParameterDefinition('dash_capstyle', str, 'butt', "虚线端点样式",
                                                 valid_values=['butt', 'round', 'projecting']),
            'dash_joinstyle': ParameterDefinition('dash_joinstyle', str, 'miter', "虚线连接样式",
                                                 valid_values=['miter', 'round', 'bevel']),
            'dashes': ParameterDefinition('dashes', (tuple, list), None, "虚线样式（元组）"),
            'zorder': ParameterDefinition('zorder', (int, float), 2, "图层顺序"),
            'visible': ParameterDefinition('visible', bool, True, "是否可见"),
            'clip_on': ParameterDefinition('clip_on', bool, True, "是否裁剪"),
            'snap': ParameterDefinition('snap', bool, False, "是否对齐像素"),
            'animated': ParameterDefinition('animated', bool, False, "是否动画"),
            'antialiased': ParameterDefinition('antialiased', bool, True, "是否抗锯齿"),
            'rasterized': ParameterDefinition('rasterized', bool, False, "是否栅格化"),
            'markevery': ParameterDefinition('markevery', (int, float, tuple, list, np.ndarray), None, "标记间隔"),
        },
        description="绘制折线图，支持多种线型和标记样式"
    ))


def _register_patch_charts():
    """注册形状与统计图表"""
    
    # Bar Chart
    def plot_bar(ax: matplotlib.axes.Axes, x=None, height=None, **kwargs):
        if x is None:
            x = ['A', 'B', 'C', 'D', 'E']
        if height is None:
            height = [23, 45, 56, 78, 32]
        return ax.bar(x, height, **kwargs)
    
    ChartRegistry.register(ChartType(
        name="bar",
        display_name="Bar Chart (垂直条形图)",
        category=ChartCategory.PATCH,
        plot_func=plot_bar,
        parameters={
            'x': ParameterDefinition('x', (list, tuple, np.ndarray, pd.Series), None, "X 轴类别"),
            'height': ParameterDefinition('height', (list, tuple, np.ndarray, pd.Series), None, "条形高度"),
            'width': ParameterDefinition('width', (float, list, tuple, np.ndarray), 0.8, "条形宽度"),
            'bottom': ParameterDefinition('bottom', (float, list, tuple, np.ndarray), 0, "条形底部位置"),
            'align': ParameterDefinition('align', str, 'center', "对齐方式", valid_values=['center', 'edge']),
            'color': ParameterDefinition('color', (str, list, tuple, np.ndarray), '#3b82f6', "颜色"),
            'alpha': ParameterDefinition('alpha', float, 0.8, "透明度", validator=lambda v: 0 <= v <= 1),
            'edgecolor': ParameterDefinition('edgecolor', (str, list, tuple), None, "边框颜色"),
            'linewidth': ParameterDefinition('linewidth', (float, list, tuple), 1.0, "边框宽度"),
            'label': ParameterDefinition('label', str, None, "标签"),
            'tick_label': ParameterDefinition('tick_label', (list, tuple), None, "刻度标签"),
            'xerr': ParameterDefinition('xerr', (float, list, tuple, np.ndarray), None, "X 轴误差"),
            'yerr': ParameterDefinition('yerr', (float, list, tuple, np.ndarray), None, "Y 轴误差"),
            'ecolor': ParameterDefinition('ecolor', (str, list, tuple), None, "误差棒颜色"),
            'capsize': ParameterDefinition('capsize', float, 0, "误差棒端帽大小"),
            'error_kw': ParameterDefinition('error_kw', dict, None, "误差棒关键字参数"),
            'log': ParameterDefinition('log', bool, False, "是否使用对数刻度"),
            'orientation': ParameterDefinition('orientation', str, 'vertical', "方向", valid_values=['vertical', 'horizontal']),
            'zorder': ParameterDefinition('zorder', (int, float), 2, "图层顺序"),
        },
        description="绘制垂直条形图",
        code_template="ax.bar({x}, {height}, width={width}, color='{color}', alpha={alpha}{edgecode}{labelcode})"
    ))
    
    # Horizontal Bar Chart
    def plot_barh(ax: matplotlib.axes.Axes, y=None, width=None, **kwargs):
        if y is None:
            y = ['A', 'B', 'C', 'D', 'E']
        if width is None:
            width = [23, 45, 56, 78, 32]
        return ax.barh(y, width, **kwargs)
    
    ChartRegistry.register(ChartType(
        name="barh",
        display_name="Barh Chart (水平条形图)",
        category=ChartCategory.PATCH,
        plot_func=plot_barh,
        parameters={
            'y': ParameterDefinition('y', (list, tuple, np.ndarray), None, "Y 轴类别"),
            'width': ParameterDefinition('width', (list, tuple, np.ndarray), None, "条形宽度"),
            'height': ParameterDefinition('height', float, 0.8, "条形高度"),
            'color': ParameterDefinition('color', str, '#3b82f6', "颜色"),
            'alpha': ParameterDefinition('alpha', float, 0.8, "透明度", validator=lambda v: 0 <= v <= 1),
            'edgecolor': ParameterDefinition('edgecolor', str, None, "边框颜色"),
            'linewidth': ParameterDefinition('linewidth', float, 1.0, "边框宽度"),
            'label': ParameterDefinition('label', str, None, "标签"),
        },
        description="绘制水平条形图"
    ))
    
    # Histogram
    def plot_hist(ax: matplotlib.axes.Axes, data=None, **kwargs):
        if data is None:
            data = np.random.randn(1000)
        return ax.hist(data, **kwargs)
    
    ChartRegistry.register(ChartType(
        name="hist",
        display_name="Histogram (直方图)",
        category=ChartCategory.PATCH,
        plot_func=plot_hist,
        parameters={
            'data': ParameterDefinition('data', (list, tuple, np.ndarray, pd.Series), None, "数据"),
            'bins': ParameterDefinition('bins', (int, list, tuple, str), 10, "分组数或分组边界"),
            'range': ParameterDefinition('range', (tuple, list), None, "数据范围 (min, max)"),
            'density': ParameterDefinition('density', bool, False, "是否归一化为密度"),
            'weights': ParameterDefinition('weights', (list, tuple, np.ndarray), None, "权重"),
            'cumulative': ParameterDefinition('cumulative', (bool, int, str), False, "是否累积"),
            'bottom': ParameterDefinition('bottom', (float, list, tuple, np.ndarray), None, "底部位置"),
            'histtype': ParameterDefinition('histtype', str, 'bar', "直方图类型",
                                           valid_values=['bar', 'barstacked', 'step', 'stepfilled']),
            'align': ParameterDefinition('align', str, 'mid', "对齐方式", valid_values=['left', 'mid', 'right']),
            'orientation': ParameterDefinition('orientation', str, 'vertical', "方向", valid_values=['vertical', 'horizontal']),
            'rwidth': ParameterDefinition('rwidth', float, None, "相对宽度"),
            'color': ParameterDefinition('color', (str, list, tuple), '#3b82f6', "颜色"),
            'alpha': ParameterDefinition('alpha', float, 0.8, "透明度", validator=lambda v: 0 <= v <= 1),
            'edgecolor': ParameterDefinition('edgecolor', (str, list, tuple), None, "边框颜色"),
            'linewidth': ParameterDefinition('linewidth', (float, list, tuple), 1.0, "边框宽度"),
            'label': ParameterDefinition('label', str, None, "标签"),
            'stacked': ParameterDefinition('stacked', bool, False, "是否堆叠"),
            'zorder': ParameterDefinition('zorder', (int, float), 2, "图层顺序"),
        },
        description="绘制直方图"
    ))
    
    # Pie Chart
    def plot_pie(ax: matplotlib.axes.Axes, sizes=None, labels=None, **kwargs):
        if sizes is None:
            sizes = [15, 30, 45, 10]
        if labels is None:
            labels = ['类别A', '类别B', '类别C', '类别D']
        return ax.pie(sizes, labels=labels, **kwargs)
    
    ChartRegistry.register(ChartType(
        name="pie",
        display_name="Pie Chart (饼图)",
        category=ChartCategory.PATCH,
        plot_func=plot_pie,
        parameters={
            'sizes': ParameterDefinition('sizes', (list, tuple, np.ndarray, pd.Series), None, "扇形大小"),
            'labels': ParameterDefinition('labels', (list, tuple), None, "标签"),
            'colors': ParameterDefinition('colors', (list, tuple, np.ndarray), None, "颜色列表"),
            'explode': ParameterDefinition('explode', (list, tuple, np.ndarray), None, "突出显示"),
            'autopct': ParameterDefinition('autopct', (str, Callable), '%1.1f%%', "百分比格式"),
            'pctdistance': ParameterDefinition('pctdistance', float, 0.6, "百分比标签距离"),
            'shadow': ParameterDefinition('shadow', bool, False, "阴影"),
            'labeldistance': ParameterDefinition('labeldistance', float, 1.1, "标签距离"),
            'startangle': ParameterDefinition('startangle', float, 0, "起始角度"),
            'radius': ParameterDefinition('radius', float, 1, "半径"),
            'counterclock': ParameterDefinition('counterclock', bool, True, "是否逆时针"),
            'wedgeprops': ParameterDefinition('wedgeprops', dict, None, "扇形属性"),
            'textprops': ParameterDefinition('textprops', dict, None, "文本属性"),
            'center': ParameterDefinition('center', (tuple, list), (0, 0), "中心位置"),
            'frame': ParameterDefinition('frame', bool, False, "是否显示框架"),
            'rotatelabels': ParameterDefinition('rotatelabels', bool, False, "是否旋转标签"),
            'normalize': ParameterDefinition('normalize', bool, True, "是否归一化"),
        },
        description="绘制饼图"
    ))
    
    # Box Plot
    def plot_box(ax: matplotlib.axes.Axes, data=None, **kwargs):
        if data is None:
            data = [np.random.normal(0, std, 100) for std in range(1, 5)]
        return ax.boxplot(data, **kwargs)
    
    ChartRegistry.register(ChartType(
        name="box",
        display_name="Box Plot (箱线图)",
        category=ChartCategory.PATCH,
        plot_func=plot_box,
        parameters={
            'data': ParameterDefinition('data', (list, tuple), None, "数据列表（每个元素是一个数据组）"),
            'labels': ParameterDefinition('labels', (list, tuple), None, "标签列表"),
            'patch_artist': ParameterDefinition('patch_artist', bool, True, "是否使用 Patch 对象"),
            'notch': ParameterDefinition('notch', bool, False, "是否显示缺口"),
            'showmeans': ParameterDefinition('showmeans', bool, False, "是否显示均值"),
        },
        description="绘制箱线图"
    ))
    
    # Errorbar
    def plot_errorbar(ax: matplotlib.axes.Axes, x=None, y=None, yerr=None, xerr=None, **kwargs):
        if x is None:
            x = np.arange(1, 6)
        if y is None:
            y = [2, 3, 4, 3, 2]
        if yerr is None:
            yerr = [0.3, 0.4, 0.5, 0.4, 0.3]
        if xerr is None:
            xerr = [0.1, 0.1, 0.1, 0.1, 0.1]
        return ax.errorbar(x, y, yerr=yerr, xerr=xerr, **kwargs)
    
    ChartRegistry.register(ChartType(
        name="errorbar",
        display_name="Errorbar (误差棒图)",
        category=ChartCategory.PATCH,
        plot_func=plot_errorbar,
        parameters={
            'x': ParameterDefinition('x', (list, tuple, np.ndarray), None, "X 轴数据"),
            'y': ParameterDefinition('y', (list, tuple, np.ndarray), None, "Y 轴数据"),
            'yerr': ParameterDefinition('yerr', (list, tuple, np.ndarray, float), None, "Y 轴误差"),
            'xerr': ParameterDefinition('xerr', (list, tuple, np.ndarray, float), None, "X 轴误差"),
            'fmt': ParameterDefinition('fmt', str, 'o', "标记格式"),
            'color': ParameterDefinition('color', str, '#3b82f6', "颜色"),
            'alpha': ParameterDefinition('alpha', float, 0.8, "透明度", validator=lambda v: 0 <= v <= 1),
            'capsize': ParameterDefinition('capsize', float, 5, "误差棒端帽大小"),
            'capthick': ParameterDefinition('capthick', float, 2, "误差棒端帽厚度"),
            'elinewidth': ParameterDefinition('elinewidth', float, 1.5, "误差棒线宽"),
        },
        description="绘制误差棒图"
    ))
    
    # Fill Between
    def plot_fill_between(ax: matplotlib.axes.Axes, x=None, y1=None, y2=None, **kwargs):
        if x is None:
            x = np.linspace(0, 10, 100)
        if y1 is None:
            y1 = np.sin(x)
        if y2 is None:
            y2 = np.cos(x)
        return ax.fill_between(x, y1, y2, **kwargs)
    
    ChartRegistry.register(ChartType(
        name="fill_between",
        display_name="Fill Between (填充区域)",
        category=ChartCategory.PATCH,
        plot_func=plot_fill_between,
        parameters={
            'x': ParameterDefinition('x', (list, tuple, np.ndarray), None, "X 轴数据"),
            'y1': ParameterDefinition('y1', (list, tuple, np.ndarray), None, "第一条曲线"),
            'y2': ParameterDefinition('y2', (list, tuple, np.ndarray), None, "第二条曲线"),
            'where': ParameterDefinition('where', (list, tuple, np.ndarray, bool), None, "填充条件"),
            'color': ParameterDefinition('color', str, '#3b82f6', "填充颜色"),
            'alpha': ParameterDefinition('alpha', float, 0.5, "透明度", validator=lambda v: 0 <= v <= 1),
            'label': ParameterDefinition('label', str, None, "标签"),
        },
        description="填充两条曲线之间的区域"
    ))


def _register_collection_charts():
    """注册集合类图表"""
    
    # Scatter Plot
    def plot_scatter(ax: matplotlib.axes.Axes, x=None, y=None, **kwargs):
        if x is None or y is None:
            n = kwargs.get('n_points', 200)
            x = np.random.rand(n)
            y = np.random.rand(n)
        return ax.scatter(x, y, **kwargs)
    
    ChartRegistry.register(ChartType(
        name="scatter",
        display_name="Scatter Plot (散点图)",
        category=ChartCategory.COLLECTION,
        plot_func=plot_scatter,
        parameters={
            'x': ParameterDefinition('x', (list, tuple, np.ndarray, pd.Series), None, "X 轴数据"),
            'y': ParameterDefinition('y', (list, tuple, np.ndarray, pd.Series), None, "Y 轴数据"),
            's': ParameterDefinition('s', (int, float, list, tuple, np.ndarray, pd.Series), 20, "点的大小"),
            'c': ParameterDefinition('c', (str, list, tuple, np.ndarray, pd.Series), None, "颜色"),
            'marker': ParameterDefinition('marker', str, 'o', "标记符号"),
            'cmap': ParameterDefinition('cmap', str, None, "颜色映射"),
            'norm': ParameterDefinition('norm', Any, None, "归一化对象"),
            'vmin': ParameterDefinition('vmin', float, None, "颜色映射最小值"),
            'vmax': ParameterDefinition('vmax', float, None, "颜色映射最大值"),
            'alpha': ParameterDefinition('alpha', (float, list, tuple, np.ndarray), 0.5, "透明度", validator=lambda v: (isinstance(v, (int, float)) and 0 <= v <= 1) or True),
            'edgecolors': ParameterDefinition('edgecolors', (str, list, tuple, np.ndarray), None, "边缘颜色"),
            'linewidths': ParameterDefinition('linewidths', (float, list, tuple, np.ndarray), 1.5, "边缘线宽"),
            'label': ParameterDefinition('label', str, None, "标签"),
            'zorder': ParameterDefinition('zorder', (int, float), 2, "图层顺序"),
            'visible': ParameterDefinition('visible', bool, True, "是否可见"),
            'clip_on': ParameterDefinition('clip_on', bool, True, "是否裁剪"),
        },
        description="绘制散点图"
    ))


# 初始化注册
_register_line_charts()
_register_patch_charts()
_register_collection_charts()


# ========== 便捷函数 ==========

def create_plot(figsize: Tuple[float, float] = (8, 5)) -> PlotAPI:
    """创建绘图 API 实例"""
    return PlotAPI(figsize=figsize)


def get_chart_types(category: Optional[ChartCategory] = None) -> List[ChartType]:
    """获取图表类型列表"""
    if category:
        return ChartRegistry.list_by_category(category)
    return ChartRegistry.list_all()


def get_chart_info(chart_type: str) -> Optional[ChartType]:
    """获取图表类型信息"""
    return ChartRegistry.get(chart_type)


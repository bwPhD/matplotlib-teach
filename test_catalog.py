"""
测试脚本：验证 catalog 模块是否正常工作
"""
import sys
import matplotlib
print(f"Matplotlib version: {matplotlib.__version__}")

# 测试导入
try:
    from catalogs.line import (
        get_linestyle_options,
        get_drawstyle_options,
        get_capstyle_options,
        get_joinstyle_options
    )
    print("✅ 成功导入 catalog.line 模块")
except Exception as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)

# 测试函数调用
try:
    linestyles = get_linestyle_options()
    print(f"✅ linestyle 选项: {len(linestyles['string_styles'])} 个字符串样式")
    
    drawstyles = get_drawstyle_options()
    print(f"✅ drawstyle 选项: {len(drawstyles)} 个")
    
    capstyles = get_capstyle_options()
    print(f"✅ capstyle 选项: {capstyles}")
    
    joinstyles = get_joinstyle_options()
    print(f"✅ joinstyle 选项: {joinstyles}")
    
    print("\n✅ 所有测试通过！")
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


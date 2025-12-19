"""
测试脚本：验证 marker catalog 模块是否正常工作
"""
import sys
import matplotlib
print(f"Matplotlib version: {matplotlib.__version__}")

# 测试导入
try:
    from catalogs.marker import (
        get_marker_options,
        get_fillstyle_options,
        render_catalog_page
    )
    print("✅ 成功导入 catalog.marker 模块")
except Exception as e:
    print(f"❌ 导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试函数调用
try:
    marker_options = get_marker_options()
    print(f"✅ marker 选项: {len(marker_options['all_markers'])} 个标记")
    print(f"   分类数量: {len([k for k, v in marker_options['categories'].items() if v])} 个类别")
    
    fillstyles = get_fillstyle_options()
    print(f"✅ fillstyle 选项: {len(fillstyles)} 个")
    print(f"   选项: {fillstyles}")
    
    print("\n✅ 所有测试通过！")
    print("\n📝 注意：render_catalog_page() 需要在 Streamlit 环境中运行")
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


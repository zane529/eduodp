#!/usr/bin/env python3
"""
快速PDF生成器 - 使用Pandoc生成ODP_Demo完整指南
"""

import os
import subprocess
from pathlib import Path

def generate_pdf():
    """生成PDF电子书"""
    
    print("📚 ODP_Demo 完整指南 PDF生成器")
    print("=" * 40)
    
    # 文档列表（按逻辑顺序）
    docs = [
        # 项目概述
        ("README.md", "项目介绍"),
        
        # 基础功能
        ("docs/00_Demo_Features_地图创建功能详解.md", "地图创建功能详解"),
        ("docs/00_Demo_Features_数据可视化功能详解.md", "数据可视化功能详解"),
        ("docs/01_ODP_Search_使用手册.md", "数据搜索功能"),
        ("docs/02_Inspector_Tool_使用手册.md", "数据检查工具"),
        
        # 数据源集成
        ("docs/03A_Maxar_Open_Data_使用手册.md", "Maxar开放数据"),
        ("docs/03B_Planet_使用手册.md", "Planet卫星数据"),
        ("docs/04_Open_Aerial_Map_使用手册.md", "开放航空地图"),
        ("docs/0A_CSV_OSM_使用手册.md", "CSV与OSM处理"),
        ("docs/0B_Basemap_使用手册.md", "底图管理"),
        
        # 高级分析
        ("docs/05_Timelapse_使用手册.md", "时间序列分析"),
        ("docs/06_Turkey_Earthquake_使用手册.md", "地震案例分析"),
        
        # AI功能
        ("docs/07_SAM_AutoMask_使用手册.md", "SAM自动掩膜"),
        ("docs/08_SAM_AutoMask_Refined_使用手册.md", "SAM精化版"),
        ("docs/09_Agricultural_SAM_使用手册.md", "农业SAM应用"),
        
        # 文本提示
        ("docs/10_Input_Prompts_Refined_使用手册.md", "输入提示优化"),
        ("docs/11_Text_Prompts_使用手册.md", "文本提示处理"),
        ("docs/12_Text_Prompts_Batch_使用手册.md", "批量文本提示"),
        ("docs/13_Text_Prompts_Swimming_Pools_使用手册.md", "游泳池检测"),
    ]
    
    # 检查存在的文档
    existing_docs = []
    for doc_path, title in docs:
        if os.path.exists(doc_path):
            existing_docs.append(doc_path)
            print(f"✅ {title}")
        else:
            print(f"❌ {title} (文件不存在: {doc_path})")
    
    print(f"\n📊 找到 {len(existing_docs)} 个文档文件")
    
    if len(existing_docs) == 0:
        print("❌ 没有找到任何文档文件")
        return False
    
    # 检查Pandoc
    try:
        result = subprocess.run(['pandoc', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Pandoc已安装: {result.stdout.split()[1]}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Pandoc未安装")
        print("安装方法:")
        print("  macOS: brew install pandoc")
        print("  Ubuntu: sudo apt install pandoc")
        print("  Windows: 从 https://pandoc.org/installing.html 下载")
        return False
    
    # 生成PDF
    output_file = "ODP_Demo_完整指南.pdf"
    
    print(f"\n🚀 开始生成PDF: {output_file}")
    
    cmd = [
        'pandoc',
        '--pdf-engine=xelatex',
        '--toc',                    # 生成目录
        '--toc-depth=3',           # 目录深度
        '--number-sections',        # 章节编号
        '--highlight-style=github', # 代码高亮
        '--geometry=margin=2.5cm',  # 页边距
        '--fontsize=11pt',         # 字体大小
        '--documentclass=book',     # 文档类型
        '--papersize=a4',          # 纸张大小
        '--metadata', f'title=ODP_Demo 地理科学解决方案包完整指南',
        '--metadata', f'author=ODP_Demo Team',
        '--metadata', f'date={subprocess.check_output(["date", "+%Y-%m-%d"]).decode().strip()}',
        '-o', output_file
    ] + existing_docs
    
    try:
        subprocess.run(cmd, check=True)
        
        # 检查生成的文件
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
            print(f"✅ PDF生成成功!")
            print(f"📄 文件: {output_file}")
            print(f"📊 大小: {file_size:.1f} MB")
            print(f"📖 页数: 约 {len(existing_docs) * 10} 页")
            return True
        else:
            print("❌ PDF文件未生成")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ PDF生成失败: {e}")
        print("\n可能的解决方案:")
        print("1. 安装中文字体支持: sudo apt install fonts-wqy-zenhei")
        print("2. 安装LaTeX: sudo apt install texlive-xetex")
        print("3. 检查文档中的特殊字符")
        return False

if __name__ == "__main__":
    success = generate_pdf()
    
    if success:
        print("\n🎉 完成! 您现在有了一个完整的PDF电子书")
        print("💡 提示: 可以使用PDF阅读器的书签功能快速导航")
    else:
        print("\n😞 生成失败，请检查上述错误信息")

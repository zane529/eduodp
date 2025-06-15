#!/usr/bin/env python3
"""
简化版PDF生成器 - 兼容新版Pandoc
"""

import os
import subprocess
from pathlib import Path

def generate_pdf():
    """生成PDF电子书"""
    
    print("📚 ODP_Demo 完整指南 PDF生成器 (简化版)")
    print("=" * 45)
    
    # 文档列表（按逻辑顺序）
    docs = [
        # 项目概述
        ("README.md", "项目介绍"),
        
        # 基础功能 - 详细分析级别
        ("docs/00_Demo_Features_地图创建功能详解.md", "地图创建功能详解"),
        ("docs/00_Demo_Features_数据可视化功能详解.md", "数据可视化功能详解"),
        ("docs/01_ODP_Search_使用手册.md", "数据搜索功能"),
        ("docs/02_Inspector_Tool_使用手册.md", "数据检查工具"),
        
        # AI功能 - 详细分析级别
        ("docs/07_SAM_AutoMask_使用手册.md", "SAM自动掩膜"),
        ("docs/11_Text_Prompts_使用手册.md", "文本提示处理"),
        
        # 其他功能
        ("docs/03A_Maxar_Open_Data_使用手册.md", "Maxar开放数据"),
        ("docs/03B_Planet_使用手册.md", "Planet卫星数据"),
        ("docs/04_Open_Aerial_Map_使用手册.md", "开放航空地图"),
        ("docs/0A_CSV_OSM_使用手册.md", "CSV与OSM处理"),
        ("docs/0B_Basemap_使用手册.md", "底图管理"),
        ("docs/05_Timelapse_使用手册.md", "时间序列分析"),
        ("docs/06_Turkey_Earthquake_使用手册.md", "地震案例分析"),
        ("docs/08_SAM_AutoMask_Refined_使用手册.md", "SAM精化版"),
        ("docs/09_Agricultural_SAM_使用手册.md", "农业SAM应用"),
        ("docs/10_Input_Prompts_Refined_使用手册.md", "输入提示优化"),
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
            print(f"❌ {title} (文件不存在)")
    
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
        return False
    
    # 生成PDF - 使用简化的参数
    output_file = "ODP_Demo_完整指南.pdf"
    
    print(f"\n🚀 开始生成PDF: {output_file}")
    
    # 简化的命令，兼容性更好
    cmd = [
        'pandoc',
        '--toc',                    # 生成目录
        '--number-sections',        # 章节编号
        '--highlight-style=github', # 代码高亮
        '-V', 'geometry:margin=2.5cm',  # 页边距
        '-V', 'fontsize=11pt',         # 字体大小
        '-V', 'documentclass=article', # 文档类型
        '-V', 'papersize=a4',          # 纸张大小
        '--metadata', f'title=ODP_Demo 地理科学解决方案包完整指南',
        '--metadata', f'author=ODP_Demo Team',
        '--metadata', f'date=2025-06-14',
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
            print(f"📖 包含: {len(existing_docs)} 个章节")
            return True
        else:
            print("❌ PDF文件未生成")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ PDF生成失败: {e}")
        
        # 尝试更简单的命令
        print("\n🔄 尝试基础版本...")
        simple_cmd = [
            'pandoc',
            '--toc',
            '-o', output_file
        ] + existing_docs
        
        try:
            subprocess.run(simple_cmd, check=True)
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file) / (1024 * 1024)
                print(f"✅ 基础PDF生成成功!")
                print(f"📄 文件: {output_file}")
                print(f"📊 大小: {file_size:.1f} MB")
                return True
        except subprocess.CalledProcessError as e2:
            print(f"❌ 基础版本也失败: {e2}")
            return False

if __name__ == "__main__":
    success = generate_pdf()
    
    if success:
        print("\n🎉 完成! 您现在有了一个完整的PDF电子书")
        print("💡 提示: 使用PDF阅读器打开，可以通过目录快速导航")
        print("📱 建议: 可以传输到平板或电子书阅读器上阅读")
    else:
        print("\n😞 生成失败")
        print("💡 建议: 尝试安装 texlive-latex-base 包")

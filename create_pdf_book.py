#!/usr/bin/env python3
"""
ODP_Demo文档PDF电子书生成工具
支持多种生成方式：GitBook、Pandoc、WeasyPrint
"""

import os
import subprocess
import json
from pathlib import Path

def create_gitbook_config():
    """创建GitBook配置文件"""
    
    book_json = {
        "title": "ODP_Demo 地理科学解决方案包完整指南",
        "description": "基于AWS开放数据的地理空间AI分析平台完整使用手册",
        "author": "ODP_Demo Team",
        "language": "zh-hans",
        "gitbook": "3.2.3",
        "plugins": [
            "theme-comscore",
            "anchors",
            "expandable-chapters",
            "page-toc-button",
            "back-to-top-button",
            "chapter-fold",
            "code",
            "splitter",
            "search-pro",
            "-search",
            "-lunr"
        ],
        "pluginsConfig": {
            "theme-comscore": {
                "color": "#2196F3"
            },
            "page-toc-button": {
                "maxTocDepth": 2,
                "minTocSize": 2
            }
        },
        "pdf": {
            "pageNumbers": True,
            "fontSize": 12,
            "fontFamily": "Arial",
            "paperSize": "a4",
            "chapterMark": "pagebreak",
            "pageBreaksBefore": "/",
            "margin": {
                "right": 62,
                "left": 62,
                "top": 56,
                "bottom": 56
            }
        }
    }
    
    with open('docs/book.json', 'w', encoding='utf-8') as f:
        json.dump(book_json, f, indent=2, ensure_ascii=False)
    
    print("✅ GitBook配置文件已创建")

def generate_gitbook_pdf():
    """使用GitBook生成PDF"""
    
    print("🚀 开始使用GitBook生成PDF...")
    
    # 检查GitBook是否安装
    try:
        subprocess.run(['gitbook', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ GitBook未安装，请先安装：")
        print("npm install -g gitbook-cli")
        print("gitbook install")
        return False
    
    # 切换到docs目录
    os.chdir('docs')
    
    try:
        # 安装插件
        print("📦 安装GitBook插件...")
        subprocess.run(['gitbook', 'install'], check=True)
        
        # 生成PDF
        print("📖 生成PDF电子书...")
        subprocess.run([
            'gitbook', 'pdf', '.', 
            '../ODP_Demo_完整指南.pdf'
        ], check=True)
        
        print("✅ PDF电子书生成成功：ODP_Demo_完整指南.pdf")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ GitBook生成失败：{e}")
        return False
    finally:
        os.chdir('..')

def generate_pandoc_pdf():
    """使用Pandoc生成PDF"""
    
    print("🚀 开始使用Pandoc生成PDF...")
    
    # 检查Pandoc是否安装
    try:
        subprocess.run(['pandoc', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Pandoc未安装，请先安装：")
        print("macOS: brew install pandoc")
        print("Ubuntu: sudo apt install pandoc")
        return False
    
    # 文档顺序
    doc_order = [
        'docs/README.md',
        'docs/00_Demo_Features_地图创建功能详解.md',
        'docs/00_Demo_Features_数据可视化功能详解.md',
        'docs/01_ODP_Search_使用手册.md',
        'docs/02_Inspector_Tool_使用手册.md',
        'docs/03A_Maxar_Open_Data_使用手册.md',
        'docs/03B_Planet_使用手册.md',
        'docs/04_Open_Aerial_Map_使用手册.md',
        'docs/0A_CSV_OSM_使用手册.md',
        'docs/0B_Basemap_使用手册.md',
        'docs/05_Timelapse_使用手册.md',
        'docs/06_Turkey_Earthquake_使用手册.md',
        'docs/07_SAM_AutoMask_使用手册.md',
        'docs/08_SAM_AutoMask_Refined_使用手册.md',
        'docs/09_Agricultural_SAM_使用手册.md',
        'docs/10_Input_Prompts_Refined_使用手册.md',
        'docs/11_Text_Prompts_使用手册.md',
        'docs/12_Text_Prompts_Batch_使用手册.md',
        'docs/13_Text_Prompts_Swimming_Pools_使用手册.md'
    ]
    
    # 检查文件是否存在
    existing_docs = [doc for doc in doc_order if os.path.exists(doc)]
    
    try:
        # 生成PDF
        cmd = [
            'pandoc',
            '--pdf-engine=xelatex',
            '--toc',
            '--toc-depth=3',
            '--number-sections',
            '--highlight-style=github',
            '--geometry=margin=2cm',
            '--mainfont=SimSun',  # 中文字体
            '--sansfont=SimHei',
            '--monofont=Monaco',
            '-V', 'documentclass=book',
            '-V', 'papersize=a4',
            '-V', 'fontsize=11pt',
            '--metadata', 'title=ODP_Demo 地理科学解决方案包完整指南',
            '--metadata', 'author=ODP_Demo Team',
            '--metadata', 'date=' + str(subprocess.check_output(['date', '+%Y-%m-%d']).decode().strip()),
            '-o', 'ODP_Demo_完整指南_Pandoc.pdf'
        ] + existing_docs
        
        subprocess.run(cmd, check=True)
        print("✅ Pandoc PDF生成成功：ODP_Demo_完整指南_Pandoc.pdf")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Pandoc生成失败：{e}")
        return False

def generate_weasyprint_pdf():
    """使用WeasyPrint生成PDF（HTML转PDF）"""
    
    print("🚀 开始使用WeasyPrint生成PDF...")
    
    try:
        import weasyprint
        import markdown
        from markdown.extensions import toc, codehilite, tables
    except ImportError:
        print("❌ 缺少依赖，请安装：")
        print("pip install weasyprint markdown")
        return False
    
    # 创建HTML内容
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>ODP_Demo 地理科学解决方案包完整指南</title>
        <style>
            body { 
                font-family: 'SimSun', serif; 
                line-height: 1.6; 
                margin: 2cm;
                font-size: 11pt;
            }
            h1 { 
                color: #2196F3; 
                border-bottom: 2px solid #2196F3; 
                padding-bottom: 10px;
                page-break-before: always;
            }
            h2 { 
                color: #1976D2; 
                margin-top: 2em;
            }
            h3 { 
                color: #1565C0; 
            }
            code { 
                background-color: #f5f5f5; 
                padding: 2px 4px; 
                border-radius: 3px;
                font-family: 'Monaco', monospace;
            }
            pre { 
                background-color: #f8f8f8; 
                padding: 15px; 
                border-radius: 5px; 
                overflow-x: auto;
                font-family: 'Monaco', monospace;
            }
            .toc {
                background-color: #f9f9f9;
                padding: 20px;
                border-radius: 5px;
                margin-bottom: 30px;
            }
            @page {
                margin: 2cm;
                @bottom-right {
                    content: counter(page);
                }
            }
        </style>
    </head>
    <body>
        <h1>ODP_Demo 地理科学解决方案包完整指南</h1>
        <div class="toc">
            <h2>目录</h2>
            <!-- 目录将自动生成 -->
        </div>
    """
    
    # 文档顺序
    doc_files = [
        'docs/README.md',
        'docs/00_Demo_Features_地图创建功能详解.md',
        'docs/00_Demo_Features_数据可视化功能详解.md',
        'docs/01_ODP_Search_使用手册.md',
        'docs/02_Inspector_Tool_使用手册.md',
        'docs/07_SAM_AutoMask_使用手册.md',
        'docs/11_Text_Prompts_使用手册.md',
        # 可以添加更多文档
    ]
    
    # 转换Markdown到HTML
    md = markdown.Markdown(extensions=['toc', 'codehilite', 'tables', 'fenced_code'])
    
    for doc_file in doc_files:
        if os.path.exists(doc_file):
            with open(doc_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            html_content += md.convert(content)
            html_content += '<div style="page-break-after: always;"></div>'
    
    html_content += """
    </body>
    </html>
    """
    
    try:
        # 生成PDF
        weasyprint.HTML(string=html_content).write_pdf('ODP_Demo_完整指南_WeasyPrint.pdf')
        print("✅ WeasyPrint PDF生成成功：ODP_Demo_完整指南_WeasyPrint.pdf")
        return True
        
    except Exception as e:
        print(f"❌ WeasyPrint生成失败：{e}")
        return False

def main():
    """主函数"""
    
    print("📚 ODP_Demo PDF电子书生成工具")
    print("=" * 50)
    
    # 创建GitBook配置
    create_gitbook_config()
    
    print("\n请选择生成方式：")
    print("1. GitBook (推荐 - 最佳排版)")
    print("2. Pandoc (快速 - 需要LaTeX)")
    print("3. WeasyPrint (简单 - HTML转PDF)")
    print("4. 全部生成")
    
    choice = input("\n请输入选择 (1-4): ").strip()
    
    success_count = 0
    
    if choice in ['1', '4']:
        if generate_gitbook_pdf():
            success_count += 1
    
    if choice in ['2', '4']:
        if generate_pandoc_pdf():
            success_count += 1
    
    if choice in ['3', '4']:
        if generate_weasyprint_pdf():
            success_count += 1
    
    print(f"\n🎉 完成！成功生成 {success_count} 个PDF文件")
    
    if success_count > 0:
        print("\n📖 生成的PDF文件：")
        pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf') and 'ODP_Demo' in f]
        for pdf_file in pdf_files:
            file_size = os.path.getsize(pdf_file) / (1024 * 1024)  # MB
            print(f"  - {pdf_file} ({file_size:.1f} MB)")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
电子书生成器 - 生成HTML和PDF版本
"""

import os
import subprocess
from pathlib import Path

def generate_html_book():
    """生成HTML电子书"""
    
    print("📚 生成HTML电子书...")
    
    # 完整文档列表
    docs = [
        "README.md",
        "docs/00_Demo_Features_地图创建功能详解.md",
        "docs/00_Demo_Features_数据可视化功能详解.md", 
        "docs/01_ODP_Search_使用手册.md",
        "docs/02_Inspector_Tool_使用手册.md",
        "docs/07_SAM_AutoMask_使用手册.md",
        "docs/11_Text_Prompts_使用手册.md",
        "docs/03A_Maxar_Open_Data_使用手册.md",
        "docs/03B_Planet_使用手册.md",
        "docs/04_Open_Aerial_Map_使用手册.md",
        "docs/0A_CSV_OSM_使用手册.md",
        "docs/0B_Basemap_使用手册.md",
        "docs/05_Timelapse_使用手册.md",
        "docs/06_Turkey_Earthquake_使用手册.md",
        "docs/08_SAM_AutoMask_Refined_使用手册.md",
        "docs/09_Agricultural_SAM_使用手册.md",
        "docs/10_Input_Prompts_Refined_使用手册.md",
        "docs/12_Text_Prompts_Batch_使用手册.md",
        "docs/13_Text_Prompts_Swimming_Pools_使用手册.md"
    ]
    
    # 检查存在的文档
    existing_docs = [doc for doc in docs if os.path.exists(doc)]
    print(f"📊 找到 {len(existing_docs)} 个文档")
    
    # 生成HTML
    cmd = [
        'pandoc',
        '--toc',
        '--toc-depth=3',
        '--standalone',
        '--embed-resources',
        '--css=https://cdn.jsdelivr.net/npm/github-markdown-css@5.2.0/github-markdown-light.css',
        '--metadata', 'title=ODP_Demo 地理科学解决方案包完整指南',
        '--metadata', 'author=ODP_Demo Team',
        '--metadata', 'date=2025-06-14',
        '-o', 'ODP_Demo_完整指南.html'
    ] + existing_docs
    
    try:
        subprocess.run(cmd, check=True)
        
        if os.path.exists('ODP_Demo_完整指南.html'):
            file_size = os.path.getsize('ODP_Demo_完整指南.html') / (1024 * 1024)
            print(f"✅ HTML电子书生成成功!")
            print(f"📄 文件: ODP_Demo_完整指南.html")
            print(f"📊 大小: {file_size:.1f} MB")
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ HTML生成失败: {e}")
        return False

def html_to_pdf():
    """将HTML转换为PDF"""
    
    print("\n📖 尝试将HTML转换为PDF...")
    
    html_file = 'ODP_Demo_完整指南.html'
    pdf_file = 'ODP_Demo_完整指南.pdf'
    
    if not os.path.exists(html_file):
        print("❌ HTML文件不存在")
        return False
    
    # 方法1: 使用wkhtmltopdf
    try:
        cmd = [
            'wkhtmltopdf',
            '--page-size', 'A4',
            '--margin-top', '20mm',
            '--margin-bottom', '20mm', 
            '--margin-left', '20mm',
            '--margin-right', '20mm',
            '--enable-local-file-access',
            '--print-media-type',
            html_file,
            pdf_file
        ]
        
        subprocess.run(cmd, check=True)
        
        if os.path.exists(pdf_file):
            file_size = os.path.getsize(pdf_file) / (1024 * 1024)
            print(f"✅ PDF转换成功!")
            print(f"📄 文件: {pdf_file}")
            print(f"📊 大小: {file_size:.1f} MB")
            return True
            
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ wkhtmltopdf未安装或转换失败")
    
    # 方法2: 使用Chrome/Chromium headless
    try:
        chrome_commands = [
            'google-chrome',
            'chromium-browser', 
            'chromium',
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        ]
        
        for chrome_cmd in chrome_commands:
            try:
                cmd = [
                    chrome_cmd,
                    '--headless',
                    '--disable-gpu',
                    '--print-to-pdf=' + pdf_file,
                    '--print-to-pdf-no-header',
                    '--virtual-time-budget=10000',
                    'file://' + os.path.abspath(html_file)
                ]
                
                subprocess.run(cmd, check=True, capture_output=True)
                
                if os.path.exists(pdf_file):
                    file_size = os.path.getsize(pdf_file) / (1024 * 1024)
                    print(f"✅ Chrome PDF转换成功!")
                    print(f"📄 文件: {pdf_file}")
                    print(f"📊 大小: {file_size:.1f} MB")
                    return True
                    
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
                
        print("❌ Chrome/Chromium未找到或转换失败")
        
    except Exception as e:
        print(f"❌ Chrome转换失败: {e}")
    
    return False

def main():
    """主函数"""
    
    print("📚 ODP_Demo 电子书生成器")
    print("=" * 40)
    
    # 生成HTML版本
    html_success = generate_html_book()
    
    if html_success:
        print("\n🎉 HTML电子书生成成功!")
        print("💡 您可以:")
        print("  1. 直接在浏览器中打开HTML文件阅读")
        print("  2. 使用浏览器的打印功能保存为PDF")
        print("  3. 运行PDF转换功能")
        
        # 询问是否转换为PDF
        convert_pdf = input("\n是否尝试转换为PDF? (y/n): ").lower().strip()
        
        if convert_pdf in ['y', 'yes', '是']:
            pdf_success = html_to_pdf()
            
            if not pdf_success:
                print("\n💡 PDF转换失败，但您可以:")
                print("  1. 在浏览器中打开HTML文件")
                print("  2. 使用Ctrl+P (Cmd+P) 打印")
                print("  3. 选择'保存为PDF'")
                print("  4. 调整页面设置后保存")
        
        print(f"\n📁 生成的文件位置: {os.getcwd()}")
        
    else:
        print("❌ 电子书生成失败")

if __name__ == "__main__":
    main()

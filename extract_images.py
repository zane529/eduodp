#!/usr/bin/env python3
"""
从Jupyter Notebook中提取图像的工具脚本
用于为文档生成高质量的可视化内容
"""

import json
import base64
import os
from pathlib import Path
import re

def extract_images_from_notebook(notebook_path, output_dir="images"):
    """
    从Jupyter notebook中提取所有图像
    
    Args:
        notebook_path (str): notebook文件路径
        output_dir (str): 输出目录
    
    Returns:
        list: 提取的图像文件列表
    """
    
    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 获取notebook名称（不含扩展名）
    notebook_name = Path(notebook_path).stem
    
    # 创建notebook专用子目录
    nb_output_dir = Path(output_dir) / notebook_name
    nb_output_dir.mkdir(parents=True, exist_ok=True)
    
    extracted_images = []
    
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        image_count = 0
        
        for cell_idx, cell in enumerate(notebook.get('cells', [])):
            if cell.get('cell_type') == 'code':
                outputs = cell.get('outputs', [])
                
                for output_idx, output in enumerate(outputs):
                    # 检查输出中的图像数据
                    if 'data' in output:
                        data = output['data']
                        
                        # 处理PNG图像
                        if 'image/png' in data:
                            image_count += 1
                            image_data = data['image/png']
                            
                            # 解码base64图像数据
                            image_bytes = base64.b64decode(image_data)
                            
                            # 生成文件名
                            filename = f"{notebook_name}_cell_{cell_idx}_output_{output_idx}_{image_count}.png"
                            filepath = nb_output_dir / filename
                            
                            # 保存图像
                            with open(filepath, 'wb') as img_file:
                                img_file.write(image_bytes)
                            
                            extracted_images.append(str(filepath))
                            print(f"提取图像: {filepath}")
                        
                        # 处理JPEG图像
                        if 'image/jpeg' in data:
                            image_count += 1
                            image_data = data['image/jpeg']
                            
                            image_bytes = base64.b64decode(image_data)
                            filename = f"{notebook_name}_cell_{cell_idx}_output_{output_idx}_{image_count}.jpg"
                            filepath = nb_output_dir / filename
                            
                            with open(filepath, 'wb') as img_file:
                                img_file.write(image_bytes)
                            
                            extracted_images.append(str(filepath))
                            print(f"提取图像: {filepath}")
        
        print(f"从 {notebook_path} 中提取了 {len(extracted_images)} 个图像")
        return extracted_images
        
    except Exception as e:
        print(f"处理 {notebook_path} 时出错: {e}")
        return []

def extract_all_notebooks(notebooks_dir=".", output_dir="images"):
    """
    提取目录中所有notebook的图像
    
    Args:
        notebooks_dir (str): notebook文件目录
        output_dir (str): 输出目录
    """
    
    notebooks_dir = Path(notebooks_dir)
    all_extracted = []
    
    # 查找所有.ipynb文件
    notebook_files = list(notebooks_dir.glob("*.ipynb"))
    
    if not notebook_files:
        print("未找到任何.ipynb文件")
        return
    
    print(f"找到 {len(notebook_files)} 个notebook文件")
    
    for notebook_path in notebook_files:
        print(f"\n处理: {notebook_path}")
        extracted = extract_images_from_notebook(notebook_path, output_dir)
        all_extracted.extend(extracted)
    
    print(f"\n总计提取了 {len(all_extracted)} 个图像")
    
    # 生成图像索引文件
    generate_image_index(all_extracted, output_dir)

def generate_image_index(image_list, output_dir):
    """
    生成图像索引文件
    
    Args:
        image_list (list): 图像文件列表
        output_dir (str): 输出目录
    """
    
    index_file = Path(output_dir) / "image_index.md"
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write("# 图像索引\n\n")
        f.write("本文件包含从Jupyter notebook中提取的所有图像的索引。\n\n")
        
        # 按notebook分组
        notebooks = {}
        for img_path in image_list:
            path_obj = Path(img_path)
            notebook_name = path_obj.parent.name
            if notebook_name not in notebooks:
                notebooks[notebook_name] = []
            notebooks[notebook_name].append(path_obj.name)
        
        for notebook_name, images in notebooks.items():
            f.write(f"## {notebook_name}\n\n")
            for img_name in sorted(images):
                img_path = f"{notebook_name}/{img_name}"
                f.write(f"- ![{img_name}](./{img_path})\n")
            f.write("\n")
    
    print(f"图像索引已生成: {index_file}")

if __name__ == "__main__":
    # 提取所有notebook的图像
    extract_all_notebooks()

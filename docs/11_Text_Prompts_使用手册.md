# 文本提示处理详细使用手册

## 功能概述

`11_Text_Prompts.ipynb`演示了基于文本提示的地理空间AI分析，通过自然语言指令实现智能图像分割。该功能结合了SAM模型和语言理解能力，让用户可以用简单的文字描述来指导AI进行精确的图像分析。

## 核心技术

### 1. LangSAM架构
- **语言理解**: 基于CLIP模型理解文本描述
- **图像分割**: 基于SAM模型进行精确分割
- **多模态融合**: 文本和图像信息的智能融合
- **零样本学习**: 无需训练即可处理新的目标类型

### 2. 环境设置

```python
import os
import leafmap
from samgeo import tms_to_geotiff
from samgeo.text_sam import LangSAM

# 设置工作目录
path = 'tmp/'
try:
    os.chdir(path)
    print("Current working directory: {0}".format(os.getcwd()))
except FileNotFoundError:
    print("Directory: {0} does not exist".format(path))
```

## 核心功能详解

### 1. 交互式地图和数据准备

```python
# 创建交互式地图
m = leafmap.Map(center=[-22.17615, -51.253043], zoom=18, height="800px")
m.add_basemap("SATELLITE")
m.attribution_control = False
m
```

**地图配置要点**:
- **高缩放级别**: zoom=18-19，确保目标清晰可见
- **卫星底图**: 使用高分辨率卫星影像
- **合适的中心点**: 选择目标丰富的区域

### 2. 影像数据下载

```python
# 下载高分辨率影像
image = "Image.tif"
tms_to_geotiff(output=image, bbox=bbox, zoom=19, source="Satellite", overwrite=True)
```

**参数优化**:
- `zoom=19`: 最高分辨率，适合精细目标检测
- `source="Satellite"`: 使用卫星影像源
- `overwrite=True`: 覆盖已存在文件

### 3. LangSAM模型初始化

```python
sam = LangSAM()
```

**模型特点**:
- **即插即用**: 无需复杂配置
- **多语言支持**: 支持中英文提示
- **高精度**: 结合语言和视觉的双重优势
- **快速响应**: 优化的推理速度

### 4. 文本提示分析

```python
# 基础文本提示
text_prompt = "trees"
sam.predict(image, text_prompt, box_threshold=0.3, text_threshold=0.25)
```

#### 参数深度解析

**text_prompt参数 - 文本描述**
- **数据类型**: 字符串
- **语言支持**: 英文、中文
- **描述策略**:
  - 简单名词: "trees", "buildings", "cars"
  - 形容词修饰: "green trees", "tall buildings"
  - 具体描述: "swimming pools", "tennis courts"

**box_threshold参数 - 边界框阈值**
- **默认值**: 0.3
- **取值范围**: 0.1-0.9
- **效果对比**:
  - 0.1-0.2: 检测更多目标，可能包含误检
  - 0.3-0.4: 平衡精度和召回率 (推荐)
  - 0.5-0.9: 高精度，可能遗漏目标

**text_threshold参数 - 文本匹配阈值**
- **默认值**: 0.25
- **取值范围**: 0.1-0.5
- **作用**: 控制文本描述与图像内容的匹配程度
- **调优建议**:
  - 0.15-0.20: 宽松匹配，适合模糊描述
  - 0.25-0.30: 标准匹配 (推荐)
  - 0.35-0.50: 严格匹配，适合精确描述

### 5. 结果可视化

#### 5.1 带边界框的可视化

```python
sam.show_anns(
    cmap='Greens',
    box_color='red',
    title='Automatic Segmentation of Trees',
    blend=True,
)
```

**可视化参数详解**:

**cmap参数 - 颜色映射**
- **常用选项**:
  - `'Greens'`: 绿色系，适合植被
  - `'Blues'`: 蓝色系，适合水体
  - `'Reds'`: 红色系，适合建筑
  - `'Greys'`: 灰度系，通用选择

**box_color参数 - 边界框颜色**
- **颜色选择**: 'red', 'blue', 'green', 'yellow'
- **对比原则**: 与背景形成鲜明对比
- **建议搭配**:
  - 绿色植被 + 红色边界框
  - 蓝色水体 + 黄色边界框

#### 5.2 纯分割结果显示

```python
sam.show_anns(
    cmap='Greens',
    add_boxes=False,
    alpha=0.5,
    title='Automatic Segmentation of Trees',
)
```

**alpha参数 - 透明度控制**
- **取值范围**: 0.0-1.0
- **效果对比**:
  - 0.3-0.5: 半透明，可见底图
  - 0.7-0.9: 较不透明，突出分割结果
  - 1.0: 完全不透明

#### 5.3 输出保存

```python
sam.show_anns(
    cmap='Greys_r',
    add_boxes=False,
    alpha=1,
    title='Automatic Segmentation of Trees',
    blend=False,
    output='trees.tif',
)
```

**输出参数**:
- `blend=False`: 纯分割结果，不与原图混合
- `output='trees.tif'`: 保存为GeoTIFF格式

### 6. 矢量化和地图集成

```python
# 转换为矢量格式
sam.raster_to_vector("trees.tif", "trees.shp")

# 添加到地图
m.add_raster("trees.tif", layer_name="Trees", palette="Greens", opacity=0.5, nodata=0)

style = {
    "color": "#3388ff",
    "weight": 2,
    "fillColor": "#7c4185", 
    "fillOpacity": 0.5,
}
m.add_vector("trees.shp", layer_name="Vector", style=style)
```

## 高级应用案例

### 案例1: 多类型目标检测

```python
# 初始化模型
sam = LangSAM()

# 定义多个目标类型
targets = {
    "buildings": {"threshold": 0.35, "color": "Reds"},
    "trees": {"threshold": 0.25, "color": "Greens"}, 
    "roads": {"threshold": 0.30, "color": "Greys"},
    "water": {"threshold": 0.40, "color": "Blues"}
}

# 批量处理
results = {}
for target_name, config in targets.items():
    print(f"检测 {target_name}...")
    
    sam.predict(
        image, 
        target_name,
        box_threshold=config["threshold"],
        text_threshold=0.25
    )
    
    output_file = f"{target_name}.tif"
    sam.show_anns(
        cmap=config["color"],
        add_boxes=False,
        alpha=1,
        blend=False,
        output=output_file
    )
    
    results[target_name] = output_file
    print(f"完成 {target_name} 检测，保存至 {output_file}")
```

### 案例2: 精确描述检测

```python
# 使用详细描述提高检测精度
detailed_prompts = {
    "residential_buildings": "residential houses and apartment buildings",
    "commercial_buildings": "office buildings and shopping centers", 
    "green_trees": "healthy green trees and forest areas",
    "swimming_pools": "blue rectangular swimming pools in backyards",
    "tennis_courts": "rectangular tennis courts with white lines",
    "parking_lots": "large paved parking areas with cars"
}

for prompt_name, prompt_text in detailed_prompts.items():
    print(f"检测: {prompt_text}")
    
    sam.predict(
        image,
        prompt_text,
        box_threshold=0.3,
        text_threshold=0.2  # 降低阈值适应复杂描述
    )
    
    sam.show_anns(
        cmap='viridis',
        add_boxes=True,
        title=f'Detection: {prompt_name}',
        output=f"{prompt_name}.tif"
    )
```

### 案例3: 中文提示应用

```python
# 中文提示示例
chinese_prompts = {
    "建筑物": "buildings",
    "树木": "trees", 
    "道路": "roads",
    "水体": "water bodies",
    "农田": "agricultural fields",
    "停车场": "parking lots"
}

for chinese_text, english_text in chinese_prompts.items():
    print(f"检测 {chinese_text} ({english_text})")
    
    # 使用英文提示（当前版本推荐）
    sam.predict(image, english_text, box_threshold=0.3)
    
    sam.show_anns(
        title=f'{chinese_text}检测结果',
        output=f"{chinese_text}.tif"
    )
```

## 参数优化策略

### 1. 阈值调优方法

```python
def optimize_thresholds(image, text_prompt, threshold_ranges):
    """自动优化检测阈值"""
    
    best_config = None
    best_score = 0
    
    for box_thresh in threshold_ranges['box']:
        for text_thresh in threshold_ranges['text']:
            sam.predict(
                image, 
                text_prompt,
                box_threshold=box_thresh,
                text_threshold=text_thresh
            )
            
            # 评估检测质量（需要实现评估函数）
            score = evaluate_detection_quality(sam.masks)
            
            if score > best_score:
                best_score = score
                best_config = {
                    'box_threshold': box_thresh,
                    'text_threshold': text_thresh,
                    'score': score
                }
    
    return best_config

# 使用示例
threshold_ranges = {
    'box': [0.2, 0.3, 0.4, 0.5],
    'text': [0.15, 0.20, 0.25, 0.30]
}

optimal_config = optimize_thresholds(image, "trees", threshold_ranges)
print(f"最优配置: {optimal_config}")
```

### 2. 提示词工程

```python
# 提示词优化策略
def generate_enhanced_prompts(base_prompt):
    """生成增强的提示词"""
    
    enhancements = {
        "trees": [
            "trees",
            "green trees", 
            "healthy trees",
            "trees and vegetation",
            "forest trees and bushes"
        ],
        "buildings": [
            "buildings",
            "houses and buildings",
            "residential and commercial buildings", 
            "structures and buildings",
            "architectural buildings"
        ],
        "water": [
            "water",
            "water bodies",
            "rivers and lakes",
            "blue water areas",
            "natural and artificial water"
        ]
    }
    
    return enhancements.get(base_prompt, [base_prompt])

# 测试不同提示词效果
base_target = "trees"
prompt_variations = generate_enhanced_prompts(base_target)

for i, prompt in enumerate(prompt_variations):
    sam.predict(image, prompt, box_threshold=0.3)
    sam.show_anns(
        title=f'Prompt {i+1}: {prompt}',
        output=f"trees_prompt_{i+1}.tif"
    )
```

## 质量评估和验证

### 1. 检测结果统计

```python
def analyze_detection_results(masks_file):
    """分析检测结果统计信息"""
    
    import rasterio
    import numpy as np
    
    with rasterio.open(masks_file) as src:
        masks = src.read(1)
    
    # 基础统计
    total_pixels = masks.size
    detected_pixels = np.count_nonzero(masks)
    detection_ratio = detected_pixels / total_pixels
    
    # 连通区域分析
    from skimage import measure
    labeled_masks = measure.label(masks)
    num_objects = labeled_masks.max()
    
    # 对象大小分布
    object_sizes = []
    for i in range(1, num_objects + 1):
        object_size = np.sum(labeled_masks == i)
        object_sizes.append(object_size)
    
    stats = {
        'total_objects': num_objects,
        'detection_ratio': detection_ratio,
        'avg_object_size': np.mean(object_sizes) if object_sizes else 0,
        'min_object_size': np.min(object_sizes) if object_sizes else 0,
        'max_object_size': np.max(object_sizes) if object_sizes else 0
    }
    
    return stats

# 使用示例
results_stats = analyze_detection_results("trees.tif")
print("检测结果统计:")
for key, value in results_stats.items():
    print(f"  {key}: {value}")
```

### 2. 可视化质量检查

```python
def create_quality_check_visualization(original_image, masks_file, sample_size=5):
    """创建质量检查可视化"""
    
    import matplotlib.pyplot as plt
    import rasterio
    from rasterio.plot import show
    
    # 读取数据
    with rasterio.open(original_image) as src:
        original = src.read()
    
    with rasterio.open(masks_file) as src:
        masks = src.read(1)
    
    # 创建对比图
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # 原始图像
    show(original, ax=axes[0], title='Original Image')
    
    # 检测结果
    axes[1].imshow(masks, cmap='Greens', alpha=0.8)
    axes[1].set_title('Detection Results')
    axes[1].axis('off')
    
    # 叠加显示
    show(original, ax=axes[2], alpha=0.7)
    axes[2].imshow(masks, cmap='Reds', alpha=0.5)
    axes[2].set_title('Overlay')
    
    plt.tight_layout()
    plt.savefig('quality_check.png', dpi=300, bbox_inches='tight')
    plt.show()

# 使用示例
create_quality_check_visualization("Image.tif", "trees.tif")
```

## 常见问题与解决方案

### 1. 检测结果不准确

**问题现象**: 目标检测不完整或有误检

**解决方案**:
```python
# 方案1: 调整阈值
sam.predict(image, "trees", box_threshold=0.2, text_threshold=0.2)  # 降低阈值

# 方案2: 改进提示词
enhanced_prompt = "green healthy trees and forest vegetation"
sam.predict(image, enhanced_prompt, box_threshold=0.3)

# 方案3: 多次检测合并
prompts = ["trees", "green trees", "forest"]
combined_masks = combine_multiple_detections(image, prompts)
```

### 2. 处理速度慢

**问题现象**: 单次检测耗时过长

**解决方案**:
```python
# 方案1: 降低图像分辨率
resized_image = resize_image("Image.tif", scale_factor=0.5)
sam.predict(resized_image, "trees")

# 方案2: 分块处理
def process_image_in_tiles(image_path, tile_size=1000):
    # 将大图像分割成小块处理
    pass
```

### 3. 内存不足

**问题现象**: CUDA out of memory或系统内存不足

**解决方案**:
```python
# 清理内存
import torch
import gc

torch.cuda.empty_cache()
gc.collect()

# 使用较小的图像
small_image = downsample_image("Image.tif", factor=2)
```

## 最佳实践建议

### 1. 提示词设计原则

- **简洁明确**: 使用清晰的目标描述
- **避免歧义**: 避免可能引起混淆的词汇
- **上下文相关**: 考虑图像的具体场景
- **迭代优化**: 根据结果不断改进提示词

### 2. 参数调优策略

- **从默认值开始**: 使用推荐的默认参数
- **逐步调整**: 一次只调整一个参数
- **记录最佳组合**: 保存有效的参数配置
- **场景特化**: 为不同应用场景定制参数

### 3. 结果验证流程

- **视觉检查**: 人工检查关键区域
- **统计分析**: 分析检测结果的统计特征
- **对比验证**: 与其他方法结果对比
- **实地验证**: 条件允许时进行实地验证

---

*本详细使用手册提供了文本提示功能的全面指导，帮助用户充分利用自然语言与AI的结合，实现高效精确的地理空间分析。*

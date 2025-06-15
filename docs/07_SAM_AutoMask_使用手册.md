# SAM自动掩膜生成详细使用手册

## 功能概述

`07_SAM_AutoMask.ipynb`展示了Segment Anything Model (SAM)在地理空间数据中的自动掩膜生成应用，实现无需人工标注的智能图像分割。本手册提供完整的参数解析、应用案例和最佳实践指导。

## 环境要求

### 硬件要求
- **GPU**: 推荐NVIDIA GPU (8GB+ VRAM)
- **内存**: 16GB+ RAM
- **存储**: 10GB+ 可用空间 (模型文件约2.4GB)

### 软件依赖
```python
import os
import leafmap
import torch
from samgeo import SamGeo, show_image, download_file, overlay_images, tms_to_geotiff
```

## 核心功能详解

### 1. 工作环境设置

```python
import os
path = 'tmp/'

try:
    os.chdir(path)
    print("Current working directory: {0}".format(os.getcwd()))
except FileNotFoundError:
    print("Directory: {0} does not exist".format(path))
except NotADirectoryError:
    print("{0} is not a directory".format(path))
except PermissionError:
    print("You do not have permissions to change to {0}".format(path))
```

**最佳实践**:
- 使用专门的工作目录避免文件混乱
- 确保目录具有读写权限
- 预留足够的磁盘空间存储结果

### 2. 交互式地图创建

```python
m = leafmap.Map(center=[37.8713, -122.2580], zoom=17, height="800px")
m.add_basemap("SATELLITE")
m.attribution_control = False
m
```

#### 参数深度解析

**center参数 - 地图中心点**
- **数据类型**: 列表 [纬度, 经度]
- **示例值**: [37.8713, -122.2580] (旧金山湾区)
- **选择原则**: 
  - 选择数据丰富的区域
  - 避免大面积水体或云层
  - 考虑建筑物密度适中的区域

**zoom参数 - 缩放级别**
- **推荐值**: 15-18 (建筑物级别)
- **效果对比**:
  - zoom=15: 街区级别，适合大范围分析
  - zoom=17: 建筑物级别，适合精细分割
  - zoom=19: 超高精度，适合小目标检测

**height参数 - 地图高度**
- **推荐值**: "600px" - "1000px"
- **影响因素**: 屏幕分辨率、分析需求

### 3. 区域选择和数据下载

```python
# 获取用户绘制的区域
if m.user_roi_bounds() is not None:
    bbox = m.user_roi_bounds()
else:
    bbox = [-122.2659, 37.8682, -122.2521, 37.8741]

# 下载卫星影像
image = "satellite.tif"
tms_to_geotiff(output=image, bbox=bbox, zoom=17, source="Satellite", overwrite=True)
```

#### 区域选择策略

**bbox参数格式**: [西经, 南纬, 东经, 北纬]

**区域大小建议**:
```python
# 小区域 (适合测试)
small_bbox = [-122.2659, 37.8682, -122.2621, 37.8720]  # ~0.4km²

# 中等区域 (适合分析)
medium_bbox = [-122.2659, 37.8682, -122.2521, 37.8741]  # ~1.5km²

# 大区域 (需要更多资源)
large_bbox = [-122.2759, 37.8582, -122.2421, 37.8841]   # ~6km²
```

**下载参数优化**:
- `zoom=17`: 高分辨率，适合建筑物分割
- `zoom=15`: 中分辨率，适合大范围分析
- `overwrite=True`: 覆盖已存在文件

### 4. SAM模型初始化

#### 4.1 GPU内存清理

```python
import torch
torch.cuda.empty_cache()
```

**重要性**: 
- 清理GPU内存避免内存不足
- 确保模型加载成功
- 提高处理稳定性

#### 4.2 模型检查点配置

```python
out_dir = os.path.join(os.path.expanduser("~"), "Downloads")
checkpoint = os.path.join(out_dir, "sam_vit_h_4b8939.pth")
```

**模型文件管理**:
- 自动下载到用户下载目录
- 文件大小约2.4GB
- 首次运行需要网络连接

#### 4.3 SAM实例化

```python
sam = SamGeo(
    model_type="vit_h",
    checkpoint=checkpoint,
    sam_kwargs=None,
)
```

**model_type参数详解**:

| 模型类型 | 文件大小 | 精度 | 速度 | 适用场景 |
|---------|---------|------|------|----------|
| vit_h | 2.4GB | 最高 | 慢 | 高精度分析 |
| vit_l | 1.2GB | 高 | 中等 | 平衡应用 |
| vit_b | 375MB | 中等 | 快 | 快速预览 |

### 5. 基础自动分割

```python
sam.generate(image, output="masks.tif", foreground=True, unique=True)
```

#### 参数深度解析

**foreground参数**:
- `True`: 生成前景掩膜 (推荐)
- `False`: 生成背景掩膜
- **效果**: 前景掩膜更适合目标检测

**unique参数**:
- `True`: 每个对象分配唯一ID
- `False`: 所有对象使用相同值
- **用途**: 便于后续统计和分析

#### 结果可视化

```python
# 显示二值掩膜
sam.show_masks(cmap="binary_r")

# 显示彩色标注
sam.show_anns(axis="off", alpha=1, output="annotations.tif")
```

**可视化参数**:
- `cmap="binary_r"`: 黑白反色显示
- `axis="off"`: 隐藏坐标轴
- `alpha=1`: 完全不透明

### 6. 高级参数调优

```python
sam_kwargs = {
    "points_per_side": 32,
    "pred_iou_thresh": 0.86,
    "stability_score_thresh": 0.92,
    "crop_n_layers": 1,
    "crop_n_points_downscale_factor": 2,
    "min_mask_region_area": 100,
}

sam = SamGeo(
    model_type="vit_h",
    checkpoint=checkpoint,
    sam_kwargs=sam_kwargs,
)
```

#### 关键参数详解

**points_per_side** - 采样点密度
- **默认值**: 32
- **取值范围**: 16-64
- **效果对比**:
  - 16: 快速处理，可能遗漏小目标
  - 32: 平衡精度和速度 (推荐)
  - 64: 高精度，处理时间长

**pred_iou_thresh** - IoU阈值
- **默认值**: 0.88
- **取值范围**: 0.7-0.95
- **作用**: 过滤低质量预测
- **调优建议**:
  - 0.86: 适合复杂场景
  - 0.88: 标准设置
  - 0.92: 严格质量控制

**stability_score_thresh** - 稳定性阈值
- **默认值**: 0.95
- **取值范围**: 0.8-0.98
- **作用**: 确保分割结果稳定性
- **调优策略**:
  - 降低阈值: 获得更多分割结果
  - 提高阈值: 获得更稳定结果

**min_mask_region_area** - 最小区域面积
- **默认值**: 0
- **推荐值**: 50-200像素
- **作用**: 过滤噪声和小碎片
- **应用场景**:
  - 建筑物分割: 100-500
  - 车辆检测: 20-100
  - 植被分析: 50-200

### 7. 结果后处理

#### 7.1 矢量化转换

```python
# 转换为GeoPackage格式
sam.tiff_to_vector("masks.tif", "masks.gpkg")

# 转换为Shapefile格式
sam.tiff_to_vector("masks.tif", "masks.shp")

# 带简化的转换
sam.tiff_to_gpkg("masks.tif", "simplified.gpkg", simplify_tolerance=0.5)
```

**格式选择建议**:
- **GeoPackage (.gpkg)**: 推荐，支持大数据
- **Shapefile (.shp)**: 兼容性好，有大小限制
- **GeoJSON (.geojson)**: 网络友好，文本格式

#### 7.2 地图可视化

```python
style = {
    "color": "#3388ff",        # 边界颜色
    "weight": 2,               # 边界宽度
    "fillColor": "#7c4185",    # 填充颜色
    "fillOpacity": 0.5,        # 填充透明度
}
m.add_vector("masks.gpkg", layer_name="Vector", style=style)
```

## 实际应用案例

### 案例1: 城市建筑物提取

```python
# 城市区域配置
urban_config = {
    "points_per_side": 32,
    "pred_iou_thresh": 0.88,
    "stability_score_thresh": 0.92,
    "min_mask_region_area": 200,  # 过滤小建筑
}

# 处理城市影像
sam_urban = SamGeo(model_type="vit_h", sam_kwargs=urban_config)
sam_urban.generate("urban_image.tif", output="buildings.tif", foreground=True)

# 统计建筑物数量和面积
import geopandas as gpd
buildings_gdf = gpd.read_file("buildings.gpkg")
print(f"检测到建筑物: {len(buildings_gdf)} 个")
print(f"总建筑面积: {buildings_gdf.geometry.area.sum():.2f} 平方米")
```

### 案例2: 农田边界识别

```python
# 农田专用配置
agricultural_config = {
    "points_per_side": 24,
    "pred_iou_thresh": 0.85,
    "stability_score_thresh": 0.90,
    "min_mask_region_area": 500,  # 农田通常较大
}

# 处理农田影像
sam_agri = SamGeo(model_type="vit_l", sam_kwargs=agricultural_config)
sam_agri.generate("farmland.tif", output="fields.tif", foreground=True)

# 计算农田统计信息
fields_gdf = gpd.read_file("fields.gpkg")
field_areas = fields_gdf.geometry.area
print(f"农田数量: {len(fields_gdf)}")
print(f"平均面积: {field_areas.mean():.2f} 平方米")
print(f"最大农田: {field_areas.max():.2f} 平方米")
```

### 案例3: 水体检测

```python
# 水体检测配置
water_config = {
    "points_per_side": 28,
    "pred_iou_thresh": 0.90,
    "stability_score_thresh": 0.94,
    "min_mask_region_area": 100,
}

# 处理水体影像
sam_water = SamGeo(model_type="vit_h", sam_kwargs=water_config)
sam_water.generate("water_scene.tif", output="water_bodies.tif", foreground=True)

# 水体面积统计
water_gdf = gpd.read_file("water_bodies.gpkg")
total_water_area = water_gdf.geometry.area.sum()
print(f"水体总面积: {total_water_area:.2f} 平方米")
```

## 性能优化策略

### 1. 内存管理

```python
# 定期清理GPU内存
def clear_gpu_memory():
    import torch
    torch.cuda.empty_cache()
    import gc
    gc.collect()

# 在处理大图像前清理内存
clear_gpu_memory()
```

### 2. 批处理优化

```python
def batch_process_images(image_list, output_dir, sam_config):
    """批量处理多个影像"""
    sam = SamGeo(model_type="vit_h", sam_kwargs=sam_config)
    
    for i, image_path in enumerate(image_list):
        try:
            output_path = f"{output_dir}/masks_{i}.tif"
            sam.generate(image_path, output=output_path, foreground=True)
            print(f"完成处理: {image_path}")
            
            # 每处理5个图像清理一次内存
            if (i + 1) % 5 == 0:
                clear_gpu_memory()
                
        except Exception as e:
            print(f"处理失败 {image_path}: {e}")
            continue
```

### 3. 参数自适应调整

```python
def adaptive_sam_config(image_size, target_objects):
    """根据图像大小和目标类型自适应调整参数"""
    
    # 基础配置
    config = {
        "pred_iou_thresh": 0.88,
        "stability_score_thresh": 0.92,
    }
    
    # 根据图像大小调整采样密度
    if image_size < 1000000:  # 小图像
        config["points_per_side"] = 24
    elif image_size < 4000000:  # 中等图像
        config["points_per_side"] = 32
    else:  # 大图像
        config["points_per_side"] = 40
    
    # 根据目标类型调整最小面积
    min_areas = {
        "buildings": 100,
        "vehicles": 20,
        "fields": 500,
        "water": 50
    }
    config["min_mask_region_area"] = min_areas.get(target_objects, 100)
    
    return config
```

## 常见问题与解决方案

### 1. GPU内存不足

**问题现象**: CUDA out of memory错误

**解决方案**:
```python
# 方案1: 使用较小的模型
sam = SamGeo(model_type="vit_b")  # 使用基础模型

# 方案2: 降低采样密度
sam_kwargs = {"points_per_side": 16}  # 减少采样点

# 方案3: 分块处理大图像
def process_large_image_in_chunks(image_path, chunk_size=1000):
    # 将大图像分割成小块处理
    pass
```

### 2. 分割结果过多碎片

**问题现象**: 生成大量小的无意义分割

**解决方案**:
```python
# 提高最小区域面积阈值
sam_kwargs = {
    "min_mask_region_area": 200,  # 增加到200
    "pred_iou_thresh": 0.90,      # 提高IoU阈值
}
```

### 3. 重要目标被遗漏

**问题现象**: 某些重要对象没有被分割

**解决方案**:
```python
# 增加采样密度和降低阈值
sam_kwargs = {
    "points_per_side": 48,        # 增加采样点
    "pred_iou_thresh": 0.85,      # 降低IoU阈值
    "stability_score_thresh": 0.88 # 降低稳定性阈值
}
```

### 4. 处理速度过慢

**问题现象**: 单张图像处理时间过长

**解决方案**:
```python
# 使用较小模型或降低参数
sam_kwargs = {
    "points_per_side": 24,        # 减少采样点
    "crop_n_layers": 0,           # 禁用裁剪层
}

# 或使用vit_l模型
sam = SamGeo(model_type="vit_l")
```

## 最佳实践建议

### 1. 参数选择策略

**通用原则**:
- 从默认参数开始测试
- 根据结果逐步调整
- 平衡精度和效率
- 记录最佳参数组合

**场景特定建议**:
```python
# 高精度场景 (科研、精密分析)
high_precision_config = {
    "points_per_side": 48,
    "pred_iou_thresh": 0.90,
    "stability_score_thresh": 0.95,
    "min_mask_region_area": 50
}

# 高效率场景 (快速预览、大批量处理)
high_efficiency_config = {
    "points_per_side": 20,
    "pred_iou_thresh": 0.85,
    "stability_score_thresh": 0.88,
    "min_mask_region_area": 200
}
```

### 2. 质量控制流程

```python
def quality_assessment(masks_path, original_image_path):
    """分割质量评估"""
    
    # 加载结果
    masks_gdf = gpd.read_file(masks_path)
    
    # 基础统计
    stats = {
        "total_objects": len(masks_gdf),
        "total_area": masks_gdf.geometry.area.sum(),
        "avg_area": masks_gdf.geometry.area.mean(),
        "area_std": masks_gdf.geometry.area.std()
    }
    
    # 面积分布检查
    area_percentiles = masks_gdf.geometry.area.quantile([0.1, 0.5, 0.9])
    
    # 形状复杂度检查
    complexity = masks_gdf.geometry.apply(
        lambda geom: geom.length / (2 * np.sqrt(np.pi * geom.area))
    )
    
    stats.update({
        "area_10th": area_percentiles[0.1],
        "area_median": area_percentiles[0.5], 
        "area_90th": area_percentiles[0.9],
        "avg_complexity": complexity.mean()
    })
    
    return stats
```

### 3. 结果验证方法

```python
def validate_segmentation_results(masks_gdf, validation_samples=10):
    """验证分割结果质量"""
    
    # 随机抽样验证
    sample_masks = masks_gdf.sample(n=min(validation_samples, len(masks_gdf)))
    
    validation_results = []
    for idx, mask in sample_masks.iterrows():
        # 几何有效性检查
        is_valid = mask.geometry.is_valid
        
        # 面积合理性检查
        area = mask.geometry.area
        is_reasonable_size = 10 < area < 100000  # 根据应用调整
        
        # 形状合理性检查
        compactness = 4 * np.pi * area / (mask.geometry.length ** 2)
        is_reasonable_shape = compactness > 0.1
        
        validation_results.append({
            "mask_id": idx,
            "is_valid": is_valid,
            "is_reasonable_size": is_reasonable_size,
            "is_reasonable_shape": is_reasonable_shape,
            "area": area,
            "compactness": compactness
        })
    
    return validation_results
```

---

*本详细使用手册提供了SAM自动掩膜生成的全面指导，从基础操作到高级优化，帮助用户充分发挥SAM在地理空间分析中的强大能力。*

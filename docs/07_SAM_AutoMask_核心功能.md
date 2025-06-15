# SAM自动掩膜生成核心功能解析

## 1. SAM模型初始化

```python
from samgeo import SamGeo
sam = SamGeo(
    model_type="vit_h",
    checkpoint="sam_vit_h_4b8939.pth",
    device="cuda"
)
```

### 参数详解
- **model_type**: 模型类型
  - "vit_h": 高精度模型 (2.4GB)
  - "vit_l": 大型模型 (1.2GB) 
  - "vit_b": 基础模型 (375MB)
- **checkpoint**: 模型权重文件路径
- **device**: 计算设备 ("cuda" 或 "cpu")

## 2. 自动掩膜生成

```python
sam.generate(
    source="image.tif",
    output="masks.tif", 
    foreground=True,
    erosion_kernel=(3, 3),
    mask_multiplier=255
)
```

### 关键参数效果
- **foreground=True**: 生成前景掩膜
- **erosion_kernel**: 形态学腐蚀核大小，影响掩膜边界
- **mask_multiplier**: 掩膜像素值倍数

## 3. 结果可视化

```python
show_image("image.tif", "masks.tif", figsize=(12, 10))
```

---
*这是核心功能的快速解析，详细版本正在编写中...*

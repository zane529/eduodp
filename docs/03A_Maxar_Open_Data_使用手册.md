# Maxar开放数据集成使用手册

## 功能概述

`03A_Maxar_Open_Data.ipynb`演示了如何集成和使用Maxar公司提供的开放卫星数据，特别是针对土耳其地震等重大事件的高分辨率影像数据。

## 核心功能

### 1. 环境设置
```python
import os
import leafmap

path = 'tmp/'
os.chdir(path)
```

### 2. Maxar数据集合查询
```python
# 查看所有可用集合
leafmap.maxar_collections()

# 查看特定集合的子集合
collections = leafmap.maxar_child_collections('Kahramanmaras-turkey-earthquake-23')
print(f"集合数量: {len(collections)}")
```

### 3. 数据项目获取
```python
gdf = leafmap.maxar_items(
    collection_id='Kahramanmaras-turkey-earthquake-23',
    child_id='1050050044DE7E00',
    return_gdf=True,
    assets=['visual'],
)
```

**参数详解**:
- `collection_id`: 主集合标识符
- `child_id`: 子集合标识符  
- `return_gdf`: 返回GeoDataFrame格式
- `assets`: 指定资产类型 ['visual', 'analytic']

### 4. 地图可视化
```python
m = leafmap.Map()
m.add_gdf(gdf, layer_name="Footprints")
m
```

### 5. 影像镶嵌
```python
images = gdf['visual'].tolist()
leafmap.create_mosaicjson(images, output='mosaic.json')

# 添加镶嵌图层
m.add_stac_layer(mosaic_url, name="Mosaic")
```

## 应用场景

- **灾害响应**: 地震、洪水等自然灾害的快速评估
- **高分辨率分析**: 亚米级精度的详细分析
- **变化检测**: 灾前灾后对比分析
- **应急管理**: 快速获取最新高分辨率影像

## 数据特点

- **超高分辨率**: 0.3-0.6米空间分辨率
- **快速响应**: 灾害事件后快速成像
- **全色+多光谱**: 支持详细分析
- **开放获取**: 特定事件数据免费开放

---

*详细参数解析和高级应用正在完善中...*

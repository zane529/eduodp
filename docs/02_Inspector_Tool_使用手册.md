# 数据检查工具使用手册

## 功能概述

`02_Inspector_Tool.ipynb`提供了交互式数据检查工具，专门用于快速检查和分析STAC (SpatioTemporal Asset Catalog) 数据的质量、属性和可视化效果。该工具通过多波段组合显示，帮助用户评估卫星影像数据的质量和适用性。

## 适用场景

- **数据质量评估** - 快速检查影像数据的质量和可用性
- **波段组合测试** - 测试不同波段组合的视觉效果
- **数据预览** - 在大规模处理前预览数据内容
- **多时相对比** - 对比不同时间的影像数据
- **光谱分析准备** - 为光谱分析选择合适的波段组合

## 环境要求

### 软件依赖
```python
import leafmap
```

### 数据要求
- 有效的STAC集合和项目标识符
- 网络访问STAC数据服务
- 足够的带宽用于影像数据加载

## 核心功能详解

### 1. 基础环境初始化

```python
import leafmap
```

**leafmap库特点**:
- 专为地理空间数据可视化设计
- 内置STAC数据支持
- 交互式地图界面
- 多种数据格式支持

### 2. 交互式地图创建

```python
m = leafmap.Map()
```

**地图初始化参数**:
- **默认中心**: 全球视图
- **默认缩放**: 适中级别
- **交互功能**: 支持缩放、平移、图层控制
- **底图**: 默认使用OpenStreetMap

**自定义地图配置**:
```python
# 自定义地图设置
m = leafmap.Map(
    center=[40.0, -100.0],    # 美国中部
    zoom=4,                   # 国家级视图
    height="600px",           # 地图高度
    attribution_control=False  # 隐藏版权信息
)
```

### 3. STAC数据配置

```python
collection = "landsat-8-c2-l2"
item = "LC08_L2SP_047027_20201204_02_T1"
```

#### 参数深度解析

**collection参数 - 数据集合标识**
- **数据类型**: 字符串
- **作用**: 指定STAC数据集合
- **格式**: 遵循STAC标准命名规范
- **示例集合**:
  - `"landsat-8-c2-l2"`: Landsat 8 Collection 2 Level-2
  - `"landsat-9-c2-l2"`: Landsat 9 Collection 2 Level-2
  - `"sentinel-2-l2a"`: Sentinel-2 Level-2A
  - `"sentinel-1-grd"`: Sentinel-1 Ground Range Detected

**item参数 - 具体数据项标识**
- **数据类型**: 字符串
- **作用**: 指定集合中的具体影像产品
- **Landsat命名规范解析**:
  ```
  LC08_L2SP_047027_20201204_02_T1
  │    │    │      │        │  │
  │    │    │      │        │  └─ 处理级别 (T1=Tier 1)
  │    │    │      │        └─── 集合版本 (02)
  │    │    │      └──────────── 获取日期 (2020-12-04)
  │    │    └─────────────────── Path/Row (047/027)
  │    └──────────────────────── 产品级别 (L2SP=Surface Reflectance)
  └───────────────────────────── 传感器 (LC08=Landsat 8)
  ```

### 4. 多波段图层添加

#### 4.1 假彩色组合 (Band 7-5-4)

```python
m.add_stac_layer(
    collection=collection,
    item=item,
    assets="SR_B7,SR_B5,SR_B4",
    name="Landsat Band-754",
)
```

**波段组合分析**:
- **SR_B7 (短波红外2)**: 2.11-2.29 μm
  - 用途: 地质分析、矿物识别
  - 特点: 穿透大气能力强
- **SR_B5 (近红外)**: 0.85-0.88 μm  
  - 用途: 植被分析、水体识别
  - 特点: 植被高反射，水体低反射
- **SR_B4 (红光)**: 0.64-0.67 μm
  - 用途: 植被叶绿素吸收
  - 特点: 植被低反射，土壤中等反射

**视觉效果**:
- **植被**: 呈现红色调
- **水体**: 呈现深蓝或黑色
- **城市**: 呈现青色或白色
- **裸土**: 呈现棕色或黄色

#### 4.2 标准假彩色组合 (Band 5-4-3)

```python
m.add_stac_layer(
    collection=collection,
    item=item,
    assets="SR_B5,SR_B4,SR_B3",
    name="Landsat Band-543",
)
```

**波段组合分析**:
- **SR_B5 (近红外)**: 0.85-0.88 μm
- **SR_B4 (红光)**: 0.64-0.67 μm
- **SR_B3 (绿光)**: 0.53-0.59 μm
  - 用途: 植被健康度评估
  - 特点: 叶绿素反射峰

**视觉效果**:
- **健康植被**: 鲜红色
- **稀疏植被**: 粉红色
- **水体**: 深蓝或黑色
- **城市建筑**: 蓝白色
- **农田**: 根据作物类型呈现不同红色调

### 5. 地图显示和交互

```python
m  # 显示交互式地图
```

**交互功能**:
- **图层控制**: 开关不同波段组合
- **透明度调节**: 调整图层透明度
- **缩放导航**: 放大缩小查看细节
- **像素值查询**: 点击获取像素值信息

## 高级应用案例

### 案例1: 多时相数据对比检查

```python
# 创建对比地图
m_compare = leafmap.Map(center=[39.5, -98.0], zoom=6)

# 添加不同时间的数据
dates = [
    ("LC08_L2SP_047027_20200601_02_T1", "2020年6月"),
    ("LC08_L2SP_047027_20200801_02_T1", "2020年8月"),
    ("LC08_L2SP_047027_20201001_02_T1", "2020年10月")
]

for item_id, label in dates:
    m_compare.add_stac_layer(
        collection="landsat-8-c2-l2",
        item=item_id,
        assets="SR_B5,SR_B4,SR_B3",
        name=f"Landsat {label}",
        opacity=0.7
    )

m_compare
```

### 案例2: 不同传感器数据对比

```python
# 创建传感器对比地图
m_sensors = leafmap.Map(center=[40.0, -74.0], zoom=8)

# Landsat 8数据
m_sensors.add_stac_layer(
    collection="landsat-8-c2-l2",
    item="LC08_L2SP_014032_20230615_02_T1",
    assets="SR_B4,SR_B3,SR_B2",  # 真彩色
    name="Landsat 8 真彩色",
    opacity=0.8
)

# Sentinel-2数据 (如果可用)
try:
    m_sensors.add_stac_layer(
        collection="sentinel-2-l2a",
        item="S2A_MSIL2A_20230615T153901_N0509_R068_T18TWL_20230615T204701",
        assets="B04,B03,B02",  # 真彩色
        name="Sentinel-2 真彩色",
        opacity=0.8
    )
except:
    print("Sentinel-2数据不可用")

m_sensors
```

### 案例3: 专题分析波段组合测试

```python
# 创建专题分析地图
m_thematic = leafmap.Map(center=[37.0, -119.0], zoom=9)

# 定义不同用途的波段组合
band_combinations = {
    "植被分析": {
        "assets": "SR_B5,SR_B4,SR_B3",
        "description": "近红外-红-绿，突出植被"
    },
    "水体分析": {
        "assets": "SR_B5,SR_B6,SR_B4", 
        "description": "近红外-短波红外1-红，突出水体"
    },
    "城市分析": {
        "assets": "SR_B7,SR_B5,SR_B3",
        "description": "短波红外2-近红外-绿，突出城市"
    },
    "地质分析": {
        "assets": "SR_B7,SR_B6,SR_B4",
        "description": "短波红外2-短波红外1-红，突出地质"
    }
}

# 添加所有波段组合
for name, config in band_combinations.items():
    m_thematic.add_stac_layer(
        collection="landsat-8-c2-l2",
        item="LC08_L2SP_042034_20230701_02_T1",
        assets=config["assets"],
        name=f"{name} ({config['description']})",
        shown=False  # 默认不显示，用户可选择开启
    )

m_thematic
```

## 数据质量检查指南

### 1. 视觉质量评估

**检查要点**:
- **云覆盖**: 查看影像中的云层分布
- **条带噪声**: 检查是否存在传感器条带
- **色彩平衡**: 评估色彩是否自然
- **边界效应**: 检查影像边缘是否正常

**质量评估代码**:
```python
def assess_image_quality(collection, item):
    """评估影像质量"""
    m_quality = leafmap.Map()
    
    # 添加真彩色用于整体评估
    m_quality.add_stac_layer(
        collection=collection,
        item=item,
        assets="SR_B4,SR_B3,SR_B2",
        name="真彩色检查"
    )
    
    # 添加质量波段 (如果可用)
    try:
        m_quality.add_stac_layer(
            collection=collection,
            item=item,
            assets="QA_PIXEL",
            name="质量评估波段"
        )
    except:
        print("质量波段不可用")
    
    return m_quality

# 使用示例
quality_map = assess_image_quality("landsat-8-c2-l2", "LC08_L2SP_047027_20201204_02_T1")
quality_map
```

### 2. 光谱特征检查

```python
def check_spectral_features(collection, item):
    """检查光谱特征"""
    m_spectral = leafmap.Map()
    
    # 不同光谱区域的组合
    spectral_combinations = {
        "可见光": "SR_B4,SR_B3,SR_B2",
        "近红外": "SR_B5,SR_B4,SR_B3", 
        "短波红外": "SR_B7,SR_B6,SR_B5"
    }
    
    for name, assets in spectral_combinations.items():
        m_spectral.add_stac_layer(
            collection=collection,
            item=item,
            assets=assets,
            name=f"{name}组合",
            shown=(name == "可见光")  # 默认显示可见光
        )
    
    return m_spectral
```

### 3. 时间序列一致性检查

```python
def check_temporal_consistency(collection, items_list):
    """检查时间序列数据的一致性"""
    m_temporal = leafmap.Map()
    
    for i, (item, date_label) in enumerate(items_list):
        m_temporal.add_stac_layer(
            collection=collection,
            item=item,
            assets="SR_B5,SR_B4,SR_B3",
            name=f"{date_label}",
            opacity=0.8,
            shown=(i == 0)  # 默认只显示第一个
        )
    
    return m_temporal

# 使用示例
time_series_items = [
    ("LC08_L2SP_047027_20200401_02_T1", "2020年4月"),
    ("LC08_L2SP_047027_20200601_02_T1", "2020年6月"),
    ("LC08_L2SP_047027_20200801_02_T1", "2020年8月")
]

temporal_map = check_temporal_consistency("landsat-8-c2-l2", time_series_items)
temporal_map
```

## 常见问题与解决方案

### 1. 数据加载失败

**问题现象**: 图层无法显示或显示错误

**可能原因及解决方案**:

1. **无效的集合或项目ID**
```python
# 验证集合和项目是否存在
def verify_stac_item(collection, item):
    try:
        # 尝试获取项目信息
        import requests
        url = f"https://earth-search.aws.element84.com/v1/collections/{collection}/items/{item}"
        response = requests.get(url)
        
        if response.status_code == 200:
            print(f"✅ 项目 {item} 在集合 {collection} 中存在")
            return True
        else:
            print(f"❌ 项目不存在: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

# 使用验证
verify_stac_item("landsat-8-c2-l2", "LC08_L2SP_047027_20201204_02_T1")
```

2. **网络连接问题**
```python
# 网络连接测试
def test_network_connection():
    import requests
    import time
    
    test_urls = [
        "https://earth-search.aws.element84.com/v1/",
        "https://landsatlook.usgs.gov/stac-server/",
    ]
    
    for url in test_urls:
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)
            end_time = time.time()
            
            print(f"✅ {url}: {response.status_code} ({end_time-start_time:.2f}s)")
        except Exception as e:
            print(f"❌ {url}: {e}")

test_network_connection()
```

### 2. 波段组合显示异常

**问题现象**: 影像颜色异常或无法显示

**解决方案**:
```python
# 检查可用的资产
def check_available_assets(collection, item):
    try:
        import requests
        url = f"https://earth-search.aws.element84.com/v1/collections/{collection}/items/{item}"
        response = requests.get(url)
        
        if response.status_code == 200:
            item_data = response.json()
            assets = item_data.get('assets', {})
            
            print("可用资产:")
            for asset_name, asset_info in assets.items():
                print(f"  - {asset_name}: {asset_info.get('title', 'No title')}")
            
            return list(assets.keys())
        else:
            print("无法获取资产信息")
            return []
    except Exception as e:
        print(f"检查资产失败: {e}")
        return []

# 使用示例
available_assets = check_available_assets("landsat-8-c2-l2", "LC08_L2SP_047027_20201204_02_T1")
```

### 3. 性能问题

**问题现象**: 地图加载缓慢或卡顿

**优化方案**:
```python
# 性能优化的地图配置
def create_optimized_map():
    m_opt = leafmap.Map(
        # 限制初始缩放范围
        zoom=8,
        max_zoom=15,
        
        # 优化渲染
        prefer_canvas=True,
        
        # 减少控件
        draw_control=False,
        measure_control=False,
        fullscreen_control=False
    )
    
    return m_opt

# 分辨率适配
def add_layer_with_resolution_check(m, collection, item, assets, name):
    """根据缩放级别添加适当分辨率的图层"""
    current_zoom = m.zoom if hasattr(m, 'zoom') else 8
    
    if current_zoom > 12:
        # 高缩放级别，使用完整分辨率
        overview_level = None
    elif current_zoom > 8:
        # 中等缩放级别，使用中等分辨率
        overview_level = 1
    else:
        # 低缩放级别，使用低分辨率
        overview_level = 2
    
    m.add_stac_layer(
        collection=collection,
        item=item,
        assets=assets,
        name=name,
        overview_level=overview_level
    )
```

## 最佳实践建议

### 1. 数据检查流程

**标准检查步骤**:
1. **验证数据可用性** - 确认集合和项目存在
2. **加载真彩色组合** - 进行初步视觉检查
3. **测试假彩色组合** - 评估数据质量
4. **检查专题波段** - 根据应用需求选择
5. **记录检查结果** - 为后续处理做准备

### 2. 波段组合选择指南

**按应用目的选择**:
- **一般检查**: 4-3-2 (真彩色)
- **植被分析**: 5-4-3 (标准假彩色)
- **水体分析**: 5-6-4 (水体突出)
- **城市分析**: 7-5-3 (城市突出)
- **农业分析**: 6-5-2 (农业假彩色)

### 3. 质量控制标准

**数据接受标准**:
- 云覆盖 < 10% (严格应用)
- 云覆盖 < 30% (一般应用)
- 无明显条带噪声
- 色彩平衡正常
- 边界完整

**数据拒绝标准**:
- 云覆盖 > 50%
- 存在严重条带噪声
- 色彩严重失真
- 大面积数据缺失

---

*本使用手册提供了STAC数据检查工具的全面指导，帮助用户高效评估和选择合适的卫星遥感数据。*

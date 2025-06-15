# AWS开放数据交互式卫星影像搜索使用手册

## 功能概述

`01_ODP_Search.ipynb`展示了如何使用AWS开放数据进行交互式卫星影像搜索，基于STAC (SpatioTemporal Asset Catalog) 标准实现高效的时空数据查询。该notebook演示了从基础搜索到高级过滤的完整工作流程。

## 适用场景

- **遥感数据发现**: 快速找到特定区域和时间的卫星数据
- **时间序列分析**: 获取多时相数据进行变化检测
- **云量筛选**: 获取高质量的无云或少云影像
- **多源数据对比**: 比较不同卫星传感器的数据
- **灾害监测**: 快速获取灾前灾后影像数据

## 环境要求

### 软件依赖
```python
import os
import leafmap
```

### 网络要求
- 稳定的互联网连接
- 访问AWS开放数据平台的权限
- STAC API服务可用性

## 核心功能详解

### 1. 环境设置

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

**功能说明**:
- 设置工作目录为`tmp/`
- 提供完整的错误处理机制
- 确保后续文件操作的路径正确性

**最佳实践**:
- 始终使用异常处理确保程序稳定性
- 在处理大量数据前检查磁盘空间
- 建议使用绝对路径避免路径混淆

### 2. STAC搜索参数配置

```python
url = 'https://earth-search.aws.element84.com/v1/'
collection = 'sentinel-2-l2a'
time_range = "2020-12-01/2020-12-31"
bbox = [-122.2751, 47.5469, -121.9613, 47.7458]
```

#### 参数深度解析

**url参数 - STAC API端点**
- **数据类型**: 字符串
- **作用**: 指定STAC服务的API端点
- **常用端点**:
  - AWS Earth Search: `https://earth-search.aws.element84.com/v1/`
  - Microsoft Planetary Computer: `https://planetarycomputer.microsoft.com/api/stac/v1/`
  - Google Earth Engine: 通过专用接口访问

**collection参数 - 数据集合标识**
- **数据类型**: 字符串
- **作用**: 指定要搜索的卫星数据集合
- **常用集合**:
  - `'sentinel-2-l2a'`: Sentinel-2 L2A级产品 (大气校正后)
  - `'sentinel-2-l1c'`: Sentinel-2 L1C级产品 (辐射校正)
  - `'landsat-c2-l2'`: Landsat Collection 2 Level-2
  - `'cop-dem-glo-30'`: Copernicus DEM 30米分辨率

**time_range参数 - 时间范围**
- **数据类型**: 字符串
- **格式**: ISO 8601标准 "开始时间/结束时间"
- **示例**:
  - 单日: `"2020-12-15"`
  - 时间段: `"2020-12-01/2020-12-31"`
  - 开放结束: `"2020-12-01/.."`

**bbox参数 - 空间边界框**
- **数据类型**: 列表 [西经, 南纬, 东经, 北纬]
- **坐标系**: WGS84 (EPSG:4326)
- **示例区域**:
  - 西雅图: `[-122.2751, 47.5469, -121.9613, 47.7458]`
  - 北京: `[116.0, 39.5, 117.0, 40.5]`
  - 纽约: `[-74.5, 40.4, -73.7, 40.9]`

### 3. 基础STAC搜索

```python
search = leafmap.stac_search(
    url=url,
    max_items=10,
    collections=[collection],
    bbox=bbox,
    datetime=time_range,
    query={"eo:cloud_cover": {"lt": 10}},
    sortby=[{'field': 'properties.eo:cloud_cover', 'direction': 'asc'}],
)
```

#### 高级参数详解

**max_items参数 - 结果数量限制**
- **数据类型**: 整数
- **默认值**: 10
- **作用**: 限制返回的搜索结果数量
- **性能考虑**:
  - 小值(1-10): 快速预览，适合测试
  - 中值(10-100): 常规分析使用
  - 大值(100+): 大规模数据处理，注意内存使用

**query参数 - 属性过滤**
- **数据类型**: 字典
- **作用**: 基于元数据属性进行过滤
- **常用过滤条件**:
```python
# 云量过滤
{"eo:cloud_cover": {"lt": 10}}  # 小于10%

# 多条件过滤
{
    "eo:cloud_cover": {"lt": 20},
    "view:sun_elevation": {"gt": 30}
}

# 范围过滤
{"datetime": {"gte": "2020-06-01", "lte": "2020-08-31"}}
```

**sortby参数 - 结果排序**
- **数据类型**: 列表
- **作用**: 指定搜索结果的排序方式
- **排序选项**:
```python
# 按云量升序
[{'field': 'properties.eo:cloud_cover', 'direction': 'asc'}]

# 按时间降序
[{'field': 'properties.datetime', 'direction': 'desc'}]

# 多字段排序
[
    {'field': 'properties.eo:cloud_cover', 'direction': 'asc'},
    {'field': 'properties.datetime', 'direction': 'desc'}
]
```

### 4. 不同输出格式的搜索

#### 4.1 获取集合信息
```python
search = leafmap.stac_search(
    url=url,
    max_items=10,
    collections=[collection],
    bbox=bbox,
    datetime=time_range,
    get_collection=True,  # 获取集合元数据
)
```

**应用场景**:
- 了解数据集的基本信息
- 查看可用的波段和属性
- 确认数据的空间和时间覆盖范围

#### 4.2 获取GeoDataFrame格式
```python
search = leafmap.stac_search(
    url=url,
    max_items=10,
    collections=[collection],
    bbox=bbox,
    datetime=time_range,
    get_gdf=True,  # 返回GeoDataFrame
)
search.head()  # 查看前5行
```

**GeoDataFrame优势**:
- 支持空间数据分析
- 易于数据筛选和统计
- 可直接用于地图可视化
- 支持导出为多种格式

#### 4.3 获取资产信息
```python
search = leafmap.stac_search(
    url=url,
    max_items=10,
    collections=[collection],
    bbox=bbox,
    datetime=time_range,
    get_assets=True,  # 获取详细资产信息
)
```

**资产信息包含**:
- 各波段的下载链接
- 文件大小和格式信息
- 数据质量标识
- 处理级别说明

#### 4.4 获取详细信息
```python
search = leafmap.stac_search(
    url=url,
    max_items=10,
    collections=[collection],
    bbox=bbox,
    datetime=time_range,
    get_info=True,  # 获取完整信息
)
```

#### 4.5 获取相关链接
```python
search = leafmap.stac_search(
    url=url,
    max_items=10,
    collections=[collection],
    bbox=bbox,
    datetime=time_range,
    get_links=True,  # 获取相关链接
)
```

### 5. 交互式地图可视化

```python
m = leafmap.Map(
    center=[37.7517, -122.4433], 
    zoom=8,
    attribution_control=False,
)
m
```

#### 地图集成功能

**搜索结果访问**:
```python
# 访问搜索结果的不同格式
m.stac_gdf    # GeoDataFrame格式的搜索结果
m.stac_dict   # 字典格式的搜索结果  
m.stac_item   # 选中的STAC项目
```

## 实际应用案例

### 案例1: 农业监测数据获取

```python
# 配置农业区域搜索参数
agricultural_bbox = [-120.5, 36.0, -119.5, 37.0]  # 加州中央谷地
growing_season = "2023-04-01/2023-09-30"

# 搜索Sentinel-2数据
farm_search = leafmap.stac_search(
    url='https://earth-search.aws.element84.com/v1/',
    max_items=50,
    collections=['sentinel-2-l2a'],
    bbox=agricultural_bbox,
    datetime=growing_season,
    query={
        "eo:cloud_cover": {"lt": 15},  # 低云量
        "s2:vegetation_percentage": {"gt": 50}  # 高植被覆盖
    },
    sortby=[
        {'field': 'properties.datetime', 'direction': 'asc'}
    ],
    get_gdf=True
)

# 分析结果
print(f"找到 {len(farm_search)} 个适合农业监测的影像")
print(f"时间跨度: {farm_search['datetime'].min()} 到 {farm_search['datetime'].max()}")
```

### 案例2: 灾害监测数据搜索

```python
# 灾害区域和时间设置
disaster_bbox = [35.0, 38.0, 37.0, 40.0]  # 土耳其地震区域
pre_disaster = "2023-01-01/2023-02-05"
post_disaster = "2023-02-07/2023-02-28"

# 搜索灾前数据
pre_search = leafmap.stac_search(
    url='https://earth-search.aws.element84.com/v1/',
    max_items=20,
    collections=['sentinel-2-l2a'],
    bbox=disaster_bbox,
    datetime=pre_disaster,
    query={"eo:cloud_cover": {"lt": 30}},
    get_gdf=True
)

# 搜索灾后数据
post_search = leafmap.stac_search(
    url='https://earth-search.aws.element84.com/v1/',
    max_items=20,
    collections=['sentinel-2-l2a'],
    bbox=disaster_bbox,
    datetime=post_disaster,
    query={"eo:cloud_cover": {"lt": 30}},
    get_gdf=True
)

print(f"灾前影像: {len(pre_search)} 个")
print(f"灾后影像: {len(post_search)} 个")
```

### 案例3: 多源数据对比搜索

```python
# 同一区域的多源数据搜索
study_area = [-74.0, 40.7, -73.9, 40.8]  # 纽约曼哈顿
time_period = "2023-07-01/2023-07-31"

# Sentinel-2数据
s2_search = leafmap.stac_search(
    url='https://earth-search.aws.element84.com/v1/',
    collections=['sentinel-2-l2a'],
    bbox=study_area,
    datetime=time_period,
    query={"eo:cloud_cover": {"lt": 10}},
    get_gdf=True
)

# Landsat数据
landsat_search = leafmap.stac_search(
    url='https://earth-search.aws.element84.com/v1/',
    collections=['landsat-c2-l2'],
    bbox=study_area,
    datetime=time_period,
    query={"eo:cloud_cover": {"lt": 10}},
    get_gdf=True
)

# 对比分析
print("数据源对比:")
print(f"Sentinel-2: {len(s2_search)} 个影像, 分辨率: 10-60m")
print(f"Landsat: {len(landsat_search)} 个影像, 分辨率: 15-100m")
```

## 性能优化策略

### 1. 搜索参数优化

```python
# 高效搜索的参数配置
optimized_search = leafmap.stac_search(
    url=url,
    max_items=20,  # 适中的数量
    collections=[collection],
    bbox=bbox,
    datetime=time_range,
    query={
        "eo:cloud_cover": {"lt": 20},  # 合理的云量阈值
    },
    sortby=[{'field': 'properties.eo:cloud_cover', 'direction': 'asc'}],
    get_gdf=True,  # 直接获取需要的格式
)
```

### 2. 网络优化

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 配置重试策略
session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)
```

### 3. 内存管理

```python
# 分批处理大量搜索结果
def batch_search(bbox, datetime, batch_size=50):
    all_results = []
    offset = 0
    
    while True:
        batch_search = leafmap.stac_search(
            url=url,
            max_items=batch_size,
            collections=[collection],
            bbox=bbox,
            datetime=datetime,
            offset=offset,
            get_gdf=True
        )
        
        if len(batch_search) == 0:
            break
            
        all_results.append(batch_search)
        offset += batch_size
        
        # 内存清理
        if len(all_results) % 10 == 0:
            import gc
            gc.collect()
    
    return pd.concat(all_results, ignore_index=True)
```

## 常见问题与解决方案

### 1. 搜索结果为空

**问题现象**: 搜索返回0个结果

**可能原因及解决方案**:

1. **时间范围问题**
```python
# 检查数据集的时间覆盖范围
collection_info = leafmap.stac_search(
    url=url,
    collections=[collection],
    get_collection=True
)
print("数据集时间范围:", collection_info['extent']['temporal'])

# 调整时间范围
time_range = "2020-01-01/2023-12-31"  # 扩大时间范围
```

2. **空间范围问题**
```python
# 检查边界框格式 [西经, 南纬, 东经, 北纬]
bbox = [-122.5, 47.0, -121.5, 48.0]  # 确保西经 < 东经, 南纬 < 北纬

# 验证坐标系统
import geopandas as gpd
from shapely.geometry import box

# 创建边界框几何体验证
bbox_geom = box(*bbox)
print(f"边界框面积: {bbox_geom.area:.6f} 平方度")
```

3. **过滤条件过严**
```python
# 放宽过滤条件
query = {
    "eo:cloud_cover": {"lt": 50},  # 从10%放宽到50%
}
```

### 2. API访问错误

**问题现象**: HTTP错误或超时

**解决方案**:
```python
import time
import random

def robust_search(search_params, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = leafmap.stac_search(**search_params)
            return result
        except Exception as e:
            print(f"尝试 {attempt + 1} 失败: {e}")
            if attempt < max_retries - 1:
                # 指数退避
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait_time)
            else:
                raise e
```

### 3. 内存不足

**问题现象**: 处理大量搜索结果时内存溢出

**解决方案**:
```python
# 使用生成器处理大数据集
def search_generator(search_params, batch_size=10):
    offset = 0
    while True:
        batch_params = search_params.copy()
        batch_params.update({
            'max_items': batch_size,
            'offset': offset
        })
        
        batch_result = leafmap.stac_search(**batch_params)
        if len(batch_result) == 0:
            break
            
        yield batch_result
        offset += batch_size

# 使用生成器
for batch in search_generator(search_params):
    # 处理每个批次
    process_batch(batch)
```

## 最佳实践建议

### 1. 搜索策略

- **渐进式搜索**: 先用宽松条件搜索，再逐步细化
- **时空平衡**: 在时间范围和空间范围之间找到平衡
- **质量优先**: 优先选择云量低、质量高的影像
- **多源验证**: 使用多个数据源进行交叉验证

### 2. 数据管理

- **元数据记录**: 保存搜索参数和结果元数据
- **版本控制**: 记录数据获取的时间和版本
- **质量检查**: 下载前检查数据质量指标
- **存储优化**: 合理组织数据存储结构

### 3. 性能优化

- **缓存机制**: 缓存常用的搜索结果
- **并行处理**: 对于大规模搜索使用并行策略
- **网络优化**: 使用CDN和镜像服务
- **资源监控**: 监控内存和网络使用情况

---

*本使用手册提供了STAC数据搜索的全面指导，帮助用户高效获取和管理卫星遥感数据。*

# CSV数据与OpenStreetMap集成使用手册

## 功能概述

`0A_CSV_OSM.ipynb`演示了如何处理CSV格式的地理数据，并与OpenStreetMap (OSM)数据进行集成分析，实现表格数据的地理可视化和空间分析。

## 核心功能

### 1. CSV数据处理
```python
import pandas as pd
import geopandas as gpd

# 读取CSV数据
df = pd.read_csv('data.csv')

# 转换为地理数据
gdf = gpd.GeoDataFrame(
    df, 
    geometry=gpd.points_from_xy(df.longitude, df.latitude)
)
```

### 2. 地理编码功能
- **地址转坐标**: 将文本地址转换为经纬度坐标
- **反向地理编码**: 将坐标转换为地址信息
- **批量处理**: 支持大量地址的批量转换
- **精度控制**: 可设置地理编码的精度要求

### 3. OSM数据集成
```python
import osmnx as ox

# 获取OSM数据
graph = ox.graph_from_place("Beijing, China", network_type='all')
buildings = ox.geometries_from_place("Beijing, China", tags={'building': True})
```

### 4. 空间分析功能
- **缓冲区分析**: 创建点、线、面的缓冲区
- **空间连接**: 将CSV点数据与OSM面数据连接
- **距离计算**: 计算点与点、点与线的距离
- **包含关系**: 判断点是否在多边形内

## 数据处理流程

### 1. 数据导入和清洗
```python
# 数据质量检查
def check_data_quality(df):
    print(f"数据行数: {len(df)}")
    print(f"缺失值: {df.isnull().sum()}")
    print(f"重复值: {df.duplicated().sum()}")
    
    # 坐标有效性检查
    valid_coords = (
        (df['latitude'].between(-90, 90)) & 
        (df['longitude'].between(-180, 180))
    )
    print(f"有效坐标: {valid_coords.sum()}/{len(df)}")
```

### 2. 地理可视化
```python
import leafmap

m = leafmap.Map()
m.add_gdf(gdf, layer_name="CSV数据点")
m.add_basemap("OpenStreetMap")
```

## 应用场景

### 1. 商业网点分析
- **选址分析**: 基于人口密度和交通便利性
- **竞争分析**: 分析竞争对手分布
- **服务范围**: 计算服务覆盖范围
- **客户分析**: 客户地理分布特征

### 2. 人口统计数据可视化
- **人口密度**: 人口分布热力图
- **年龄结构**: 不同区域年龄结构对比
- **收入分布**: 收入水平地理分布
- **教育水平**: 教育程度空间分析

### 3. 交通流量分析
- **流量统计**: 交通流量时空分布
- **拥堵分析**: 交通拥堵热点识别
- **路网分析**: 道路网络连通性分析
- **公交规划**: 公交线路优化建议

### 4. 环境监测站点管理
- **站点分布**: 监测站点空间分布
- **覆盖分析**: 监测覆盖范围评估
- **数据质量**: 站点数据质量评估
- **网络优化**: 监测网络优化建议

## 技术实现要点

### 1. 坐标系统处理
```python
# 坐标系转换
gdf_utm = gdf.to_crs('EPSG:32633')  # 转换为UTM坐标系
gdf_wgs84 = gdf_utm.to_crs('EPSG:4326')  # 转换回WGS84
```

### 2. 空间索引优化
```python
# 创建空间索引提高查询效率
gdf_indexed = gdf.sindex
```

### 3. 大数据处理
```python
# 分块处理大型CSV文件
chunk_size = 10000
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    process_chunk(chunk)
```

---

*详细代码实现和高级空间分析功能正在完善中...*

# 底图管理使用手册

## 功能概述

`0B_Basemap.ipynb`专注于地图底图的管理和配置，包括多种底图源的集成、自定义底图创建和底图切换功能。

## 核心功能

### 1. 多底图源支持
```python
import leafmap

# 常用底图类型
basemaps = {
    'OpenStreetMap': 'OpenStreetMap',
    'Google Satellite': 'SATELLITE',
    'Google Terrain': 'TERRAIN', 
    'Esri World Imagery': 'Esri.WorldImagery',
    'CartoDB Positron': 'CartoDB.Positron'
}

m = leafmap.Map()
for name, basemap in basemaps.items():
    m.add_basemap(basemap)
```

### 2. 底图切换控制
- **图层控制器**: 动态切换不同底图
- **透明度调节**: 调整底图透明度
- **混合显示**: 多个底图叠加显示
- **自定义样式**: 修改底图显示样式

### 3. 自定义底图创建
```python
# 添加自定义XYZ瓦片服务
custom_url = "https://server.com/tiles/{z}/{x}/{y}.png"
m.add_tile_layer(
    url=custom_url,
    name="Custom Basemap",
    attribution="Custom Data Source"
)
```

### 4. 底图性能优化
- **缓存策略**: 本地瓦片缓存
- **加载优化**: 按需加载瓦片
- **分辨率控制**: 根据缩放级别调整
- **网络优化**: CDN加速和镜像服务

## 底图类型详解

### 1. 街道地图类
- **OpenStreetMap**: 开源街道地图
- **Google Maps**: Google标准地图
- **Bing Maps**: 微软地图服务
- **Here Maps**: Here地图服务

### 2. 卫星影像类
- **Google Satellite**: Google卫星影像
- **Esri World Imagery**: Esri全球影像
- **Bing Aerial**: 微软航空影像
- **Mapbox Satellite**: Mapbox卫星底图

### 3. 地形图类
- **OpenTopoMap**: 开源地形图
- **Google Terrain**: Google地形图
- **USGS Topo**: 美国地质调查局地形图
- **Swiss Topo**: 瑞士地形图

### 4. 专题地图类
- **CartoDB Dark**: 深色主题地图
- **CartoDB Positron**: 浅色简洁地图
- **Stamen Watercolor**: 水彩风格地图
- **Stamen Toner**: 黑白风格地图

## 应用配置示例

### 1. 科研用途配置
```python
# 科研分析专用底图
m_research = leafmap.Map()
m_research.add_basemap("CartoDB.Positron")  # 简洁底图不干扰数据
m_research.add_basemap("OpenTopoMap")       # 地形参考
```

### 2. 商业展示配置
```python
# 商业展示用底图
m_business = leafmap.Map()
m_business.add_basemap("Esri.WorldImagery")  # 高质量卫星影像
m_business.add_basemap("Google.Satellite")   # 备用卫星底图
```

### 3. 教学演示配置
```python
# 教学用多样化底图
m_education = leafmap.Map()
basemap_list = [
    "OpenStreetMap",
    "SATELLITE", 
    "TERRAIN",
    "CartoDB.Positron"
]
for basemap in basemap_list:
    m_education.add_basemap(basemap)
```

---

*详细底图配置和自定义底图创建正在完善中...*

# 地理科学解决方案包 - 数据可视化功能深度解析

## 1. COG图层加载功能

### 1.1 基础COG图层添加

```python
m = leafmap.Map()
url = 'https://opendata.digitalglobe.com/events/california-fire-2020/pre-event/2018-02-16/pine-gulch-fire20/1030010076004E00.tif'
m.add_cog_layer(url, name="Fire (pre-event)")
```

#### 参数深度解析

**url参数 - COG数据源地址**
- **数据类型**: 字符串
- **支持协议**: HTTP/HTTPS, S3, GCS等
- **文件格式**: 云优化GeoTIFF (.tif)
- **示例**: 
  - 本地文件: `"file:///path/to/data.tif"`
  - HTTP服务: `"https://example.com/data.tif"`
  - S3存储: `"s3://bucket/data.tif"`

**name参数 - 图层显示名称**
- **数据类型**: 字符串
- **默认值**: 自动从URL提取
- **作用**: 图层控制面板中的显示名称
- **最佳实践**: 使用描述性名称，如"火灾前影像"、"2020年土地覆盖"

#### 高级参数配置

```python
m.add_cog_layer(
    url=cog_url,
    name="详细图层名称",
    bands=[1, 2, 3],           # 波段选择
    vmin=0,                    # 最小显示值
    vmax=255,                  # 最大显示值
    nodata=0,                  # 无数据值
    opacity=0.8,               # 透明度
    gamma=1.0,                 # 伽马校正
    fit_bounds=True,           # 自动缩放到数据范围
)
```

**bands参数效果对比**:
```python
# 真彩色显示 (RGB)
m.add_cog_layer(url, bands=[4, 3, 2], name="真彩色")

# 假彩色显示 (近红外)
m.add_cog_layer(url, bands=[5, 4, 3], name="假彩色")

# 单波段灰度显示
m.add_cog_layer(url, bands=[1], name="灰度")
```

## 2. STAC图层集成功能

### 2.1 STAC数据加载

```python
m = leafmap.Map()
url = 'https://canada-spot-ortho.s3.amazonaws.com/canada_spot_orthoimages/canada_spot5_orthoimages/S5_2007/S5_11055_6057_20070622/S5_11055_6057_20070622.json'
m.add_stac_layer(url, bands=['B3', 'B2', 'B1'], name='False color')
```

#### STAC标准优势

**标准化元数据**:
- 统一的数据描述格式
- 丰富的时空信息
- 标准化的访问接口

**多源数据集成**:
- 支持不同卫星数据
- 统一的数据访问方式
- 便于数据发现和使用

#### 波段组合应用

```python
# 不同波段组合的视觉效果
combinations = {
    "真彩色": ['B4', 'B3', 'B2'],      # 红绿蓝
    "假彩色": ['B5', 'B4', 'B3'],      # 近红外、红、绿
    "植被指数": ['B5', 'B6', 'B4'],    # 植被分析
    "城市分析": ['B7', 'B5', 'B3'],    # 城市建设
}

for name, bands in combinations.items():
    m.add_stac_layer(url, bands=bands, name=name)
```

## 3. WMS服务集成

### 3.1 标准WMS图层

```python
m = leafmap.Map(center=[40, -100], zoom=4)
naip_url = 'https://www.mrlc.gov/geoserver/mrlc_display/NLCD_2019_Land_Cover_L48/wms?'
m.add_wms_layer(
    url=naip_url,
    layers='NLCD_2019_Land_Cover_L48',
    name='NLCD 2019',
    attribution='MRLC',
    format='image/png',
    shown=True,
)
```

#### WMS参数详解

**layers参数 - 图层标识**
- **数据类型**: 字符串或列表
- **作用**: 指定要显示的WMS图层
- **多图层**: `layers=['layer1', 'layer2']`
- **获取方式**: 通过GetCapabilities请求获取

**format参数 - 图像格式**
- **image/png**: 支持透明度，适合叠加
- **image/jpeg**: 文件较小，适合底图
- **image/gif**: 支持动画，适合时序数据

**transparent参数效果对比**:
```python
# 不透明图层 - 适合作为底图
m.add_wms_layer(url, layers='base_layer', transparent=False)

# 透明图层 - 适合数据叠加
m.add_wms_layer(url, layers='overlay_layer', transparent=True)
```

## 4. 矢量数据可视化

### 4.1 GeoJSON数据处理

#### 基础GeoJSON加载
```python
m = leafmap.Map(center=[0, 0], zoom=2)
in_geojson = 'https://raw.githubusercontent.com/opengeos/leafmap/master/examples/data/cable_geo.geojson'
m.add_geojson(in_geojson, layer_name="Cable lines")
```

#### 样式自定义
```python
# 自定义样式配置
style = {
    "stroke": True,           # 显示边框
    "color": "#0000ff",       # 边框颜色
    "weight": 2,              # 边框宽度
    "opacity": 1,             # 边框透明度
    "fill": True,             # 填充
    "fillColor": "#0000ff",   # 填充颜色
    "fillOpacity": 0.1,       # 填充透明度
}

hover_style = {"fillOpacity": 0.7}  # 鼠标悬停样式

m.add_geojson(url, layer_name="Countries", style=style, hover_style=hover_style)
```

#### 颜色映射功能
```python
# 随机颜色填充
m.add_geojson(
    url,
    layer_name="Countries",
    style={'fillOpacity': 0.5},
    fill_colors=['red', 'yellow', 'green', 'orange'],
)
```

**颜色参数详解**:
- **固定颜色**: 所有要素使用相同颜色
- **随机颜色**: 从颜色列表中随机选择
- **属性映射**: 根据要素属性值映射颜色

## 5. 热力图生成

### 5.1 点数据热力图

```python
m = leafmap.Map()
in_csv = "https://raw.githubusercontent.com/opengeos/leafmap/master/examples/data/world_cities.csv"
m.add_heatmap(
    in_csv,
    latitude="latitude",
    longitude='longitude',
    value="pop_max",
    name="Heat map",
    radius=20,
)
```

#### 热力图参数优化

**radius参数 - 影响半径**
- **取值范围**: 5-50像素
- **效果对比**:
  - 小半径(5-15): 精确定位，适合密集数据
  - 中半径(15-25): 平衡效果，通用场景
  - 大半径(25-50): 平滑效果，稀疏数据

```python
# 不同半径效果对比
for radius in [10, 20, 30]:
    m.add_heatmap(
        data, 
        radius=radius, 
        name=f"热力图_半径{radius}"
    )
```

**value参数 - 权重字段**
- **数值字段**: 人口、收入、温度等
- **归一化**: 自动处理数值范围
- **缺失值**: 自动忽略空值

## 6. 图例和色标系统

### 6.1 内置图例

```python
m.add_legend(builtin_legend='NLCD')
```

**内置图例类型**:
- `'NLCD'`: 美国土地覆盖分类
- `'ESA_WorldCover'`: ESA全球土地覆盖
- `'MODIS_LC'`: MODIS土地覆盖类型

### 6.2 自定义色标

```python
colors = ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']
vmin = 0
vmax = 4000
m.add_colorbar(colors=colors, vmin=vmin, vmax=vmax)
```

#### 色标设计原则

**颜色选择**:
- **连续数据**: 使用渐变色系
- **分类数据**: 使用对比色系
- **科学可视化**: 遵循ColorBrewer标准

**数值范围设置**:
```python
# 基于数据统计的范围设置
import numpy as np
data_array = np.array([...])  # 你的数据
vmin = np.percentile(data_array, 2)   # 2%分位数
vmax = np.percentile(data_array, 98)  # 98%分位数
```

## 7. 实际应用案例

### 7.1 环境监测应用

```python
# 空气质量监测
m = leafmap.Map(center=[39.9, 116.4], zoom=8)

# 添加监测站点
stations_geojson = "air_quality_stations.geojson"
m.add_geojson(
    stations_geojson,
    style={"color": "red", "radius": 8},
    layer_name="监测站点"
)

# 添加污染浓度热力图
pollution_csv = "pollution_data.csv"
m.add_heatmap(
    pollution_csv,
    latitude="lat",
    longitude="lon", 
    value="pm25",
    radius=25,
    name="PM2.5浓度分布"
)

# 添加色标
m.add_colorbar(
    colors=['green', 'yellow', 'orange', 'red', 'purple'],
    vmin=0, vmax=300,
    caption="PM2.5浓度 (μg/m³)"
)
```

### 7.2 灾害监测应用

```python
# 洪水监测
m = leafmap.Map(center=[30.5, 114.3], zoom=10)

# 灾前影像
pre_disaster_url = "pre_flood_image.tif"
m.add_cog_layer(
    pre_disaster_url,
    bands=[4, 3, 2],
    name="灾前影像",
    opacity=0.7
)

# 灾后影像
post_disaster_url = "post_flood_image.tif" 
m.add_cog_layer(
    post_disaster_url,
    bands=[4, 3, 2],
    name="灾后影像",
    opacity=0.7
)

# 受灾区域
flood_extent = "flood_boundary.geojson"
m.add_geojson(
    flood_extent,
    style={"color": "blue", "fillOpacity": 0.3},
    layer_name="淹没范围"
)
```

## 8. 性能优化策略

### 8.1 大数据处理

```python
# COG数据优化
m.add_cog_layer(
    large_cog_url,
    overview_level=2,      # 使用概览级别
    max_zoom=12,           # 限制最大缩放
    tile_size=512,         # 优化瓦片大小
)
```

### 8.2 网络优化

```python
# 启用数据缓存
import os
os.environ['GDAL_DISABLE_READDIR_ON_OPEN'] = 'EMPTY_DIR'
os.environ['CPL_VSIL_CURL_CACHE_SIZE'] = '200000000'
```

---

*本文档详细解析了数据可视化功能的各个方面，为用户提供了全面的参数配置和应用指导。*

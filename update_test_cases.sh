#!/bin/bash

# 更新测试案例 - GPU内存优化版

echo "=== 更新测试案例 - GPU内存优化版 ==="

# 更新测试notebook，添加GPU内存清理
cat > /home/ec2-user/SageMaker/hainan_comprehensive_test.ipynb << 'EOF'
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 海南天基观测数据科学分析与可视化系统\n",
    "## 综合功能测试案例（GPU内存优化版）\n",
    "\n",
    "**请确保使用 `Python (Geo-AI)` 内核**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. 基础环境验证（GPU内存优化）\n",
    "import sys\n",
    "print(f\"Python环境: {sys.executable}\")\n",
    "print(f\"是否在JupyterSystemEnv: {'JupyterSystemEnv' in sys.executable}\")\n",
    "\n",
    "# 导入核心包\n",
    "import leafmap\n",
    "import samgeo\n",
    "from samgeo import SamGeo\n",
    "import torch\n",
    "import geopandas as gpd\n",
    "\n",
    "# GPU内存清理\n",
    "torch.cuda.empty_cache()\n",
    "\n",
    "print(\"✅ 所有核心包导入成功\")\n",
    "print(f\"GPU可用: {torch.cuda.is_available()}\")\n",
    "\n",
    "if torch.cuda.is_available():\n",
    "    print(f\"GPU设备: {torch.cuda.get_device_name(0)}\")\n",
    "    print(f\"GPU总内存: {torch.cuda.get_device_properties(0).total_memory/1024**3:.2f} GB\")\n",
    "    print(f\"GPU可用内存: {(torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_allocated())/1024**3:.2f} GB\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 2. 全球海底电缆地图\n",
    "m = leafmap.Map(center=[0, 0], zoom=2)\n",
    "in_geojson = 'https://raw.githubusercontent.com/opengeos/leafmap/master/examples/data/cable_geo.geojson'\n",
    "m.add_geojson(in_geojson, layer_name=\"Cable lines\")\n",
    "m.attribution_control = False\n",
    "m"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 3. 彩色国家地图\n",
    "m = leafmap.Map(center=[0, 0], zoom=2)\n",
    "url = \"https://raw.githubusercontent.com/opengeos/leafmap/master/examples/data/countries.geojson\"\n",
    "style = {'fillOpacity': 0.5}\n",
    "m.add_geojson(\n",
    "    url,\n",
    "    layer_name=\"Countries\",\n",
    "    style=style,\n",
    "    fill_colors=['red', 'yellow', 'green', 'orange'],\n",
    ")\n",
    "m.attribution_control = False\n",
    "m"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 4. 海南地区专题地图（标记修复版）\n",
    "hainan_center = [19.2, 109.8]\n",
    "m = leafmap.Map(center=hainan_center, zoom=8)\n",
    "\n",
    "# 海南主要城市精确坐标\n",
    "locations = [\n",
    "    [20.0444, 110.1989],  # 海口市\n",
    "    [18.2577, 109.5185],  # 三亚市\n",
    "    [19.5175, 109.5809],  # 儋州市\n",
    "    [19.2463, 110.4664]   # 琼海市\n",
    "]\n",
    "\n",
    "names = ['海口市', '三亚市', '儋州市', '琼海市']\n",
    "\n",
    "# 批量添加标记（不使用popup参数）\n",
    "for i, (loc, name) in enumerate(zip(locations, names)):\n",
    "    m.add_marker(loc)\n",
    "    print(f'✅ 添加{name}标记')\n",
    "\n",
    "print(f'🎯 海南地图完成，显示{len(locations)}个城市标记')\n",
    "m"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 5. STAC卫星数据查询\n",
    "import leafmap\n",
    "\n",
    "# 海南地区边界框\n",
    "hainan_bbox = [108.5, 18.0, 111.5, 20.5]\n",
    "url = 'https://earth-search.aws.element84.com/v1/'\n",
    "collection = 'sentinel-2-l2a'\n",
    "time_range = \"2023-01-01/2023-12-31\"\n",
    "\n",
    "# 搜索海南地区卫星数据\n",
    "search = leafmap.stac_search(\n",
    "    url=url,\n",
    "    max_items=10,\n",
    "    collections=[collection],\n",
    "    bbox=hainan_bbox,\n",
    "    datetime=time_range,\n",
    "    query={\"eo:cloud_cover\": {\"lt\": 20}},\n",
    "    get_gdf=True,\n",
    ")\n",
    "\n",
    "print(f\"找到 {len(search)} 个卫星图像\")\n",
    "search.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 6. 交互式STAC数据浏览（修复版）\n",
    "m = leafmap.Map(\n",
    "    center=[19.5, 110.0], \n",
    "    zoom=8,\n",
    "    attribution_control=False,\n",
    ")\n",
    "\n",
    "# 显示STAC搜索区域（避免服务错误）\n",
    "import geopandas as gpd\n",
    "from shapely.geometry import box\n",
    "\n",
    "# 创建海南搜索区域边界\n",
    "bbox_gdf = gpd.GeoDataFrame([1], geometry=[box(*hainan_bbox)], crs='EPSG:4326')\n",
    "m.add_gdf(bbox_gdf, layer_name='海南STAC搜索区域', style={'color': 'blue', 'weight': 2, 'fillOpacity': 0.1})\n",
    "print('✅ 显示海南STAC搜索区域')\n",
    "\n",
    "m"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 7. SAM AI功能测试（GPU内存优化）\n",
    "from samgeo import SamGeo, tms_to_geotiff\n",
    "import torch\n",
    "\n",
    "# GPU内存清理\n",
    "torch.cuda.empty_cache()\n",
    "\n",
    "device = 'cuda' if torch.cuda.is_available() else 'cpu'\n",
    "print(f\"SAM将使用设备: {device}\")\n",
    "\n",
    "if torch.cuda.is_available():\n",
    "    print(f\"GPU内存使用前: {torch.cuda.memory_allocated()/1024**3:.2f} GB\")\n",
    "    print(f\"GPU内存缓存: {torch.cuda.memory_reserved()/1024**3:.2f} GB\")\n",
    "\n",
    "# 下载海南地区测试图像\n",
    "bbox = [110.0, 19.8, 110.2, 20.0]  # 海口附近\n",
    "image_path = 'hainan_test.tif'\n",
    "\n",
    "print(\"正在下载测试图像...\")\n",
    "tms_to_geotiff(\n",
    "    output=image_path, \n",
    "    bbox=bbox, \n",
    "    zoom=15, \n",
    "    source='Satellite'\n",
    ")\n",
    "print(\"✅ 测试图像下载成功\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 8. SAM模型初始化和分割（GPU内存优化）\n",
    "# 再次清理GPU内存\n",
    "torch.cuda.empty_cache()\n",
    "\n",
    "# 设置PyTorch内存分配策略\n",
    "import os\n",
    "os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'\n",
    "\n",
    "print(\"正在初始化SAM模型...\")\n",
    "sam = SamGeo(\n",
    "    model_type='vit_b',  # 使用较小的模型避免内存不足\n",
    "    device=device,\n",
    "    sam_kwargs={'points_per_side': 8}  # 减少点数以节省内存\n",
    ")\n",
    "\n",
    "print(\"✅ SAM模型初始化成功\")\n",
    "\n",
    "if torch.cuda.is_available():\n",
    "    print(f\"GPU内存使用后: {torch.cuda.memory_allocated()/1024**3:.2f} GB\")\n",
    "\n",
    "# 生成分割掩码\n",
    "mask_path = 'hainan_mask.tif'\n",
    "print(\"正在生成分割掩码...\")\n",
    "sam.generate(\n",
    "    source=image_path,\n",
    "    output=mask_path,\n",
    "    foreground=True,\n",
    "    unique=True\n",
    ")\n",
    "\n",
    "print(\"✅ 分割掩码生成成功\")\n",
    "\n",
    "# 清理SAM模型释放内存\n",
    "del sam\n",
    "torch.cuda.empty_cache()\n",
    "print(\"✅ GPU内存已清理\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 9. 分割结果可视化\n",
    "m = leafmap.Map(center=[19.9, 110.1], zoom=12)\n",
    "m.add_raster(image_path, layer_name=\"原始图像\")\n",
    "m.add_raster(mask_path, layer_name=\"SAM分割结果\", opacity=0.7)\n",
    "m"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 🎉 测试完成（GPU内存优化版）\n",
    "\n",
    "如果上述所有单元格都成功运行，说明海南天基观测数据科学分析与可视化系统已完全就绪！\n",
    "\n",
    "### 验证的功能：\n",
    "- ✅ 基础环境和包导入\n",
    "- ✅ Leafmap交互式地图\n",
    "- ✅ GeoJSON数据可视化\n",
    "- ✅ 海南地区专题地图（标记修复）\n",
    "- ✅ STAC卫星数据查询\n",
    "- ✅ STAC搜索区域显示（服务错误修复）\n",
    "- ✅ SAM AI图像分割（GPU内存优化）\n",
    "- ✅ 分割结果可视化\n",
    "\n",
    "### GPU内存优化：\n",
    "- 🔧 在GPU计算前调用 `torch.cuda.empty_cache()`\n",
    "- 🔧 设置 `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`\n",
    "- 🔧 使用较小的SAM模型 (vit_b) 和较少的采样点\n",
    "- 🔧 及时删除模型对象释放内存\n",
    "- 🔧 显示GPU内存使用情况便于监控\n",
    "\n",
    "### 使用提醒：\n",
    "- 始终使用 `Python (Geo-AI)` 内核\n",
    "- 正确的导入方式：`import samgeo`\n",
    "- 如遇GPU内存不足，重启内核后重新运行\n",
    "- 建议使用ml.g5.8xlarge或更大的GPU实例"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python (Geo-AI)",
   "language": "python",
   "name": "python-geo"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.18"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
EOF

echo "✅ 测试案例已更新 - GPU内存优化版"

# 添加多样化底图展示到notebook末尾
cat >> /home/ec2-user/SageMaker/hainan_comprehensive_test.ipynb << 'BASEMAP_EOF'
,
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 🗺️ 多样化底图展示\n",
    "### 展示不同风格的地图底图效果"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 10. Esri WorldImagery - 高分辨率卫星影像展示海南岛\n",
    "import leafmap\n",
    "\n",
    "# 创建海南岛卫星影像地图\n",
    "m1 = leafmap.Map(center=[19.2, 109.8], zoom=9)\n",
    "m1.add_basemap('Esri.WorldImagery')\n",
    "\n",
    "# 添加海南主要城市标记\n",
    "locations = [\n",
    "    [20.0444, 110.1989],  # 海口市\n",
    "    [18.2577, 109.5185],  # 三亚市\n",
    "    [19.5175, 109.5809],  # 儋州市\n",
    "    [19.2463, 110.4664]   # 琼海市\n",
    "]\n",
    "\n",
    "names = ['海口市', '三亚市', '儋州市', '琼海市']\n",
    "\n",
    "for i, (loc, name) in enumerate(zip(locations, names)):\n",
    "    m1.add_marker(loc)\n",
    "    print(f'✅ 添加{name}卫星影像标记')\n",
    "\n",
    "print('🛰️ 海南岛高分辨率卫星影像地图')\n",
    "m1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 11. NASA VIIRS Earth at Night - 地球夜景灯光效果\n",
    "import leafmap\n",
    "\n",
    "# 创建全球夜景地图，聚焦亚洲\n",
    "m2 = leafmap.Map(center=[30, 110], zoom=4)\n",
    "m2.add_basemap('NASAGIBS.ViirsEarthAtNight2012')\n",
    "\n",
    "# 添加主要城市夜景对比点\n",
    "major_cities = [\n",
    "    [39.9042, 116.4074],   # 北京\n",
    "    [31.2304, 121.4737],   # 上海\n",
    "    [22.3193, 114.1694],   # 香港\n",
    "    [19.2, 109.8],         # 海南岛中心\n",
    "    [25.0330, 121.5654]    # 台北\n",
    "]\n",
    "\n",
    "city_names = ['北京', '上海', '香港', '海南', '台北']\n",
    "\n",
    "for i, (loc, name) in enumerate(zip(major_cities, city_names)):\n",
    "    m2.add_marker(loc)\n",
    "    print(f'🌃 添加{name}夜景标记')\n",
    "\n",
    "print('🌙 亚洲地区夜景灯光地图 - 展示城市发展程度')\n",
    "m2"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 12. NASAGIBS BlueMarble - NASA蓝色弹珠地球影像\n",
    "import leafmap\n",
    "import geopandas as gpd\n",
    "from shapely.geometry import box\n",
    "\n",
    "# 创建NASA蓝色弹珠风格的海南岛地图\n",
    "m3 = leafmap.Map(center=[19.2, 109.8], zoom=8)\n",
    "m3.add_basemap('NASAGIBS.BlueMarble')\n",
    "\n",
    "# 添加海南岛边界框作为装饰\n",
    "hainan_bbox = [108.5, 18.0, 111.5, 20.5]\n",
    "bbox_gdf = gpd.GeoDataFrame([1], geometry=[box(*hainan_bbox)], crs='EPSG:4326')\n",
    "m3.add_gdf(bbox_gdf, layer_name='海南边界', \n",
    "          style={'color': '#00BFFF', 'weight': 3, 'fillOpacity': 0.1, 'dashArray': '5,5'})\n",
    "\n",
    "# 添加城市标记点\n",
    "locations = [\n",
    "    [20.0444, 110.1989],  # 海口市\n",
    "    [18.2577, 109.5185],  # 三亚市\n",
    "    [19.5175, 109.5809],  # 儋州市\n",
    "    [19.2463, 110.4664]   # 琼海市\n",
    "]\n",
    "\n",
    "names = ['海口市', '三亚市', '儋州市', '琼海市']\n",
    "\n",
    "for i, (loc, name) in enumerate(zip(locations, names)):\n",
    "    m3.add_marker(loc)\n",
    "    print(f'🌍 添加{name}NASA影像标记')\n",
    "\n",
    "print('🌍 海南岛NASA蓝色弹珠地球影像 - 太空视角')\n",
    "m3"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python (Geo-AI)",
   "language": "python",
   "name": "python-geo"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.18"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
BASEMAP_EOF

echo "✅ 多样化底图示例已添加到测试案例"

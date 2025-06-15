# 时间序列分析和动画使用手册

## 功能概述

`05_Timelapse.ipynb`展示了如何创建时间序列动画，用于展示地理现象的时间变化过程，包括卫星影像时序分析、变化检测和动态可视化。

## 核心功能

### 1. 时序数据处理
```python
import leafmap

# 创建时间序列动画
m = leafmap.Map()
m.add_time_slider(
    layers=time_series_layers,
    labels=time_labels,
    time_interval=1
)
```

### 2. 动画生成功能
- **帧序列创建**: 将多时相数据组织为动画帧
- **时间控制**: 可控制的播放速度和方向
- **循环播放**: 支持循环和单次播放模式
- **导出功能**: 导出为GIF或MP4格式

### 3. 变化检测分析
```python
# 时间序列变化检测
def detect_changes(before_image, after_image):
    difference = after_image - before_image
    change_mask = np.abs(difference) > threshold
    return change_mask
```

### 4. 交互式时间轴
- **时间滑块**: 拖拽查看不同时间点
- **播放控制**: 播放、暂停、快进、倒退
- **时间标签**: 显示具体的时间信息
- **速度调节**: 调整播放速度

## 应用场景

### 1. 城市发展监测
- **城市扩张**: 城市边界变化动画
- **建筑发展**: 建筑密度变化过程
- **交通网络**: 道路网络发展历程
- **土地利用**: 土地利用类型变化

### 2. 环境变化监测
- **森林砍伐**: 森林覆盖变化动画
- **湖泊变化**: 水体面积变化过程
- **冰川消融**: 冰川退缩时序分析
- **沙漠化**: 土地沙漠化进程

### 3. 农业季节监测
- **作物生长**: 农作物生长周期动画
- **收获季节**: 收获活动时空分布
- **灌溉模式**: 农田灌溉变化模式
- **产量评估**: 产量变化趋势分析

### 4. 灾害影响评估
- **洪水过程**: 洪水淹没范围变化
- **火灾蔓延**: 森林火灾扩散过程
- **地震影响**: 地震前后对比分析
- **台风路径**: 台风移动轨迹动画

## 技术实现

### 1. 数据预处理
```python
# 时序数据标准化
def normalize_time_series(image_list):
    normalized_images = []
    for img in image_list:
        # 辐射定标
        normalized = (img - img.min()) / (img.max() - img.min())
        normalized_images.append(normalized)
    return normalized_images
```

### 2. 动画参数配置
```python
animation_config = {
    'fps': 2,                    # 帧率
    'duration': 10,              # 总时长(秒)
    'loop': True,                # 循环播放
    'reverse': False,            # 反向播放
    'fade_transition': True      # 淡入淡出效果
}
```

### 3. 性能优化
- **数据压缩**: 压缩影像数据减少内存占用
- **分辨率适配**: 根据显示需求调整分辨率
- **缓存机制**: 缓存处理结果提高响应速度
- **并行处理**: 多线程处理提高效率

---

*详细动画创建和高级时序分析功能正在完善中...*

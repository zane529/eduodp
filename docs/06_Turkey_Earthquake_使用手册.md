# 土耳其地震案例分析使用手册

## 功能概述
`06_Turkey_Earthquake.ipynb`以土耳其地震为案例，演示了灾害监测和影响评估的完整工作流程，包括灾前灾后数据对比、损失评估和应急响应数据产品生成。

## 核心功能

### 1. 灾害数据获取
```python
import leafmap

# 获取地震区域数据
earthquake_bbox = [35.0, 38.0, 37.0, 40.0]  # 土耳其地震区域
pre_disaster_date = "2023-01-01/2023-02-05"
post_disaster_date = "2023-02-07/2023-02-28"
```

### 2. 影响范围分析
- **建筑物损毁检测**: 基于高分辨率影像的建筑物损毁识别
- **道路中断分析**: 道路网络连通性分析
- **基础设施评估**: 关键基础设施受损情况
- **人口影响评估**: 受影响人口数量和分布

### 3. 损失评估方法
```python
# 变化检测分析
def assess_damage(pre_image, post_image):
    # 计算NDVI变化
    ndvi_change = calculate_ndvi_change(pre_image, post_image)
    
    # 建筑物指数变化
    ndbi_change = calculate_ndbi_change(pre_image, post_image)
    
    # 综合损失评估
    damage_index = combine_indices(ndvi_change, ndbi_change)
    return damage_index
```

### 4. 应急响应产品
- **快速评估报告**: 自动生成损失评估报告
- **优先救援区域**: 识别需要优先救援的区域
- **交通路线规划**: 应急救援路线规划
- **资源需求评估**: 救援资源需求量化分析

## 应用价值
- **灾害响应**: 为应急管理部门提供决策支持
- **损失评估**: 为保险和重建提供科学依据
- **经验总结**: 为未来类似灾害提供参考
- **方法验证**: 验证遥感技术在灾害评估中的有效性

---
*详细损失评估算法和应急响应流程正在完善中...*

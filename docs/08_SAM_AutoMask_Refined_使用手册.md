# SAM自动掩膜精化版使用手册

## 功能概述
`08_SAM_AutoMask (Refined).ipynb`是SAM自动掩膜的优化版本，提供了更精确的分割结果和更高效的处理流程。

## 核心改进

### 1. 精化分割算法
```python
from samgeo import SamGeo

# 精化版SAM配置
sam_refined = SamGeo(
    model_type="vit_h",
    checkpoint="sam_vit_h_4b8939.pth",
    device="cuda",
    # 精化参数
    points_per_side=64,        # 增加采样点密度
    pred_iou_thresh=0.88,      # 提高IoU阈值
    stability_score_thresh=0.95 # 提高稳定性阈值
)
```

### 2. 参数优化策略
- **采样密度优化**: 提高点采样密度获得更精细分割
- **阈值调优**: 优化IoU和稳定性阈值
- **后处理增强**: 改进的形态学处理
- **质量筛选**: 更严格的质量控制标准

### 3. 性能提升
- **内存优化**: 减少内存占用
- **速度提升**: 优化算法流程
- **批处理**: 支持更大规模数据
- **并行计算**: 多GPU并行处理

---
*详细优化参数和性能对比正在完善中...*

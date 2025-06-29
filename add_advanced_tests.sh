#!/bin/bash

# 添加STAC和SAM高级测试

echo "=== 添加高级测试功能 ==="

# 创建简化的Python测试脚本
cat > /home/ec2-user/SageMaker/stac_sam_tests.py << 'EOF'
# 海南天基观测数据科学分析与可视化系统 - Python测试脚本（GPU内存优化）

import leafmap
import samgeo
from samgeo import SamGeo, tms_to_geotiff
import torch
import os

print("=== 海南项目Python测试脚本（GPU内存优化版）===")

# GPU内存清理
torch.cuda.empty_cache()

# 1. 基础环境检查
print(f"GPU可用: {torch.cuda.is_available()}")
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"使用设备: {device}")

if torch.cuda.is_available():
    print(f"GPU设备: {torch.cuda.get_device_name(0)}")
    print(f"GPU总内存: {torch.cuda.get_device_properties(0).total_memory/1024**3:.2f} GB")
    print(f"GPU可用内存: {(torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_allocated())/1024**3:.2f} GB")

# 2. STAC卫星数据查询
print("\n=== STAC卫星数据查询 ===")
hainan_bbox = [108.5, 18.0, 111.5, 20.5]
url = 'https://earth-search.aws.element84.com/v1/'
collection = 'sentinel-2-l2a'
time_range = "2023-01-01/2023-12-31"

search = leafmap.stac_search(
    url=url,
    max_items=5,
    collections=[collection],
    bbox=hainan_bbox,
    datetime=time_range,
    query={"eo:cloud_cover": {"lt": 20}},
    get_gdf=True,
)

print(f"✅ 找到 {len(search)} 个卫星图像")

# 3. SAM AI图像分割测试（GPU内存优化）
print("\n=== SAM AI图像分割测试（GPU内存优化）===")

# 再次清理GPU内存
torch.cuda.empty_cache()

# 设置PyTorch内存分配策略
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'

# 下载测试图像
bbox = [110.0, 19.8, 110.2, 20.0]  # 海口附近
image_path = 'hainan_test.tif'

print("正在下载测试图像...")
tms_to_geotiff(
    output=image_path, 
    bbox=bbox, 
    zoom=15, 
    source='Satellite'
)
print("✅ 测试图像下载成功")

# 初始化SAM模型
print("正在初始化SAM模型...")
if torch.cuda.is_available():
    print(f"GPU内存使用前: {torch.cuda.memory_allocated()/1024**3:.2f} GB")

sam = SamGeo(
    model_type='vit_b',  # 使用较小模型避免内存不足
    device=device,
    sam_kwargs={'points_per_side': 8}  # 减少点数节省内存
)
print("✅ SAM模型初始化成功")

if torch.cuda.is_available():
    print(f"GPU内存使用后: {torch.cuda.memory_allocated()/1024**3:.2f} GB")

# 生成分割掩码
mask_path = 'hainan_mask.tif'
print("正在生成分割掩码...")
sam.generate(
    source=image_path,
    output=mask_path,
    foreground=True,
    unique=True
)
print("✅ 分割掩码生成成功")

# 转换为矢量格式
vector_path = 'hainan_segments.gpkg'
sam.tiff_to_gpkg(mask_path, vector_path)
print("✅ 矢量转换成功")

# 清理模型释放内存
del sam
torch.cuda.empty_cache()
print("✅ GPU内存已清理")

print(f"\n🎉 所有测试完成！输出文件: {vector_path}")
if torch.cuda.is_available():
    print(f"最终GPU内存使用: {torch.cuda.memory_allocated()/1024**3:.2f} GB")
EOF

echo "✅ 高级测试脚本创建完成"
echo "文件位置: /home/ec2-user/SageMaker/stac_sam_tests.py"

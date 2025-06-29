#!/bin/bash

# 海南天基观测数据科学分析与可视化系统 - 完整测试套件

echo "=== 海南项目完整测试套件 ==="
echo "开始时间: $(date)"

# 确保在正确目录
cd /home/ec2-user/SageMaker

echo "=== 第1步: 生成简化测试案例 ==="
bash update_test_cases.sh

echo "=== 第2步: 添加高级测试 ==="
bash add_advanced_tests.sh

echo "=== 第4步: 运行Python测试 ==="
# 激活正确的conda环境
source /home/ec2-user/anaconda3/etc/profile.d/conda.sh
conda activate JupyterSystemEnv

# 运行高级测试
python stac_sam_tests.py

echo "=== 测试完成 ==="
echo "结束时间: $(date)"
echo ""
echo "=== 生成的文件 ==="
echo "1. hainan_comprehensive_test.ipynb - Jupyter测试notebook"
echo "2. stac_sam_tests.py - Python高级测试脚本"
echo ""
echo "=== 使用说明 ==="
echo "1. 在Jupyter中打开 hainan_comprehensive_test.ipynb"
echo "2. 选择 'Python (Geo-AI)' 内核"
echo "3. 运行所有单元格进行交互式测试"
echo "4. 或直接运行: python stac_sam_tests.py"

#!/bin/bash

# 手动创建Python (Geo-AI)内核

echo "=== 创建Python (Geo-AI)内核 ==="

# 激活正确的conda环境
source /home/ec2-user/anaconda3/etc/profile.d/conda.sh
conda activate JupyterSystemEnv

echo "当前Python环境: $(which python)"
echo "当前conda环境: $CONDA_DEFAULT_ENV"

# 创建内核
echo "正在创建内核..."
python -m ipykernel install --user --name "python-geo" --display-name "Python (Geo-AI)"

# 验证内核创建
echo "=== 验证内核创建 ==="
jupyter kernelspec list

echo "✅ 内核创建完成"
echo "现在可以在Jupyter中选择 'Python (Geo-AI)' 内核了！"

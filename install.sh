#!/bin/bash

# 海南天基观测数据科学分析与可视化系统
# 完整安装脚本（包含测试案例生成）

echo "=== 海南项目完整安装 + 测试案例 ==="
echo "开始时间: $(date)"

# 第1步: 运行主安装脚本
echo "=== 第1步: 执行主安装 ==="
bash sagemaker_notebook_install_final.sh

# 检查安装是否成功
if [ $? -eq 0 ]; then
    echo "✅ 主安装完成"
    
    # 第1.5步: 确保内核创建
    echo "=== 第1.5步: 确保内核创建 ==="
    bash create_kernel.sh
    
    # 第2步: 生成测试案例
    echo "=== 第2步: 生成测试案例 ==="
    bash run_all_tests.sh
    
    echo "=== 安装和测试案例生成完成 ==="
    echo "🎉 海南天基观测数据科学分析与可视化系统已完全就绪！"
    
    echo ""
    echo "=== 可用的测试文件 ==="
    ls -la /home/ec2-user/SageMaker/*.ipynb
    ls -la /home/ec2-user/SageMaker/*test*.py
    
    echo ""
    echo "=== 重要提醒 ==="
    echo "✅ 请在Jupyter中选择 'Python (Geo-AI)' 内核"
    echo "✅ 如果看不到内核，请重启Jupyter Notebook"
    
else
    echo "❌ 主安装失败，跳过测试案例生成"
    exit 1
fi

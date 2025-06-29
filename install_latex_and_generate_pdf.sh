#!/bin/bash

echo "📚 ODP_Demo PDF图书生成环境安装脚本"
echo "=================================="

# 检查是否为macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "✅ 检测到macOS系统"
    
    # 检查Homebrew
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew未安装，请先安装Homebrew"
        echo "安装命令: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
    
    echo "🔧 开始安装LaTeX环境..."
    
    # 安装MacTeX (完整LaTeX环境)
    echo "📦 安装MacTeX (这可能需要几分钟)..."
    brew install --cask mactex
    
    # 安装图像处理工具
    echo "📦 安装图像处理工具..."
    brew install librsvg
    
    # 更新PATH
    echo "🔧 更新PATH环境变量..."
    export PATH="/usr/local/texlive/2023/bin/universal-darwin:$PATH"
    
    echo "✅ LaTeX环境安装完成"
    
else
    echo "❌ 此脚本仅支持macOS，请手动安装LaTeX环境"
    echo "Ubuntu: sudo apt install texlive-full texlive-xetex"
    echo "CentOS: sudo yum install texlive-scheme-full"
    exit 1
fi

echo ""
echo "🚀 开始生成专业PDF图书..."

# 运行PDF生成器
python3 create_professional_pdf.py

echo ""
echo "🎉 完成！如果成功，您现在应该有一个专业的PDF图书了。"
echo "💡 如果仍有问题，请重启终端后再试。"

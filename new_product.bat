@echo off
chcp 65001 >nul
title 隆腾智能 - 新产品创建工具
color 0A

echo.
echo ===============================================
echo           隆腾智能 - 新产品创建工具
echo ===============================================
echo.

set /p product_id="请输入产品ID (如: product03): "
if "%product_id%"=="" (
    echo 错误：产品ID不能为空！
    pause
    goto :eof
)

set /p product_name="请输入产品名称: "
if "%product_name%"=="" (
    echo 错误：产品名称不能为空！
    pause
    goto :eof
)

set /p product_price="请输入产品价格 (如: ¥2,999.00): "
if "%product_price%"=="" set product_price=¥0.00

echo.
echo 正在创建产品结构...
echo.

:: 创建产品图片目录
if not exist "Static" mkdir "Static"
mkdir "Static\%product_id%" 2>nul
echo ✓ 创建图片目录: Static\%product_id%\

:: 创建产品页面目录
if not exist "product" mkdir "product"
if not exist "product_null" mkdir "product_null"
echo ✓ 确保页面目录存在

:: 检查模板是否存在
if not exist "product-template.html" (
    echo ⚠ 警告：找不到产品页面模板 product-template.html
    echo   请先运行 Python 脚本创建模板文件
    pause
    goto :eof
)

:: 复制并修改模板
copy "product-template.html" "product\%product_id%.html" >nul
echo ✓ 创建产品页面: product\%product_id%.html

:: 创建简化版页面
copy "product-template.html" "product_null\%product_id%_null.html" >nul
echo ✓ 创建简化页面: product_null\%product_id%_null.html

:: 替换模板中的占位符
powershell -Command "(Get-Content 'product\%product_id%.html') -replace '{PRODUCT_NAME}', '%product_name%' -replace '{PRICE}', '%product_price%' -replace '{MAIN_IMAGE}', 'Static/%product_id%/overview.webp' | Set-Content 'product\%product_id%.html'"

echo.
echo ===============================================
echo              产品创建完成！
echo ===============================================
echo.
echo 产品ID:   %product_id%
echo 产品名称: %product_name%
echo 价格:     %product_price%
echo.
echo 📋 后续操作清单：
echo 1. 将产品图片放入 Static\%product_id%\ 目录
echo    - overview.webp (主图)
echo    - detail1.webp (详情图1) 
echo    - detail2.webp (详情图2)
echo.
echo 2. 编辑产品页面内容
echo    - product\%product_id%.html
echo.
echo 3. 更新产品目录页面
echo    - 在 catalog.html 中添加产品卡片
echo.
echo 4. 推荐使用 Python 脚本进行自动化管理
echo    - python manage_products.py
echo.
pause 
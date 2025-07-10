#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from pathlib import Path

def load_products_data():
    """加载产品数据"""
    try:
        with open('products.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("错误：找不到 products.json 文件")
        return None
    except json.JSONDecodeError as e:
        print(f"错误：JSON 格式错误 - {e}")
        return None

def load_template():
    """加载产品页面模板"""
    try:
        with open('product-template.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("错误：找不到 product-template.html 文件")
        return None

def generate_product_page(product, template):
    """为单个产品生成页面"""
    # 替换模板中的占位符
    page_content = template
    page_content = page_content.replace('{PRODUCT_NAME}', product['name'])
    page_content = page_content.replace('{BADGE}', product['badge'])
    
    # 修复图片路径：产品页面在子目录中，需要添加../ 前缀
    main_image_path = product['images']['main']
    if not main_image_path.startswith('../'):
        main_image_path = '../' + main_image_path
    page_content = page_content.replace('{MAIN_IMAGE}', main_image_path)
    
    page_content = page_content.replace('{LONG_DESCRIPTION}', product['longDescription'])
    
    return page_content

def create_directory_structure():
    """创建必要的目录结构"""
    directories = ['product', 'product_null']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"确保目录存在: {directory}/")

def generate_all_pages():
    """生成所有产品页面"""
    print("🚀 开始生成产品页面...")
    
    # 加载数据和模板
    data = load_products_data()
    if not data:
        return False
    
    template = load_template()
    if not template:
        return False
    
    # 创建目录结构
    create_directory_structure()
    
    # 生成每个产品的页面
    for product in data['products']:
        product_id = product['id']
        
        # 生成完整版产品页面
        page_content = generate_product_page(product, template)
        
        # 保存完整版产品页面
        full_page_path = f"product/{product_id}.html"
        with open(full_page_path, 'w', encoding='utf-8') as f:
            f.write(page_content)
        print(f"✅ 生成完整产品页面: {full_page_path}")
        
        # 生成简化版产品页面（无公司信息）
        simplified_content = generate_simplified_page(product, template)
        
        # 保存简化版产品页面
        simple_page_path = f"product_null/{product_id}_null.html"
        with open(simple_page_path, 'w', encoding='utf-8') as f:
            f.write(simplified_content)
        print(f"✅ 生成简化产品页面: {simple_page_path}")
    
    print(f"🎉 成功生成了 {len(data['products'])} 个产品的页面!")
    return True

def generate_simplified_page(product, template):
    """生成简化版产品页面（移除公司品牌信息）"""
    page_content = template
    
    # 替换基本信息
    page_content = page_content.replace('{PRODUCT_NAME}', product['name'])
    page_content = page_content.replace('{BADGE}', product['badge'])
    
    # 修复图片路径：简化版页面也在子目录中，需要添加../ 前缀
    main_image_path = product['images']['main']
    if not main_image_path.startswith('../'):
        main_image_path = '../' + main_image_path
    page_content = page_content.replace('{MAIN_IMAGE}', main_image_path)
    
    page_content = page_content.replace('{LONG_DESCRIPTION}', product['longDescription'])
    
    # 移除公司信息
    page_content = page_content.replace('隆腾智能', '产品展示')
    page_content = page_content.replace('| 隆腾智能', '')
    
    # 移除导航栏
    nav_start = page_content.find('<header>')
    nav_end = page_content.find('</header>') + len('</header>')
    if nav_start != -1 and nav_end != -1:
        page_content = page_content[:nav_start] + page_content[nav_end:]
    
    # 调整主内容的margin-top
    page_content = page_content.replace('margin-top: 80px;', 'margin-top: 20px;')
    
    # 移除聊天气泡
    chat_start = page_content.find('<!-- Chat Bubble -->')
    chat_end = page_content.find('</div>', chat_start) + len('</div>')
    if chat_start != -1 and chat_end != -1:
        page_content = page_content[:chat_start] + page_content[chat_end:]
    
    return page_content

def update_catalog_page():
    """更新产品目录页面"""
    print("🔄 更新产品目录页面...")
    
    data = load_products_data()
    if not data:
        return False
    
    try:
        # 读取现有的catalog.html
        with open('catalog.html', 'r', encoding='utf-8') as f:
            catalog_content = f.read()
        
        # 由于目录页面现在使用动态加载，这个函数不再需要更新静态HTML
        print("✅ 目录页面使用动态加载，无需更新静态HTML")
        return True
            
    except FileNotFoundError:
        print("错误：找不到 catalog.html 文件")
        return False

def main():
    """主函数"""
    print("=== 隆腾智能产品页面生成器 ===\n")
    
    if generate_all_pages():
        update_catalog_page()
        print("\n🎊 所有任务完成！")
        print("\n📝 使用说明：")
        print("1. 要添加新产品，请编辑 products.json 文件")
        print("2. 运行此脚本重新生成所有页面")
        print("3. 产品图片放在 Static/productXX/ 目录下")
        print("4. 完整版页面在 product/ 目录")
        print("5. 简化版页面在 product_null/ 目录")
    else:
        print("\n❌ 生成失败，请检查错误信息")

if __name__ == "__main__":
    main() 
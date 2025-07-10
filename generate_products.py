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
    page_content = page_content.replace('{PRICE}', product['price'])
    page_content = page_content.replace('{MAIN_IMAGE}', product['images']['main'])
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
    page_content = page_content.replace('{PRICE}', product['price'])
    page_content = page_content.replace('{MAIN_IMAGE}', product['images']['main'])
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
        
        # 生成产品卡片HTML
        product_cards = []
        for product in data['products']:
            card_html = f'''
                    <div class="product-card">
                        <div class="product-image">
                            <img src="{product['images']['main']}" alt="{product['name']}" 
                                 onerror="this.style.display='none'; this.parentElement.innerHTML='<div style=\\'display:flex;align-items:center;justify-content:center;height:100%;color:#666;font-size:1.2rem;\\'>📱 {product['name']}</div>'">
                        </div>
                        <div class="product-info">
                            <span class="product-badge">{product['badge']}</span>
                            <h3>{product['name']}</h3>
                            <p>{product['shortDescription']}</p>
                            <div class="product-specs">
                                {''.join([f'<span class="spec-item">{feature}</span>' for feature in product['features'][:4]])}
                            </div>
                            <div class="product-price">{product['price']}</div>
                            <a href="product/{product['id']}" class="btn btn-primary">查看详情</a>
                        </div>
                    </div>'''
            product_cards.append(card_html)
        
        # 更新产品网格内容 (查找products-grid)
        grid_start = catalog_content.find('<div class="products-grid" id="products-grid">')
        grid_end = catalog_content.find('</div>', grid_start) + len('</div>')
        
        if grid_start != -1 and grid_end != -1:
            new_grid = f'<div class="products-grid" id="products-grid">{"".join(product_cards)}\n                </div>'
            catalog_content = catalog_content[:grid_start] + new_grid + catalog_content[grid_end:]
            
            # 保存更新后的catalog.html
            with open('catalog.html', 'w', encoding='utf-8') as f:
                f.write(catalog_content)
            print("✅ 产品目录页面更新成功")
            return True
        else:
            print("⚠️  警告：无法找到产品网格区域")
            return False
            
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
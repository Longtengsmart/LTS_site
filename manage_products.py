#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
from pathlib import Path

def load_products():
    """加载产品数据"""
    try:
        with open('products.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"products": []}
    except json.JSONDecodeError as e:
        print(f"错误：JSON格式错误 - {e}")
        return None

def save_products(data):
    """保存产品数据"""
    try:
        with open('products.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存失败：{e}")
        return False

def list_products(data):
    """列出所有产品"""
    if not data or not data.get('products'):
        print("❌ 暂无产品数据")
        return
    
    print("\n📦 现有产品列表：")
    print("-" * 50)
    for i, product in enumerate(data['products'], 1):
        print(f"{i}. {product['name']} ({product['id']})")
        print(f"   💰 价格: {product['price']}")
        print(f"   🏷️  标签: {product['badge']}")
        print(f"   📝 简介: {product['shortDescription'][:50]}...")
        print()

def add_product(data):
    """添加新产品"""
    print("\n➕ 添加新产品")
    print("=" * 30)
    
    # 基本信息
    product_id = input("🆔 产品ID (如: product03): ").strip()
    if not product_id:
        print("❌ 产品ID不能为空")
        return False
    
    # 检查ID是否已存在
    existing_ids = [p['id'] for p in data['products']]
    if product_id in existing_ids:
        print("❌ 该产品ID已存在")
        return False
    
    name = input("📱 产品名称: ").strip()
    if not name:
        print("❌ 产品名称不能为空")
        return False
    
    category = input("📂 产品类别 (如: 显示器): ").strip() or "未分类"
    badge = input("🏷️  产品标签 (如: HOT/NEW): ").strip() or "NEW"
    price = input("💰 产品价格 (如: ¥2,999.00): ").strip() or "¥0.00"
    
    short_desc = input("📝 简短描述: ").strip()
    if not short_desc:
        print("❌ 简短描述不能为空")
        return False
    
    long_desc = input("📄 详细描述: ").strip() or short_desc
    
    # 图片信息
    print("\n🖼️  图片设置 (按回车使用默认路径):")
    main_image = input(f"主图路径 [Static/{product_id}/overview.webp]: ").strip()
    if not main_image:
        main_image = f"Static/{product_id}/overview.webp"
    
    # 产品特性
    print("\n⭐ 产品特性 (每行一个，空行结束):")
    features = []
    while True:
        feature = input(f"特性 {len(features)+1}: ").strip()
        if not feature:
            break
        features.append(feature)
    
    if not features:
        features = ["高品质", "智能化", "易安装"]
    
    # 应用场景
    print("\n🚗 应用场景:")
    applications = []
    
    for i in range(3):  # 最多3个应用场景
        print(f"\n应用场景 {i+1} (可选):")
        app_title = input("  标题: ").strip()
        if not app_title:
            break
        
        app_icon = input("  图标 (emoji): ").strip() or "🚗"
        app_desc = input("  描述: ").strip() or f"适用于{app_title}"
        
        applications.append({
            "icon": app_icon,
            "title": app_title,
            "description": app_desc
        })
    
    if not applications:
        applications = [
            {
                "icon": "🚗",
                "title": "通用车辆",
                "description": "适用于各类车型，提供优质的使用体验"
            }
        ]
    
    # 构建产品数据
    product = {
        "id": product_id,
        "name": name,
        "category": category,
        "badge": badge,
        "price": price,
        "shortDescription": short_desc,
        "longDescription": long_desc,
        "images": {
            "main": main_image,
            "gallery": [
                main_image,
                f"Static/{product_id}/detail1.webp",
                f"Static/{product_id}/detail2.webp"
            ]
        },
        "features": features,
        "specifications": {
            "基本参数": {
                "型号": product_id.upper(),
                "尺寸": "待确定",
                "重量": "待确定",
                "工作电压": "12V/24V"
            },
            "技术特性": {
                "接口类型": "CAN总线",
                "工作温度": "-20°C ~ 70°C",
                "防护等级": "IP65",
                "质保期": "2年"
            }
        },
        "applications": applications
    }
    
    # 添加到数据中
    data['products'].append(product)
    
    # 确认保存
    print("\n✅ 产品信息准备完成！")
    print(f"产品名称: {name}")
    print(f"产品ID: {product_id}")
    print(f"价格: {price}")
    
    confirm = input("\n确认保存？(y/N): ").strip().lower()
    if confirm == 'y':
        if save_products(data):
            print("✅ 产品添加成功！")
            print(f"💡 提示：请确保图片文件存在于 Static/{product_id}/ 目录下")
            return True
        else:
            print("❌ 保存失败")
            return False
    else:
        print("❌ 已取消添加")
        return False

def edit_product(data):
    """编辑产品"""
    if not data or not data.get('products'):
        print("❌ 暂无产品可编辑")
        return False
    
    list_products(data)
    
    try:
        choice = int(input("\n选择要编辑的产品编号: ")) - 1
        if choice < 0 or choice >= len(data['products']):
            print("❌ 无效的选择")
            return False
        
        product = data['products'][choice]
        print(f"\n✏️  编辑产品: {product['name']}")
        
        # 简单编辑几个关键字段
        new_name = input(f"产品名称 [{product['name']}]: ").strip()
        if new_name:
            product['name'] = new_name
        
        new_price = input(f"价格 [{product['price']}]: ").strip()
        if new_price:
            product['price'] = new_price
        
        new_badge = input(f"标签 [{product['badge']}]: ").strip()
        if new_badge:
            product['badge'] = new_badge
        
        new_short_desc = input(f"简短描述 [{product['shortDescription'][:30]}...]: ").strip()
        if new_short_desc:
            product['shortDescription'] = new_short_desc
        
        if save_products(data):
            print("✅ 产品信息更新成功！")
            return True
        else:
            print("❌ 保存失败")
            return False
            
    except ValueError:
        print("❌ 请输入有效的数字")
        return False

def delete_product(data):
    """删除产品"""
    if not data or not data.get('products'):
        print("❌ 暂无产品可删除")
        return False
    
    list_products(data)
    
    try:
        choice = int(input("\n选择要删除的产品编号: ")) - 1
        if choice < 0 or choice >= len(data['products']):
            print("❌ 无效的选择")
            return False
        
        product = data['products'][choice]
        print(f"\n⚠️  确认删除产品: {product['name']} ({product['id']})")
        confirm = input("确认删除？(y/N): ").strip().lower()
        
        if confirm == 'y':
            data['products'].pop(choice)
            if save_products(data):
                print("✅ 产品删除成功！")
                return True
            else:
                print("❌ 保存失败")
                return False
        else:
            print("❌ 已取消删除")
            return False
            
    except ValueError:
        print("❌ 请输入有效的数字")
        return False

def regenerate_pages():
    """重新生成页面"""
    print("\n🔄 重新生成产品页面...")
    
    # 检查生成脚本是否存在
    if not os.path.exists('generate_products.py'):
        print("❌ 找不到 generate_products.py 脚本")
        return False
    
    # 运行生成脚本
    try:
        import subprocess
        result = subprocess.run([sys.executable, 'generate_products.py'], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("✅ 页面生成成功！")
            print(result.stdout)
            return True
        else:
            print("❌ 页面生成失败：")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ 执行生成脚本失败：{e}")
        return False

def main_menu():
    """主菜单"""
    while True:
        print("\n" + "="*50)
        print("🏭 隆腾智能产品管理系统")
        print("="*50)
        print("1. 📋 查看产品列表")
        print("2. ➕ 添加新产品")
        print("3. ✏️  编辑产品")
        print("4. 🗑️  删除产品")
        print("5. 🔄 重新生成页面")
        print("6. 🚪 退出")
        print("-" * 50)
        
        choice = input("请选择操作 (1-6): ").strip()
        
        # 加载数据
        data = load_products()
        if data is None:
            print("❌ 数据加载失败，请检查 products.json 文件")
            continue
        
        if choice == '1':
            list_products(data)
        elif choice == '2':
            add_product(data)
        elif choice == '3':
            edit_product(data)
        elif choice == '4':
            delete_product(data)
        elif choice == '5':
            regenerate_pages()
        elif choice == '6':
            print("👋 再见!")
            break
        else:
            print("❌ 无效选择，请重新输入")
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    main_menu() 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
认知生态系统测试结果可视化

生成测试结果的图表和可视化报告
"""

import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import seaborn as sns
from datetime import datetime

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_test_results(filename: str):
    """加载测试结果"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_overall_performance_chart(results_data):
    """创建整体性能对比图"""
    # 提取成功的测试结果
    successful_results = []
    for model_name, result in results_data['individual_results'].items():
        if result.get('status') == 'success':
            successful_results.append({
                'model': model_name.split('/')[-1],  # 只取模型名称
                'service': result['service_name'],
                'hallucination_resistance': result['scores']['hallucination_resistance'],
                'role_consistency': result['scores']['role_consistency'],
                'cognitive_diversity': result['scores']['cognitive_diversity'],
                'overall_score': result['scores']['overall_score']
            })
    
    if not successful_results:
        print("没有成功的测试结果可以可视化")
        return
    
    df = pd.DataFrame(successful_results)
    
    # 创建子图
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('认知生态系统测试结果 - 整体性能对比', fontsize=16, fontweight='bold')
    
    # 1. 综合得分对比
    bars1 = ax1.bar(range(len(df)), df['overall_score'], 
                    color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    ax1.set_title('综合得分对比', fontweight='bold')
    ax1.set_ylabel('得分')
    ax1.set_xticks(range(len(df)))
    ax1.set_xticklabels(df['model'], rotation=45, ha='right')
    ax1.set_ylim(0, 1)
    
    # 添加数值标签
    for i, bar in enumerate(bars1):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom')
    
    # 2. 幻觉抵抗能力
    bars2 = ax2.bar(range(len(df)), df['hallucination_resistance'], 
                    color=['#FF9999', '#66B2FF', '#99FF99', '#FFB366'])
    ax2.set_title('幻觉抵抗能力', fontweight='bold')
    ax2.set_ylabel('得分')
    ax2.set_xticks(range(len(df)))
    ax2.set_xticklabels(df['model'], rotation=45, ha='right')
    ax2.set_ylim(0, 1)
    
    for i, bar in enumerate(bars2):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom')
    
    # 3. 角色一致性
    bars3 = ax3.bar(range(len(df)), df['role_consistency'], 
                    color=['#FFB3BA', '#BAFFC9', '#BAE1FF', '#FFFFBA'])
    ax3.set_title('角色一致性', fontweight='bold')
    ax3.set_ylabel('得分')
    ax3.set_xticks(range(len(df)))
    ax3.set_xticklabels(df['model'], rotation=45, ha='right')
    ax3.set_ylim(0, 1)
    
    for i, bar in enumerate(bars3):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom')
    
    # 4. 认知多样性
    bars4 = ax4.bar(range(len(df)), df['cognitive_diversity'], 
                    color=['#E6E6FA', '#F0E68C', '#DDA0DD', '#98FB98'])
    ax4.set_title('认知多样性', fontweight='bold')
    ax4.set_ylabel('得分')
    ax4.set_xticks(range(len(df)))
    ax4.set_xticklabels(df['model'], rotation=45, ha='right')
    ax4.set_ylim(0, 1)
    
    for i, bar in enumerate(bars4):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('cognitive_ecosystem_performance_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return df

def create_radar_chart(results_data):
    """创建雷达图对比"""
    # 提取成功的测试结果
    successful_results = []
    for model_name, result in results_data['individual_results'].items():
        if result.get('status') == 'success':
            successful_results.append({
                'model': model_name.split('/')[-1],
                'hallucination_resistance': result['scores']['hallucination_resistance'],
                'role_consistency': result['scores']['role_consistency'],
                'cognitive_diversity': result['scores']['cognitive_diversity']
            })
    
    if not successful_results:
        return
    
    # 设置雷达图参数
    categories = ['幻觉抵抗', '角色一致性', '认知多样性']
    N = len(categories)
    
    # 计算角度
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # 闭合图形
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    for i, result in enumerate(successful_results):
        values = [
            result['hallucination_resistance'],
            result['role_consistency'],
            result['cognitive_diversity']
        ]
        values += values[:1]  # 闭合图形
        
        ax.plot(angles, values, 'o-', linewidth=2, label=result['model'], color=colors[i % len(colors)])
        ax.fill(angles, values, alpha=0.25, color=colors[i % len(colors)])
    
    # 设置标签
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'])
    ax.grid(True)
    
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    plt.title('认知生态系统测试 - 雷达图对比', size=16, fontweight='bold', pad=20)
    
    plt.savefig('cognitive_ecosystem_radar_chart.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_role_performance_heatmap(results_data):
    """创建角色表现热力图"""
    # 提取角色详细得分
    role_data = []
    models = []
    
    for model_name, result in results_data['individual_results'].items():
        if result.get('status') == 'success' and 'detailed_role_scores' in result:
            models.append(model_name.split('/')[-1])
            role_scores = result['detailed_role_scores']
            role_data.append([
                role_scores.get('creator', 0),
                role_scores.get('analyst', 0),
                role_scores.get('critic', 0),
                role_scores.get('synthesizer', 0)
            ])
    
    if not role_data:
        print("没有角色详细得分数据可以可视化")
        return
    
    # 创建热力图
    role_names = ['创作者', '分析师', '批评家', '综合者']
    df_heatmap = pd.DataFrame(role_data, index=models, columns=role_names)
    
    plt.figure(figsize=(10, 6))
    sns.heatmap(df_heatmap, annot=True, cmap='RdYlGn', center=0.5, 
                fmt='.3f', cbar_kws={'label': '得分'})
    plt.title('各模型角色表现热力图', fontsize=16, fontweight='bold')
    plt.xlabel('角色类型')
    plt.ylabel('模型')
    
    plt.tight_layout()
    plt.savefig('cognitive_ecosystem_role_heatmap.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_summary_statistics(results_data):
    """创建汇总统计图"""
    summary = results_data['test_summary']
    
    # 创建饼图显示测试成功率
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 1. 测试成功率饼图
    labels = ['成功测试', '失败测试']
    sizes = [summary['successful_tests'], summary['failed_tests']]
    colors = ['#4CAF50', '#F44336']
    explode = (0.1, 0)  # 突出显示成功部分
    
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.set_title('测试成功率分布', fontweight='bold')
    
    # 2. 平均得分条形图
    successful_results = [r for r in results_data['individual_results'].values() 
                         if r.get('status') == 'success']
    
    if successful_results:
        avg_scores = {
            '幻觉抵抗': np.mean([r['scores']['hallucination_resistance'] for r in successful_results]),
            '角色一致性': np.mean([r['scores']['role_consistency'] for r in successful_results]),
            '认知多样性': np.mean([r['scores']['cognitive_diversity'] for r in successful_results]),
            '综合得分': np.mean([r['scores']['overall_score'] for r in successful_results])
        }
        
        bars = ax2.bar(avg_scores.keys(), avg_scores.values(), 
                      color=['#FF9800', '#2196F3', '#4CAF50', '#9C27B0'])
        ax2.set_title('平均得分统计', fontweight='bold')
        ax2.set_ylabel('平均得分')
        ax2.set_ylim(0, 1)
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{height:.3f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('cognitive_ecosystem_summary_stats.png', dpi=300, bbox_inches='tight')
    plt.show()

def generate_visual_report(results_filename):
    """生成完整的可视化报告"""
    print("🎨 生成认知生态系统测试结果可视化报告")
    print("=" * 50)
    
    # 加载测试结果
    results_data = load_test_results(results_filename)
    
    print("📊 创建整体性能对比图...")
    df = create_overall_performance_chart(results_data)
    
    print("🎯 创建雷达图对比...")
    create_radar_chart(results_data)
    
    print("🔥 创建角色表现热力图...")
    create_role_performance_heatmap(results_data)
    
    print("📈 创建汇总统计图...")
    create_summary_statistics(results_data)
    
    print("\n✅ 可视化报告生成完成！")
    print("生成的图表文件:")
    print("  - cognitive_ecosystem_performance_comparison.png")
    print("  - cognitive_ecosystem_radar_chart.png") 
    print("  - cognitive_ecosystem_role_heatmap.png")
    print("  - cognitive_ecosystem_summary_stats.png")
    
    return df

def main():
    """主函数"""
    # 查找最新的测试结果文件
    result_files = list(Path('.').glob('quick_cognitive_test_results_*.json'))
    
    if not result_files:
        print("❌ 没有找到测试结果文件")
        return
    
    # 使用最新的结果文件
    latest_file = max(result_files, key=lambda x: x.stat().st_mtime)
    print(f"📁 使用测试结果文件: {latest_file}")
    
    # 生成可视化报告
    df = generate_visual_report(str(latest_file))
    
    if df is not None:
        print(f"\n📋 测试结果数据框:")
        print(df.to_string(index=False))

if __name__ == "__main__":
    main()

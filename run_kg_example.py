#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
运行知识图谱推荐示例 / Run Knowledge Graph Recommendation Example

这个脚本演示如何使用生成的知识图谱文件在RecBole中训练知识感知推荐模型。
This script demonstrates how to use the generated knowledge graph files 
to train knowledge-aware recommendation models in RecBole.

使用方法 Usage:
    # 使用默认配置运行CKE模型
    python run_kg_example.py
    
    # 运行不同的模型
    python run_kg_example.py --model KGAT
    python run_kg_example.py --model RippleNet
    
    # 使用不同的数据集
    python run_kg_example.py --dataset product_example
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description='运行知识图谱推荐示例 / Run Knowledge Graph Recommendation Example')
    parser.add_argument('--model', type=str, default='CKE', 
                       help='模型名称 / Model name (default: CKE)')
    parser.add_argument('--dataset', type=str, default='movie_example',
                       help='数据集名称 / Dataset name (default: movie_example)')
    parser.add_argument('--config', type=str, default='kg_example_config.yaml',
                       help='配置文件路径 / Config file path (default: kg_example_config.yaml)')
    
    args = parser.parse_args()
    
    print("="*80)
    print("RecBole 知识图谱推荐示例 / RecBole Knowledge Graph Recommendation Example")
    print("="*80)
    print(f"\n模型 / Model: {args.model}")
    print(f"数据集 / Dataset: {args.dataset}")
    print(f"配置文件 / Config: {args.config}\n")
    
    # 检查是否已安装 RecBole
    try:
        from recbole.quick_start import run_recbole
        print("✓ RecBole 已安装 / RecBole is installed\n")
    except ImportError:
        print("✗ RecBole 未安装 / RecBole is not installed")
        print("\n请先安装 RecBole / Please install RecBole first:")
        print("  pip install recbole")
        print("\n或从源码安装 / Or install from source:")
        print("  cd RecBole")
        print("  pip install -e .\n")
        sys.exit(1)
    
    # 运行模型
    print("-"*80)
    print("开始训练 / Starting training...")
    print("-"*80 + "\n")
    
    try:
        run_recbole(
            model=args.model, 
            dataset=args.dataset, 
            config_file_list=[args.config]
        )
    except Exception as e:
        print(f"\n✗ 训练过程中出现错误 / Error during training: {e}")
        print("\n请确保:")
        print("Please ensure:")
        print("  1. 数据集文件存在 / Dataset files exist:")
        print(f"     - dataset/{args.dataset}/{args.dataset}.inter")
        print(f"     - dataset/{args.dataset}/{args.dataset}.kg")
        print(f"     - dataset/{args.dataset}/{args.dataset}.link")
        print(f"  2. 配置文件存在 / Config file exists: {args.config}")
        print(f"  3. 模型名称正确 / Model name is correct: {args.model}")
        print("\n支持的知识感知推荐模型 / Supported knowledge-aware models:")
        print("  CKE, KGAT, KGCN, KGNNLS, RippleNet, MKR, KTUP, KGIN, MCCLK, CFKG")
        sys.exit(1)


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
知识图谱三元组文件构建示例 / Knowledge Graph Triple File Builder Example

此脚本演示如何根据RecBole的格式要求构建知识图谱三元组文件和实体链接文件。
This script demonstrates how to build knowledge graph triple files and entity link files 
according to RecBole's format requirements.

RecBole要求的知识图谱文件包括两个部分：
RecBole requires two types of knowledge graph files:

1. .kg 文件 (Knowledge Graph Triples): 包含实体之间的关系三元组
   .kg file (Knowledge Graph Triples): Contains relationship triples between entities
   格式 Format: head_id:token   relation_id:token   tail_id:token

2. .link 文件 (Item-Entity Links): 将推荐系统中的物品ID映射到知识图谱中的实体ID
   .link file (Item-Entity Links): Maps item IDs in the recommendation system to entity IDs in the knowledge graph
   格式 Format: item_id:token   entity_id:token

使用方法 Usage:
    python build_kg_example.py --dataset_name example --output_dir ./dataset/example

作者 Author: RecBole Knowledge Graph Example
日期 Date: 2024
"""

import argparse
import os
import pandas as pd
from typing import List, Tuple, Dict


class KnowledgeGraphBuilder:
    """
    知识图谱三元组文件构建器
    Knowledge Graph Triple File Builder
    
    这个类提供了构建符合RecBole格式的知识图谱文件的方法。
    This class provides methods to build knowledge graph files in RecBole format.
    """
    
    def __init__(self, dataset_name: str, output_dir: str = './dataset'):
        """
        初始化构建器
        Initialize the builder
        
        Args:
            dataset_name: 数据集名称 / Dataset name
            output_dir: 输出目录 / Output directory
        """
        self.dataset_name = dataset_name
        self.output_dir = output_dir
        self.kg_file = os.path.join(output_dir, dataset_name, f"{dataset_name}.kg")
        self.link_file = os.path.join(output_dir, dataset_name, f"{dataset_name}.link")
        
        # 创建输出目录 / Create output directory
        os.makedirs(os.path.join(output_dir, dataset_name), exist_ok=True)
    
    def build_kg_triples(self, triples: List[Tuple[str, str, str]]) -> None:
        """
        构建知识图谱三元组文件 (.kg)
        Build knowledge graph triples file (.kg)
        
        Args:
            triples: 三元组列表，格式为 [(head_id, relation_id, tail_id), ...]
                     List of triples in format [(head_id, relation_id, tail_id), ...]
        
        示例 Example:
            triples = [
                ('entity_1', 'directed_by', 'entity_10'),
                ('entity_1', 'has_genre', 'entity_20'),
                ('entity_2', 'acted_by', 'entity_30'),
            ]
        """
        # 创建DataFrame
        # Create DataFrame
        df = pd.DataFrame(triples, columns=['head_id', 'relation_id', 'tail_id'])
        
        # 写入文件，第一行包含字段名和类型
        # Write to file, first row contains field names and types
        with open(self.kg_file, 'w', encoding='utf-8') as f:
            # 写入头部（字段名:类型）
            # Write header (field_name:type)
            f.write('head_id:token\trelation_id:token\ttail_id:token\n')
            
            # 写入数据
            # Write data
            for _, row in df.iterrows():
                f.write(f"{row['head_id']}\t{row['relation_id']}\t{row['tail_id']}\n")
        
        print(f"✓ 知识图谱三元组文件已创建 / Knowledge graph triples file created: {self.kg_file}")
        print(f"  共 {len(triples)} 条三元组 / Total {len(triples)} triples")
    
    def build_item_entity_links(self, links: List[Tuple[str, str]]) -> None:
        """
        构建物品-实体链接文件 (.link)
        Build item-entity link file (.link)
        
        Args:
            links: 链接列表，格式为 [(item_id, entity_id), ...]
                   List of links in format [(item_id, entity_id), ...]
        
        示例 Example:
            links = [
                ('item_1', 'entity_1'),
                ('item_2', 'entity_2'),
                ('item_3', 'entity_3'),
            ]
        """
        # 创建DataFrame
        # Create DataFrame
        df = pd.DataFrame(links, columns=['item_id', 'entity_id'])
        
        # 写入文件，第一行包含字段名和类型
        # Write to file, first row contains field names and types
        with open(self.link_file, 'w', encoding='utf-8') as f:
            # 写入头部（字段名:类型）
            # Write header (field_name:type)
            f.write('item_id:token\tentity_id:token\n')
            
            # 写入数据
            # Write data
            for _, row in df.iterrows():
                f.write(f"{row['item_id']}\t{row['entity_id']}\n")
        
        print(f"✓ 物品-实体链接文件已创建 / Item-entity link file created: {self.link_file}")
        print(f"  共 {len(links)} 条链接 / Total {len(links)} links")
    
    def build_from_dict(self, kg_data: Dict[str, List[Tuple[str, str]]], 
                       item_entity_map: Dict[str, str]) -> None:
        """
        从字典数据构建知识图谱文件
        Build knowledge graph files from dictionary data
        
        Args:
            kg_data: 知识图谱数据，格式为 {head_id: [(relation, tail_id), ...], ...}
                     Knowledge graph data in format {head_id: [(relation, tail_id), ...], ...}
            item_entity_map: 物品-实体映射，格式为 {item_id: entity_id, ...}
                             Item-entity mapping in format {item_id: entity_id, ...}
        
        示例 Example:
            kg_data = {
                'entity_1': [('directed_by', 'entity_10'), ('has_genre', 'entity_20')],
                'entity_2': [('acted_by', 'entity_30')],
            }
            item_entity_map = {
                'item_1': 'entity_1',
                'item_2': 'entity_2',
            }
        """
        # 将字典转换为三元组列表
        # Convert dictionary to triple list
        triples = []
        for head_id, relations in kg_data.items():
            for relation_id, tail_id in relations:
                triples.append((head_id, relation_id, tail_id))
        
        # 将字典转换为链接列表
        # Convert dictionary to link list
        links = [(item_id, entity_id) for item_id, entity_id in item_entity_map.items()]
        
        # 构建文件
        # Build files
        self.build_kg_triples(triples)
        self.build_item_entity_links(links)


def create_movie_example():
    """
    创建一个电影推荐的知识图谱示例
    Create a movie recommendation knowledge graph example
    
    此示例展示了如何为电影推荐系统构建知识图谱：
    - 电影与导演、演员、类型等实体的关系
    - 物品ID（电影ID）到实体ID的映射
    
    This example demonstrates how to build a knowledge graph for a movie recommendation system:
    - Relationships between movies and entities like directors, actors, genres
    - Mapping from item IDs (movie IDs) to entity IDs
    """
    print("\n" + "="*80)
    print("电影推荐知识图谱示例 / Movie Recommendation Knowledge Graph Example")
    print("="*80 + "\n")
    
    # 初始化构建器
    # Initialize builder
    builder = KnowledgeGraphBuilder(dataset_name='movie_example', output_dir='./dataset')
    
    # 方式1: 使用三元组列表构建
    # Method 1: Build using triple list
    print("方式1: 使用三元组列表 / Method 1: Using triple list\n")
    
    # 定义知识图谱三元组
    # Define knowledge graph triples
    # 格式: (头实体, 关系, 尾实体)
    # Format: (head_entity, relation, tail_entity)
    kg_triples = [
        # 电影相关的三元组
        # Movie related triples
        ('movie_1', 'directed_by', 'director_nolan'),
        ('movie_1', 'has_actor', 'actor_dicaprio'),
        ('movie_1', 'has_genre', 'genre_scifi'),
        ('movie_1', 'has_genre', 'genre_thriller'),
        
        ('movie_2', 'directed_by', 'director_tarantino'),
        ('movie_2', 'has_actor', 'actor_travolta'),
        ('movie_2', 'has_actor', 'actor_jackson'),
        ('movie_2', 'has_genre', 'genre_crime'),
        
        ('movie_3', 'directed_by', 'director_nolan'),
        ('movie_3', 'has_actor', 'actor_bale'),
        ('movie_3', 'has_genre', 'genre_action'),
        ('movie_3', 'has_genre', 'genre_crime'),
        
        # 导演之间的关系
        # Relations between directors
        ('director_nolan', 'won_award', 'award_oscar'),
        ('director_tarantino', 'won_award', 'award_oscar'),
        
        # 演员之间的关系
        # Relations between actors
        ('actor_dicaprio', 'collaborated_with', 'actor_bale'),
        ('actor_travolta', 'collaborated_with', 'actor_jackson'),
    ]
    
    # 定义物品-实体链接
    # Define item-entity links
    # 格式: (物品ID, 实体ID)
    # Format: (item_id, entity_id)
    item_links = [
        ('1', 'movie_1'),  # 物品1对应电影实体movie_1 / Item 1 maps to movie entity movie_1
        ('2', 'movie_2'),  # 物品2对应电影实体movie_2 / Item 2 maps to movie entity movie_2
        ('3', 'movie_3'),  # 物品3对应电影实体movie_3 / Item 3 maps to movie entity movie_3
    ]
    
    builder.build_kg_triples(kg_triples)
    builder.build_item_entity_links(item_links)
    
    print("\n" + "-"*80 + "\n")


def create_product_example():
    """
    创建一个商品推荐的知识图谱示例
    Create a product recommendation knowledge graph example
    """
    print("\n" + "="*80)
    print("商品推荐知识图谱示例 / Product Recommendation Knowledge Graph Example")
    print("="*80 + "\n")
    
    # 初始化构建器
    # Initialize builder
    builder = KnowledgeGraphBuilder(dataset_name='product_example', output_dir='./dataset')
    
    # 方式2: 使用字典构建
    # Method 2: Build using dictionary
    print("方式2: 使用字典数据 / Method 2: Using dictionary data\n")
    
    # 定义知识图谱数据（字典格式）
    # Define knowledge graph data (dictionary format)
    kg_data = {
        'product_laptop_1': [
            ('brand', 'brand_dell'),
            ('category', 'category_electronics'),
            ('has_feature', 'feature_16gb_ram'),
            ('has_feature', 'feature_ssd'),
        ],
        'product_laptop_2': [
            ('brand', 'brand_apple'),
            ('category', 'category_electronics'),
            ('has_feature', 'feature_retina_display'),
            ('has_feature', 'feature_m1_chip'),
        ],
        'product_phone_1': [
            ('brand', 'brand_apple'),
            ('category', 'category_electronics'),
            ('has_feature', 'feature_5g'),
        ],
        'brand_dell': [
            ('headquartered_in', 'location_usa'),
        ],
        'brand_apple': [
            ('headquartered_in', 'location_usa'),
            ('founded_by', 'person_jobs'),
        ],
    }
    
    # 定义物品-实体映射（字典格式）
    # Define item-entity mapping (dictionary format)
    item_entity_map = {
        '101': 'product_laptop_1',
        '102': 'product_laptop_2',
        '103': 'product_phone_1',
    }
    
    builder.build_from_dict(kg_data, item_entity_map)
    
    print("\n" + "-"*80 + "\n")


def print_file_format_guide():
    """
    打印文件格式说明
    Print file format guide
    """
    print("\n" + "="*80)
    print("RecBole 知识图谱文件格式说明 / RecBole Knowledge Graph File Format Guide")
    print("="*80 + "\n")
    
    print("1. 知识图谱三元组文件 (.kg) / Knowledge Graph Triples File (.kg)")
    print("-" * 80)
    print("   格式 Format: head_id:token\\trelation_id:token\\ttail_id:token")
    print("   说明 Description:")
    print("   - 第一行必须是字段定义: head_id:token, relation_id:token, tail_id:token")
    print("   - First line must be field definition")
    print("   - 使用制表符(\\t)分隔字段 / Use tab (\\t) to separate fields")
    print("   - head_id: 头实体ID / Head entity ID")
    print("   - relation_id: 关系类型 / Relation type")
    print("   - tail_id: 尾实体ID / Tail entity ID\n")
    
    print("   示例 Example:")
    print("   head_id:token\\trelation_id:token\\ttail_id:token")
    print("   movie_1\\tdirected_by\\tdirector_nolan")
    print("   movie_1\\thas_actor\\tactor_dicaprio")
    print("   movie_2\\thas_genre\\tgenre_action\n")
    
    print("2. 物品-实体链接文件 (.link) / Item-Entity Link File (.link)")
    print("-" * 80)
    print("   格式 Format: item_id:token\\tentity_id:token")
    print("   说明 Description:")
    print("   - 第一行必须是字段定义: item_id:token, entity_id:token")
    print("   - First line must be field definition")
    print("   - 使用制表符(\\t)分隔字段 / Use tab (\\t) to separate fields")
    print("   - item_id: 推荐系统中的物品ID / Item ID in recommendation system")
    print("   - entity_id: 知识图谱中的实体ID / Entity ID in knowledge graph\n")
    
    print("   示例 Example:")
    print("   item_id:token\\tentity_id:token")
    print("   1\\tmovie_1")
    print("   2\\tmovie_2")
    print("   3\\tmovie_3\n")
    
    print("3. 使用方法 / Usage")
    print("-" * 80)
    print("   创建知识图谱文件后，在RecBole配置文件中添加:")
    print("   After creating knowledge graph files, add to RecBole config:\n")
    print("   load_col:")
    print("       inter: [user_id, item_id]")
    print("       kg: [head_id, relation_id, tail_id]")
    print("       link: [item_id, entity_id]\n")
    print("   然后运行知识感知推荐模型，如CKE、KGAT等")
    print("   Then run knowledge-aware recommendation models like CKE, KGAT, etc.\n")
    print("="*80 + "\n")


def main():
    """
    主函数 / Main function
    """
    parser = argparse.ArgumentParser(
        description='RecBole 知识图谱三元组文件构建示例 / RecBole Knowledge Graph Builder Example'
    )
    parser.add_argument('--example', type=str, default='all', 
                       choices=['all', 'movie', 'product', 'guide'],
                       help='运行示例类型 / Example type to run (default: all)')
    
    args = parser.parse_args()
    
    print("\n" + "="*80)
    print(" RecBole 知识图谱三元组文件构建工具")
    print(" RecBole Knowledge Graph Triple File Builder")
    print("="*80)
    
    if args.example in ['all', 'guide']:
        print_file_format_guide()
    
    if args.example in ['all', 'movie']:
        create_movie_example()
    
    if args.example in ['all', 'product']:
        create_product_example()
    
    print("\n" + "="*80)
    print("完成! / Done!")
    print("="*80)
    print("\n生成的文件位于 / Generated files are in:")
    print("  - ./dataset/movie_example/ (电影示例 / Movie example)")
    print("  - ./dataset/product_example/ (商品示例 / Product example)")
    print("\n下一步 / Next steps:")
    print("  1. 检查生成的文件 / Check generated files")
    print("  2. 准备对应的 .inter 交互文件 / Prepare corresponding .inter interaction file")
    print("  3. 在RecBole中使用这些数据集训练知识感知推荐模型")
    print("     Use these datasets in RecBole to train knowledge-aware recommendation models")
    print("  4. 示例: python run_recbole.py --model=CKE --dataset=movie_example")
    print("     Example: python run_recbole.py --model=CKE --dataset=movie_example")
    print("\n")


if __name__ == '__main__':
    main()

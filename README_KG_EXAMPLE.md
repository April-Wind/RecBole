# 知识图谱三元组文件构建示例 / Knowledge Graph Triple File Builder Example

[English](#english) | [中文](#chinese)

---

## <a name="chinese"></a>中文说明

### 📚 简介

本示例演示如何使用RecBole库构建知识图谱三元组文件，用于知识感知推荐系统。

### 🚀 快速开始

#### 1. 生成知识图谱文件

```bash
# 运行示例脚本生成知识图谱文件
python build_kg_example.py

# 这将在 ./dataset/ 目录下创建两个示例数据集：
# - movie_example (电影推荐知识图谱)
# - product_example (商品推荐知识图谱)
```

#### 2. 验证生成的文件

```bash
# 运行测试脚本验证文件格式
python test_kg_files.py
```

#### 3. 在RecBole中使用

```bash
# 首先确保已安装RecBole
pip install recbole

# 运行知识感知推荐模型
python run_kg_example.py --model CKE --dataset movie_example

# 或使用其他模型
python run_kg_example.py --model KGAT --dataset product_example
```

### 📁 文件说明

| 文件 | 说明 |
|------|------|
| `build_kg_example.py` | 知识图谱文件构建脚本（主要工具） |
| `run_kg_example.py` | 运行知识感知推荐模型的示例脚本 |
| `test_kg_files.py` | 测试生成的知识图谱文件格式 |
| `kg_example_config.yaml` | RecBole配置文件示例 |
| `知识图谱构建指南.md` | 详细的中文使用指南 |
| `KG_BUILD_GUIDE.md` | 详细的英文使用指南 |
| `dataset/movie_example/` | 电影推荐知识图谱示例 |
| `dataset/product_example/` | 商品推荐知识图谱示例 |

### 📖 详细文档

请查看以下详细文档：

- **中文完整指南**: [知识图谱构建指南.md](./知识图谱构建指南.md)
- **English Full Guide**: [KG_BUILD_GUIDE.md](./KG_BUILD_GUIDE.md)

### 🎯 支持的模型

本示例支持以下知识感知推荐模型：

- **CKE** - Collaborative Knowledge base Embedding
- **KGAT** - Knowledge Graph Attention Network
- **KGCN** - Knowledge Graph Convolutional Network
- **KGNNLS** - Knowledge Graph Neural Network with Label Smoothness
- **RippleNet** - Propagation-based Knowledge Graph Network
- **MKR** - Multi-task Knowledge Graph Recommendation
- **KTUP** - Knowledge-aware Tuple-wise Learning
- **KGIN** - Knowledge Graph Integrated Network
- **MCCLK** - Meta-Context Contrastive Learning
- **CFKG** - Collaborative Filtering with Knowledge Graph

### 📊 生成的示例数据

#### 电影推荐示例 (movie_example)

包含16个知识图谱三元组和3个物品-实体链接：

```
movie_1 ---directed_by---> director_nolan
movie_1 ---has_actor---> actor_dicaprio
movie_1 ---has_genre---> genre_scifi
...
```

#### 商品推荐示例 (product_example)

包含14个知识图谱三元组和3个物品-实体链接：

```
product_laptop_1 ---brand---> brand_dell
product_laptop_1 ---has_feature---> feature_16gb_ram
...
```

### 🛠️ 自定义使用

#### 方式1: 使用三元组列表

```python
from build_kg_example import KnowledgeGraphBuilder

builder = KnowledgeGraphBuilder('my_dataset', './dataset')

kg_triples = [
    ('entity_1', 'relation_type', 'entity_2'),
    ('entity_1', 'another_relation', 'entity_3'),
]

item_links = [
    ('item_1', 'entity_1'),
    ('item_2', 'entity_2'),
]

builder.build_kg_triples(kg_triples)
builder.build_item_entity_links(item_links)
```

#### 方式2: 使用字典

```python
kg_data = {
    'entity_1': [('relation_1', 'entity_2'), ('relation_2', 'entity_3')],
    'entity_2': [('relation_3', 'entity_4')],
}

item_entity_map = {
    'item_1': 'entity_1',
    'item_2': 'entity_2',
}

builder.build_from_dict(kg_data, item_entity_map)
```

### ❓ 常见问题

**Q: 知识图谱数据从哪里获取？**

A: 可以从以下来源获取：
- 公开知识库：DBpedia, Freebase, Wikidata等
- 领域知识库：IMDB（电影）, MusicBrainz（音乐）等
- 自建知识库：根据业务数据构建

**Q: 为什么需要 .link 文件？**

A: .link 文件建立推荐系统中的物品ID和知识图谱中的实体ID之间的映射关系。

**Q: 如何在RecBole中使用生成的文件？**

A: 参见 `run_kg_example.py` 脚本或阅读详细文档。

### 📝 许可证

本项目基于 MIT License 开源。

---

## <a name="english"></a>English

### 📚 Introduction

This example demonstrates how to build knowledge graph triple files using RecBole library for knowledge-aware recommendation systems.

### 🚀 Quick Start

#### 1. Generate Knowledge Graph Files

```bash
# Run the example script to generate knowledge graph files
python build_kg_example.py

# This will create two example datasets in ./dataset/ directory:
# - movie_example (Movie recommendation knowledge graph)
# - product_example (Product recommendation knowledge graph)
```

#### 2. Validate Generated Files

```bash
# Run test script to validate file formats
python test_kg_files.py
```

#### 3. Use in RecBole

```bash
# First, ensure RecBole is installed
pip install recbole

# Run knowledge-aware recommendation model
python run_kg_example.py --model CKE --dataset movie_example

# Or use other models
python run_kg_example.py --model KGAT --dataset product_example
```

### 📁 File Description

| File | Description |
|------|-------------|
| `build_kg_example.py` | Knowledge graph file builder script (main tool) |
| `run_kg_example.py` | Example script to run knowledge-aware recommendation models |
| `test_kg_files.py` | Test script to validate generated knowledge graph files |
| `kg_example_config.yaml` | RecBole configuration file example |
| `知识图谱构建指南.md` | Detailed Chinese usage guide |
| `KG_BUILD_GUIDE.md` | Detailed English usage guide |
| `dataset/movie_example/` | Movie recommendation knowledge graph example |
| `dataset/product_example/` | Product recommendation knowledge graph example |

### 📖 Detailed Documentation

Please refer to the following detailed documentation:

- **Chinese Full Guide**: [知识图谱构建指南.md](./知识图谱构建指南.md)
- **English Full Guide**: [KG_BUILD_GUIDE.md](./KG_BUILD_GUIDE.md)

### 🎯 Supported Models

This example supports the following knowledge-aware recommendation models:

- **CKE** - Collaborative Knowledge base Embedding
- **KGAT** - Knowledge Graph Attention Network
- **KGCN** - Knowledge Graph Convolutional Network
- **KGNNLS** - Knowledge Graph Neural Network with Label Smoothness
- **RippleNet** - Propagation-based Knowledge Graph Network
- **MKR** - Multi-task Knowledge Graph Recommendation
- **KTUP** - Knowledge-aware Tuple-wise Learning
- **KGIN** - Knowledge Graph Integrated Network
- **MCCLK** - Meta-Context Contrastive Learning
- **CFKG** - Collaborative Filtering with Knowledge Graph

### 📊 Generated Example Data

#### Movie Recommendation Example (movie_example)

Contains 16 knowledge graph triples and 3 item-entity links:

```
movie_1 ---directed_by---> director_nolan
movie_1 ---has_actor---> actor_dicaprio
movie_1 ---has_genre---> genre_scifi
...
```

#### Product Recommendation Example (product_example)

Contains 14 knowledge graph triples and 3 item-entity links:

```
product_laptop_1 ---brand---> brand_dell
product_laptop_1 ---has_feature---> feature_16gb_ram
...
```

### 🛠️ Custom Usage

#### Method 1: Using Triple List

```python
from build_kg_example import KnowledgeGraphBuilder

builder = KnowledgeGraphBuilder('my_dataset', './dataset')

kg_triples = [
    ('entity_1', 'relation_type', 'entity_2'),
    ('entity_1', 'another_relation', 'entity_3'),
]

item_links = [
    ('item_1', 'entity_1'),
    ('item_2', 'entity_2'),
]

builder.build_kg_triples(kg_triples)
builder.build_item_entity_links(item_links)
```

#### Method 2: Using Dictionary

```python
kg_data = {
    'entity_1': [('relation_1', 'entity_2'), ('relation_2', 'entity_3')],
    'entity_2': [('relation_3', 'entity_4')],
}

item_entity_map = {
    'item_1': 'entity_1',
    'item_2': 'entity_2',
}

builder.build_from_dict(kg_data, item_entity_map)
```

### ❓ FAQ

**Q: Where to get knowledge graph data?**

A: You can obtain from:
- Public knowledge bases: DBpedia, Freebase, Wikidata, etc.
- Domain knowledge bases: IMDB (movies), MusicBrainz (music), etc.
- Self-built knowledge bases: Build from business data

**Q: Why do we need the .link file?**

A: The .link file establishes the mapping between item IDs in the recommendation system and entity IDs in the knowledge graph.

**Q: How to use the generated files in RecBole?**

A: See the `run_kg_example.py` script or read the detailed documentation.

### 📝 License

This project is open source under the MIT License.

---

**维护者 / Maintainer**: RecBole Team  
**最后更新 / Last Updated**: December 2024
